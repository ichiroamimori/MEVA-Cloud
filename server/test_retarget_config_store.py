from __future__ import annotations

import json
import os
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from server.retarget_config_store import (
    ConfigStoreError,
    archive_config,
    list_configs,
    load_config,
    publish_to_workspace,
    replace_xenoma_standard,
    runtime_config,
    save_user_config,
)
from server.api.retarget_config_api import (
    SharedConfigSaveRequest,
    get_main_config,
    get_shared_config,
    get_shared_configs,
    replace_standard_config,
    save_shared_config,
)
from server.api.retarget_run_api import RunRequest, _prepare_run
from server.api.retarget_artifact_api import release_id_reservation
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
            ("xenoma_standard", "Primary Standard"), ("personal", "Walking Test")
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
            "note": "This belongs to one run only.",
            "source": {"file": "workspace/users/local_user/capsules/2608250001/meva/a.csv"},
            "frame_range": {"start": 10, "stop": 20, "step": 1},
            "sampling": {"rate_fps": 60.0},
            "offsets": {"file": "offsets.json"},
            "output": {"run_id": "2608250001", "pkl_name": "run.pkl", "root_rot_order": "xyzw"},
            "artifact_generation_id": "2608250001-01",
            "primary_motion_file": "2608250001_primary.npz",
            "primary_target_npz": "2608250001_primary_target.npz",
            "main_target_npz": "2608250001-01_main_target.npz",
            "main_runtime_context": {"primary_run_id": "2608250001"},
        })
        record, saved = save_user_config(
            runtime, name="Factory Picking", source_type="meva",
            manufacturer="unitree", robot_variant="g1_29dof",
        )
        self.assertEqual(saved["schema_version"], "1.0")
        self.assertEqual(saved["name"], "Factory Picking")
        self.assertIn("mappings", saved)
        self.assertNotIn("mjcf", saved["robot"])
        for field in ("capsule_id", "source", "frame_range", "sampling", "offsets", "note"):
            self.assertNotIn(field, saved)
        for field in (
            "artifact_generation_id", "primary_motion_file", "primary_target_npz",
            "main_target_npz", "main_runtime_context",
        ):
            self.assertNotIn(field, saved)
        self.assertRegex(saved["config_id"], r"^cfg_[0-9a-f]{32}$")
        self.assertEqual(saved["scope"], "personal")
        self.assertEqual(saved["owner_id"], "Xenoma_Admin_01")
        self.assertEqual(saved["target_robot"]["variant"], "g1_29dof")
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
        self.assertEqual(copied.filename, record.filename)
        self.assertEqual(len([item for item in list_configs(
            source_type="meva", manufacturer="unitree", robot_variant="g1_29dof"
        ) if item.scope == "personal"]), 1)

    def test_same_display_name_is_allowed_and_paths_are_safe(self) -> None:
        record, _ = save_user_config(
            BASE_CONFIG, name="Primary Standard", source_type="meva",
            manufacturer="unitree", robot_variant="g1_29dof",
        )
        self.assertEqual(record.scope, "personal")
        with self.assertRaises(ConfigStoreError):
            load_config(
                scope="xenoma", filename="../primary_standard.json",
                source_type="meva", manufacturer="unitree", robot_variant="g1_29dof",
            )
        with self.assertRaisesRegex(ConfigStoreError, "target_robot"):
            save_user_config(
                BASE_CONFIG, name="Wrong Robot", source_type="meva",
                manufacturer="booster", robot_variant="k1_22dof",
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

    def test_publish_copies_personal_and_archive_hides_workspace_config(self) -> None:
        personal_record, personal = save_user_config(
            BASE_CONFIG, name="Shared Walk", source_type="meva",
            manufacturer="unitree", robot_variant="g1_29dof",
        )
        workspace_record, workspace = publish_to_workspace(
            personal, name="Shared Walk", source_type="meva",
            manufacturer="unitree", robot_variant="g1_29dof",
        )
        self.assertNotEqual(personal_record.config_id, workspace_record.config_id)
        self.assertEqual(workspace["source_config_id"], personal_record.config_id)
        self.assertEqual(workspace_record.scope, "workspace")
        self.assertTrue(any(item.config_id == personal_record.config_id for item in list_configs(
            source_type="meva", manufacturer="unitree", robot_variant="g1_29dof",
        )))

        edited_record, edited = save_user_config(
            workspace, name="Shared Walk Updated", source_type="meva",
            manufacturer="unitree", robot_variant="g1_29dof",
            selected_scope="workspace", selected_filename=workspace_record.filename,
        )
        self.assertEqual(edited_record.config_id, workspace_record.config_id)
        self.assertEqual(edited_record.scope, "workspace")
        self.assertEqual(edited["version"], workspace["version"] + 1)

        archived = archive_config(
            scope="workspace", filename=edited_record.filename,
            source_type="meva", manufacturer="unitree", robot_variant="g1_29dof",
        )
        self.assertEqual(archived.status, "archived")
        active_ids = {item.config_id for item in list_configs(
            source_type="meva", manufacturer="unitree", robot_variant="g1_29dof",
        )}
        all_ids = {item.config_id for item in list_configs(
            source_type="meva", manufacturer="unitree", robot_variant="g1_29dof",
            include_archived=True,
        )}
        self.assertNotIn(workspace_record.config_id, active_ids)
        self.assertIn(workspace_record.config_id, all_ids)

        personal_archived = archive_config(
            scope="personal", filename=personal_record.filename,
            source_type="meva", manufacturer="unitree", robot_variant="g1_29dof",
        )
        self.assertEqual(personal_archived.status, "archived")
        self.assertNotIn(personal_record.config_id, {
            item.config_id for item in list_configs(
                source_type="meva", manufacturer="unitree", robot_variant="g1_29dof",
            )
        })

    def test_replace_standard_creates_new_generation_and_archives_old(self) -> None:
        old_record, old = load_config(
            scope="xenoma_standard", filename="primary_standard.json",
            source_type="meva", manufacturer="unitree", robot_variant="g1_29dof",
        )
        replacement_config = deepcopy(old)
        replacement_config["solver"]["max_iterations_per_frame"] = 44
        new_record, replacement, archived_record = replace_xenoma_standard(
            replacement_config,
            name="Primary Standard",
            filename="primary_standard.json",
            source_type="meva", manufacturer="unitree", robot_variant="g1_29dof",
        )
        self.assertNotEqual(new_record.config_id, old_record.config_id)
        self.assertEqual(replacement["source_config_id"], old_record.config_id)
        self.assertEqual(replacement["version"], old_record.version + 1)
        self.assertEqual(new_record.status, "active")
        self.assertEqual(archived_record.config_id, old_record.config_id)
        self.assertEqual(archived_record.status, "archived")
        self.assertEqual(new_record.standard_key, archived_record.standard_key)
        active_standard = [item for item in list_configs(
            source_type="meva", manufacturer="unitree", robot_variant="g1_29dof",
        ) if item.scope == "xenoma_standard"]
        self.assertEqual([item.config_id for item in active_standard], [new_record.config_id])

    def test_replace_standard_api_checks_server_side_role(self) -> None:
        request = SharedConfigSaveRequest(
            capsule_id="2608250001",
            name="Primary Standard",
            selected_scope="xenoma_standard",
            selected_filename="primary_standard.json",
            config=BASE_CONFIG,
        )
        with patch(
            "server.api.retarget_config_api.can_replace_standard", return_value=False,
        ), self.assertRaises(HTTPException) as raised:
            replace_standard_config(request)
        self.assertEqual(raised.exception.status_code, 403)

    def test_api_list_load_save_and_xenoma_rejection(self) -> None:
        listed = get_shared_configs()
        self.assertEqual(listed["configs"][0]["scope"], "xenoma_standard")
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
        self.assertEqual(saved["selection"]["scope"], "personal")
        runtime_path = (
            self.workspace / "users" / "local_user" / "capsules" / "2608250002"
            / "retarget" / "g1_29dof" / "config.json"
        )
        snapshot = json.loads(runtime_path.read_text(encoding="utf-8"))
        self.assertEqual(snapshot["name"], "Factory Picking")
        self.assertIn("2608250002", snapshot["source"]["file"])

        payload.name = "Primary Standard"
        same_name = save_shared_config(payload)
        self.assertEqual(same_name["selection"]["scope"], "personal")

    def test_primary_request_remains_a_complete_runtime_snapshot(self) -> None:
        loaded = get_shared_config(
            capsule_id="2608250001", scope="xenoma",
            filename="primary_standard.json",
        )
        request = RunRequest(
            capsule_id="2608250001",
            config=loaded["config"],
            note="Primary review note",
        )
        fake_bin = self.workspace / "users" / "local_user" / "capsules" / "2608250001" / "meva" / "2608250001_meva_viewer.bin"
        fake_bin.write_bytes(b"bin")
        with patch("server.api.retarget_run_api.generate_meva_viewer_bin", return_value=fake_bin), patch(
            "server.api.retarget_run_api.read_viewer_bin", return_value=({"capsule_id": "2608250001"}, {})
        ):
            run_id, _, _, request_path, _, reservation = _prepare_run(request, "test-job-1")
        snapshot = json.loads(request_path.read_text(encoding="utf-8"))
        self.assertEqual(snapshot["name"], "Primary Standard")
        self.assertEqual(snapshot["capsule_id"], "2608250001")
        self.assertEqual(snapshot["note"], "Primary review note")
        self.assertTrue(snapshot["source"]["file"].endswith("_meva_viewer.bin"))
        self.assertIn("2608250001", snapshot["source"]["original_file"])
        self.assertEqual(snapshot["retarget_job"]["capsule_id"], "2608250001")
        self.assertEqual(snapshot["mappings"], BASE_CONFIG["mappings"])
        self.assertEqual(snapshot["output"]["run_id"], run_id)
        self.assertNotIn("pkl_name", snapshot["output"])
        self.assertFalse(snapshot["output"]["save_diagnostics_csv"])
        request_path.unlink()
        release_id_reservation(reservation, "test-job-1")

    def test_main_context_and_ui_preserve_primary_frame_range(self) -> None:
        run_id = "2608250001"
        run = (
            self.workspace / "users" / "local_user" / "capsules" / "2608250001"
            / "retarget" / "g1_29dof" / run_id
        )
        config_path = run / f"{run_id}_primary_config.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        config["frame_range"] = {"start": 123, "stop": 456, "step": 1}
        config_path.write_text(json.dumps(config), encoding="utf-8")
        (run / f"{run_id}_primary.npz").write_bytes(b"present")

        context = get_main_config(
            capsule_id="2608250001",
            robot_variant="g1_29dof",
            run_id=run_id,
            main_id="new",
        )
        self.assertEqual(context["config"]["frame_range"], {
            "start": 123, "stop": 456, "step": 1,
        })

        html = (
            Path(__file__).resolve().parents[1] / "app" / "retarget" / "index.html"
        ).read_text(encoding="utf-8")
        self.assertIn(
            'preservedStart != null && preservedStart !== ""', html,
        )
        self.assertIn(
            'preservedEnd != null && preservedEnd !== ""', html,
        )

    def test_primary_request_refreshes_robot_metadata_from_manifest(self) -> None:
        config = deepcopy(BASE_CONFIG)
        config["robot"]["ui"] = {
            "skeleton": {"parts": [{"role": "stale", "pattern": "segment"}]}
        }
        request = RunRequest(
            capsule_id="2608250001",
            robot_variant="k1_22dof",
            config=config,
        )

        fake_bin = self.workspace / "users" / "local_user" / "capsules" / "2608250001" / "meva" / "2608250001_meva_viewer.bin"
        fake_bin.write_bytes(b"bin")
        with patch("server.api.retarget_run_api.generate_meva_viewer_bin", return_value=fake_bin), patch(
            "server.api.retarget_run_api.read_viewer_bin", return_value=({"capsule_id": "2608250001"}, {})
        ):
            _, _, _, request_path, _, reservation = _prepare_run(request, "test-job-2")
        snapshot = json.loads(request_path.read_text(encoding="utf-8"))

        self.assertEqual(snapshot["robot"]["variant"], "k1_22dof")
        parts = snapshot["robot"]["ui"]["skeleton"]["parts"]
        hand_parts = {
            part["body"]: part
            for part in parts
            if part.get("pattern") == "semantic_axis"
        }
        self.assertEqual(
            set(hand_parts), {"left_hand_link", "right_hand_link"}
        )
        self.assertEqual(snapshot["mappings"], BASE_CONFIG["mappings"])
        request_path.unlink()
        release_id_reservation(reservation, "test-job-2")

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
        self.assertEqual(saved["selection"]["scope"], "personal")
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
        self.assertEqual(save_shared_config(payload)["selection"]["scope"], "personal")

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
        self.assertIn('xenoma_standard: "Xenoma Standard"', html)
        self.assertIn('personal: "Personal"', html)
        self.assertIn('workspace: "Workspace"', html)
        self.assertIn('id="saveConfigModal"', html)
        self.assertIn('id="replaceStandardBtn"', html)
        self.assertIn('/api/retarget/configs/replace-standard', html)
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
        self.assertIn('class="joint-condition-group"', html)
        self.assertIn('id="accelerationLimitEnabled"', html)
        self.assertIn('id="accelerationLimitRadS2"', html)
        self.assertIn('class="mapping-weight-head"', html)
        self.assertIn('class="ignore-head">Ignore<br>axial rot.', html)
        self.assertIn('class="mapping-weight-head-sub">Ori. / Joint', html)
        self.assertIn('ori.disabled = !sel.value', html)
        self.assertIn('ori.disabled = !m?.source_segment', html)
        self.assertNotIn('class="joint-acceleration-input"', html)
        self.assertIn('analyticClusterMembers.has(joint.name)', html)
        self.assertIn('input.disabled=!analyticTargets.has(joint.name)', html)
        self.assertIn('id="rvShowA" type="checkbox" checked', html)
        self.assertIn('id="rvShowB" type="checkbox" checked', html)
        self.assertIn('localFrameTime(sf).toFixed(3)', html)
        self.assertNotIn('id="rvG1Visual"', html)
        self.assertNotIn('id="rvAPill"', html)
        self.assertNotIn('id="rvBPill"', html)
        self.assertIn(
            'data.config?.robot || null',
            html,
        )
        self.assertIn('id="targetRobotSelect"', html)
        self.assertIn('fetch("/api/retarget/robots"', html)
        self.assertIn('saveConfigStage === "main"', html)
        self.assertIn('Main Result Config is a Run snapshot', html)
        self.assertIn('id="primaryRunNote"', html)
        self.assertIn('id="mainRunNote"', html)
        self.assertIn('maxlength="2000"', html)
        self.assertIn('cfg.note = String(primaryRunNote?.value || "").trim()', html)
        self.assertIn('cfg.note = String(mainRunNote?.value || "").trim()', html)
        self.assertIn('Primary Standard', html)
        self.assertIn('Main Standard', html)
        self.assertIn('Xenoma Standard', html)
        self.assertNotIn('Robot Standard', html)


if __name__ == "__main__":
    unittest.main()
