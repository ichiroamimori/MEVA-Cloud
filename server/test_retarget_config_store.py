from __future__ import annotations

import json
import os
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from server.retarget_config_store import (
    ConfigNameCollision,
    ConfigStoreError,
    list_configs,
    load_config,
    runtime_config,
    save_user_config,
)
from server.api.retarget_api import (
    RunRequest,
    SharedConfigSaveRequest,
    _prepare_run,
    get_shared_config,
    get_shared_configs,
    save_shared_config,
)
from fastapi import HTTPException


BASE_CONFIG = {
    "schema_version": "1.0",
    "name": "Primary Standard",
    "retarget_stage": "primary",
    "robot": {
        "manufacturer": "unitree",
        "model": "g1",
        "variant": "g1_29dof",
        "mjcf": "server/robots/unitree/g1/g1_29dof.xml",
    },
    "mappings": [{
        "source_segment": "Pelvis",
        "target_link": "pelvis",
        "orientation_weight": 1.0,
        "position_weight": 0.0,
    }],
    "solver": {"name": "daqp", "max_iterations_per_frame": 20},
}


class RetargetConfigStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        root = Path(self.temporary.name)
        self.workspace = root / "workspace"
        self.assets = root / "retarget_assets"
        self.environment = patch.dict(os.environ, {
            "MEVA_WORKSPACE_ROOT": str(self.workspace),
            "MEVA_RETARGET_ASSETS_ROOT": str(self.assets),
        })
        self.environment.start()
        self.xenoma_directory = (
            self.assets / "configs" / "meva" / "unitree" / "g1_29dof"
        )
        self.xenoma_directory.mkdir(parents=True)
        (self.xenoma_directory / "primary_standard.json").write_text(
            json.dumps(BASE_CONFIG), encoding="utf-8"
        )
        (self.xenoma_directory / "main_standard.json").write_text(
            json.dumps({
                **BASE_CONFIG,
                "name": "Main Standard",
                "retarget_stage": "main",
                "main": {
                    "balance": {"support_margin_m": 0.02},
                    "posture": {"torso_pitch_deg": 0.0},
                },
            }),
            encoding="utf-8",
        )
        for number in (1, 2):
            capsule_id = f"260825000{number}"
            capsule = self.workspace / "users" / "local_user" / "capsules" / capsule_id
            meva = capsule / "meva"
            meva.mkdir(parents=True)
            filename = f"source_{number}.csv"
            (meva / filename).write_text("header\n", encoding="utf-8")
            (capsule / "metadata.json").write_text(json.dumps({
                "capsule_id": capsule_id,
                "meva_source": {
                    "file": f"meva/{filename}",
                    "header_row": 8,
                    "sampling_rate_hz": 100,
                },
            }), encoding="utf-8")

        primary_run_id = "2608250001"
        primary_run_directory = (
            self.workspace / "users" / "local_user" / "capsules" / "2608250001"
            / "retarget" / "g1_29dof" / primary_run_id
        )
        primary_run_directory.mkdir(parents=True)
        primary_snapshot = runtime_config(BASE_CONFIG, {
            "capsule_id": "2608250001",
            "source": {
                "file": "workspace/users/local_user/capsules/2608250001/meva/source_1.csv",
                "header_row": 8,
            },
            "sampling": {"rate_fps": 100.0},
        })
        primary_snapshot["output"]["run_id"] = primary_run_id
        (primary_run_directory / f"{primary_run_id}_primary_config.json").write_text(
            json.dumps(primary_snapshot), encoding="utf-8"
        )

    def tearDown(self) -> None:
        self.environment.stop()
        self.temporary.cleanup()

    def test_lists_xenoma_and_legacy_user_config(self) -> None:
        user_directory = (
            self.workspace / "users" / "local_user" / "retarget_assets"
            / "configs" / "meva" / "unitree" / "g1_29dof"
        )
        user_directory.mkdir(parents=True)
        (user_directory / "walking_test.json").write_text(
            json.dumps({"config_name": "Walking Test", "mappings": []}),
            encoding="utf-8",
        )
        records = list_configs(
            source_type="meva", manufacturer="unitree", robot_variant="g1_29dof"
        )
        self.assertEqual([(item.scope, item.name) for item in records], [
            ("xenoma", "Primary Standard"), ("user", "Walking Test")
        ])
        self.assertTrue(records[1].legacy)
        _, loaded = load_config(
            scope="user", filename="walking_test.json", source_type="meva",
            manufacturer="unitree", robot_variant="g1_29dof",
        )
        self.assertEqual(loaded["schema_version"], "1.0")
        self.assertEqual(loaded["name"], "Walking Test")

    def test_save_update_save_as_and_shared_fields(self) -> None:
        runtime = deepcopy(BASE_CONFIG)
        runtime.update({
            "capsule_id": "2608250001",
            "source": {"file": "workspace/users/local_user/capsules/2608250001/meva/a.csv"},
            "frame_range": {"start": 10, "stop": 20, "step": 1},
            "sampling": {"rate_fps": 60.0},
            "offsets": {"file": "offsets.json"},
            "output": {"run_id": "2608250001", "pkl_name": "run.pkl", "root_rot_order": "xyzw"},
        })
        record, saved = save_user_config(
            runtime, name="Factory Picking", source_type="meva",
            manufacturer="unitree", robot_variant="g1_29dof",
        )
        self.assertEqual(saved["schema_version"], "1.0")
        self.assertEqual(saved["name"], "Factory Picking")
        self.assertIn("mappings", saved)
        self.assertNotIn("mjcf", saved["robot"])
        for field in ("capsule_id", "source", "frame_range", "sampling", "offsets", "config_id"):
            self.assertNotIn(field, saved)
        self.assertEqual(saved["output"], {"root_rot_order": "xyzw"})

        runtime["solver"]["max_iterations_per_frame"] = 30
        updated, _ = save_user_config(
            runtime, name="Factory Picking", source_type="meva",
            manufacturer="unitree", robot_variant="g1_29dof",
            selected_scope="user", selected_filename=record.filename,
        )
        self.assertEqual(updated.filename, record.filename)

        copied, _ = save_user_config(
            runtime, name="Walking Test", source_type="meva",
            manufacturer="unitree", robot_variant="g1_29dof",
            selected_scope="user", selected_filename=record.filename,
        )
        self.assertNotEqual(copied.filename, record.filename)
        self.assertEqual(len([item for item in list_configs(
            source_type="meva", manufacturer="unitree", robot_variant="g1_29dof"
        ) if item.scope == "user"]), 2)

    def test_xenoma_name_is_read_only_and_paths_are_safe(self) -> None:
        with self.assertRaises(ConfigNameCollision):
            save_user_config(
                BASE_CONFIG, name="Primary Standard", source_type="meva",
                manufacturer="unitree", robot_variant="g1_29dof",
            )
        with self.assertRaises(ConfigStoreError):
            load_config(
                scope="xenoma", filename="../primary_standard.json",
                source_type="meva", manufacturer="unitree", robot_variant="g1_29dof",
            )

    def test_runtime_merge_uses_current_capsule_source(self) -> None:
        first = runtime_config(BASE_CONFIG, {
            "capsule_id": "2608250001",
            "source": {"file": "workspace/users/local_user/capsules/2608250001/meva/a.csv"},
            "sampling": {"rate_fps": 60.0},
        })
        second = runtime_config(BASE_CONFIG, {
            "capsule_id": "2608250002",
            "source": {"file": "workspace/users/local_user/capsules/2608250002/meva/b.csv"},
        })
        self.assertNotEqual(first["capsule_id"], second["capsule_id"])
        self.assertNotEqual(first["source"]["file"], second["source"]["file"])
        self.assertEqual(first["mappings"], second["mappings"])
        self.assertEqual(first["sampling"]["rate_fps"], 60.0)
        self.assertEqual(second["sampling"]["rate_fps"], 30.0)

    def test_api_list_load_save_and_xenoma_rejection(self) -> None:
        listed = get_shared_configs()
        self.assertEqual(listed["configs"][0]["scope"], "xenoma")
        self.assertFalse(listed["configs"][0]["writable"])
        loaded = get_shared_config(
            capsule_id="2608250002", scope="xenoma",
            filename="primary_standard.json",
        )
        self.assertIn("2608250002", loaded["config"]["source"]["file"])
        self.assertEqual(loaded["config"]["name"], "Primary Standard")

        payload = SharedConfigSaveRequest(
            capsule_id="2608250002",
            name="Factory Picking",
            selected_scope="xenoma",
            selected_filename="primary_standard.json",
            config=loaded["config"],
        )
        saved = save_shared_config(payload)
        self.assertEqual(saved["selection"]["scope"], "user")
        runtime_path = (
            self.workspace / "users" / "local_user" / "capsules" / "2608250002"
            / "retarget" / "g1_29dof" / "config.json"
        )
        snapshot = json.loads(runtime_path.read_text(encoding="utf-8"))
        self.assertEqual(snapshot["name"], "Factory Picking")
        self.assertIn("2608250002", snapshot["source"]["file"])

        payload.name = "Primary Standard"
        with self.assertRaises(HTTPException) as raised:
            save_shared_config(payload)
        self.assertEqual(raised.exception.status_code, 409)

    def test_primary_request_remains_a_complete_runtime_snapshot(self) -> None:
        loaded = get_shared_config(
            capsule_id="2608250001", scope="xenoma",
            filename="primary_standard.json",
        )
        request = RunRequest(
            capsule_id="2608250001",
            config=loaded["config"],
        )
        run_id, _, _, request_path, _ = _prepare_run(request)
        snapshot = json.loads(request_path.read_text(encoding="utf-8"))
        self.assertEqual(snapshot["name"], "Primary Standard")
        self.assertEqual(snapshot["capsule_id"], "2608250001")
        self.assertIn("2608250001", snapshot["source"]["file"])
        self.assertEqual(snapshot["mappings"], BASE_CONFIG["mappings"])
        self.assertEqual(snapshot["output"]["run_id"], run_id)
        self.assertNotIn("pkl_name", snapshot["output"])
        self.assertFalse(snapshot["output"]["save_diagnostics_csv"])

    def test_main_configs_are_stage_separated_loadable_and_saveable(self) -> None:
        primary_records = get_shared_configs(stage="primary")["configs"]
        main_records = get_shared_configs(stage="main")["configs"]
        self.assertEqual([item["name"] for item in primary_records], ["Primary Standard"])
        self.assertEqual([item["name"] for item in main_records], ["Main Standard"])
        self.assertFalse(main_records[0]["writable"])
        self.assertEqual(main_records[0]["stage"], "main")

        loaded = get_shared_config(
            capsule_id="2608250001",
            scope="xenoma",
            filename="main_standard.json",
            stage="main",
            run_id="2608250001",
        )
        self.assertEqual(loaded["config"]["name"], "Main Standard")
        self.assertEqual(loaded["config"]["retarget_stage"], "main")
        self.assertIn("main", loaded["config"])
        self.assertIn("2608250001", loaded["config"]["source"]["file"])

        payload = SharedConfigSaveRequest(
            capsule_id="2608250001",
            name="Factory Main",
            stage="main",
            run_id="2608250001",
            selected_scope="xenoma",
            selected_filename="main_standard.json",
            config=loaded["config"],
        )
        saved = save_shared_config(payload)
        self.assertEqual(saved["selection"]["scope"], "user")
        self.assertEqual(saved["selection"]["stage"], "main")
        self.assertEqual(saved["shared_config"]["retarget_stage"], "main")
        for field in (
            "capsule_id", "source", "frame_range", "sampling", "offsets",
            "primary_run_id", "main_id", "primary_post_csv", "main_input_csv",
        ):
            self.assertNotIn(field, saved["shared_config"])

        runtime_path = (
            self.workspace / "users" / "local_user" / "capsules" / "2608250001"
            / "retarget" / "g1_29dof" / "main_config.json"
        )
        runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
        self.assertEqual(runtime["name"], "Factory Main")
        self.assertIn("2608250001", runtime["source"]["file"])

        payload.name = "Main Standard"
        with self.assertRaises(HTTPException) as raised:
            save_shared_config(payload)
        self.assertEqual(raised.exception.status_code, 409)

    def test_primary_and_main_config_ui_use_shared_dropdown_and_save_modal(self) -> None:
        html = (Path(__file__).resolve().parents[1] / "app" / "retarget" / "index.html").read_text(
            encoding="utf-8"
        )
        self.assertIn('<select class="config-name" id="configName"', html)
        self.assertIn('<select class="config-name" id="configNameBottom"', html)
        self.assertIn('<select class="config-name" id="mainConfigName"', html)
        self.assertIn('<select class="config-name" id="mainConfigNameBottom"', html)
        self.assertNotIn('id="configName" type="text"', html)
        self.assertNotIn('id="mainConfigName" type="text"', html)
        self.assertIn('group.label = scope === "xenoma" ? "Xenoma" : "User"', html)
        self.assertIn('id="saveConfigModal"', html)
        self.assertIn('id="saveConfigName" type="text"', html)
        self.assertIn('saveConfigName.value = stage === "main"', html)
        self.assertIn('id="configDirtyIndicator"', html)
        self.assertIn('id="mainConfigDirtyIndicator"', html)
        self.assertIn('configSignature(cfg) !== baselineConfigSignature', html)
        self.assertIn('"frame_range", "sampling", "offsets"', html)
        self.assertIn('<div class="config-label-row">', html)
        self.assertIn('function applyConfig(cfg, {updateBaseline=false}={})', html)
        self.assertIn('function applyMainConfig(cfg, {updateBaseline=false}={})', html)
        self.assertIn('if(updateBaseline){', html)
        self.assertIn('applyConfig(data.config, {updateBaseline:true})', html)
        self.assertIn('loadRetargetContext({preserveWorkingConfig:true})', html)
        # After a run, reapply the authoritative Run Config so model-driven
        # controls such as selected collision pairs reflect the executed
        # snapshot. applyConfig intentionally does not update the Shared
        # Config baseline, so unsaved changes remain marked dirty.
        self.assertIn('loadRetargetedData({preserveWorkingConfig:false})', html)
        self.assertIn('A Run Config is a reproducibility snapshot', html)
        self.assertIn('/api/retarget/configs/load?', html)
        self.assertIn('applyConfig(data.config)', html)
        self.assertIn('stage: "main"', html)
        self.assertIn('loadSelectedMainSharedConfig(runId)', html)
        self.assertIn('id="targetRobotSelect"', html)
        self.assertIn('fetch("/api/retarget/robots"', html)
        self.assertIn('saveConfigStage === "main"', html)
        self.assertIn('Main Result Config is a Run snapshot', html)
        self.assertIn('Primary Standard', html)
        self.assertIn('Main Standard', html)
        self.assertNotIn('Xenoma Standard', html)
        self.assertNotIn('Robot Standard', html)


if __name__ == "__main__":
    unittest.main()
