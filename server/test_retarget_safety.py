from __future__ import annotations

import json
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from fastapi import HTTPException

from server.api import retarget_run_api as run_api
from server.api.retarget_artifact_api import (
    JOBS,
    JOBS_LOCK,
    allocate_main_id,
    allocate_run_id,
    release_id_reservation,
    robot_dir,
)


class RetargetSafetyTests(unittest.TestCase):
    def tearDown(self) -> None:
        with JOBS_LOCK:
            JOBS.clear()
            run_api.JOB_CANCEL_EVENTS.clear()

    def test_robot_dir_validates_capsule_user_and_registered_variant(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            workspace = Path(name)
            capsule = workspace / "users" / "local_user" / "capsules" / "2609110001"
            capsule.mkdir(parents=True)
            with patch(
                "server.api.retarget_artifact_api.workspace_root",
                return_value=workspace,
            ):
                self.assertEqual(
                    (capsule / "retarget" / "g1_29dof").resolve(),
                    robot_dir("2609110001", "g1_29dof", "local_user"),
                )
                for capsule_id, user_id in (
                    ("../../escape", "local_user"),
                    ("2609110001", "../escape"),
                ):
                    with self.assertRaises(HTTPException):
                        robot_dir(capsule_id, "g1_29dof", user_id)
                with self.assertRaises(HTTPException):
                    robot_dir("2609110001", "../../variant", "local_user")

    def test_primary_prepare_overwrites_browser_source_from_capsule_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            rdir = Path(name)
            request = run_api.RunRequest(
                capsule_id="2609110001",
                robot_variant="g1_29dof",
                config={
                    "source": {"file": "../../untrusted.csv"},
                    "output": {},
                },
            )
            authoritative = {
                "capsule_id": "2609110001",
                "source": {
                    "type": "meva_csv",
                    "file": "workspace/users/local_user/capsules/2609110001/meva/source.csv",
                    "header_row_1based": 8,
                    "sampling_rate_hz": 100.0,
                },
            }
            meva_bin = rdir / "2609110001_meva_viewer.bin"
            meva_bin.write_bytes(b"bin")
            with (
                patch.object(run_api, "robot_dir", return_value=rdir),
                patch.object(run_api, "_registered_variant", return_value=object()),
                patch.object(
                    run_api, "_runtime_robot_config",
                    side_effect=lambda config, _variant: deepcopy(config),
                ),
                patch.object(run_api, "_capsule_runtime_context", return_value=authoritative),
                patch.object(run_api, "_normalize_ground_contact_estimation"),
                patch.object(run_api, "generate_meva_viewer_bin", return_value=meva_bin),
                patch.object(
                    run_api, "read_viewer_bin",
                    return_value=({"capsule_id": "2609110001"}, {}),
                ),
            ):
                prepared = run_api._prepare_run(request, "job-owner")
            try:
                saved = json.loads(prepared[3].read_text(encoding="utf-8"))
                self.assertEqual(
                    authoritative["source"]["file"], saved["source"]["original_file"],
                )
                self.assertEqual(str(meva_bin), saved["source"]["file"])
                self.assertEqual("2609110001", saved["capsule_id"])
                self.assertIn("job-owner", prepared[3].name)
            finally:
                prepared[3].unlink(missing_ok=True)
                release_id_reservation(prepared[5], "job-owner")

    def test_run_and_main_id_reservations_are_atomic(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)

            def reserve_run(index: int):
                return allocate_run_id(root, f"run-owner-{index}")

            with ThreadPoolExecutor(max_workers=8) as executor:
                runs = list(executor.map(reserve_run, range(16)))
            self.assertEqual(16, len({run_id for run_id, _ in runs}))

            primary_id = runs[0][0]

            def reserve_main(index: int):
                return allocate_main_id(root, primary_id, f"main-owner-{index}")

            with ThreadPoolExecutor(max_workers=8) as executor:
                mains = list(executor.map(reserve_main, range(16)))
            self.assertEqual(16, len({main_id for main_id, _ in mains}))

            for index, (_, marker) in enumerate(runs):
                release_id_reservation(marker, f"run-owner-{index}")
            for index, (_, marker) in enumerate(mains):
                release_id_reservation(marker, f"main-owner-{index}")

    def test_thread_start_failure_releases_primary_reservation(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            request_path = root / ".request.json"
            request_path.write_text(json.dumps({"source": {}}), encoding="utf-8")
            marker = root / ".2609110001.reserved"
            marker.write_text("fixed-job\n", encoding="utf-8")
            prepared = (
                "2609110001", root, ["python", str(request_path)], request_path, False, marker,
            )
            request = run_api.RunRequest(capsule_id="2609110001", config={})
            fake_uuid = type("FakeUUID", (), {"hex": "fixed-job"})()
            with (
                patch.object(run_api.uuid, "uuid4", return_value=fake_uuid),
                patch.object(run_api, "_prepare_run", return_value=prepared),
                patch.object(run_api.threading, "Thread") as thread_class,
            ):
                thread_class.return_value.start.side_effect = RuntimeError("no thread")
                with self.assertRaisesRegex(RuntimeError, "no thread"):
                    run_api.run_retarget_start(request)
            self.assertFalse(request_path.exists())
            self.assertFalse(marker.exists())
            self.assertNotIn("fixed-job", JOBS)

    def test_retarget_page_has_no_real_capsule_bootstrap_and_cards_use_text(self) -> None:
        root = Path(__file__).resolve().parents[1]
        page = (root / "app" / "retarget" / "index.html").read_text(encoding="utf-8")
        cards = (root / "app" / "assets" / "js" / "my-capsules.js").read_text(
            encoding="utf-8"
        )
        self.assertIn("const EMBEDDED_CONFIG = {};", page)
        self.assertNotIn("2606050001", page)
        self.assertIn("let contextReady = false;", page)
        self.assertNotIn("card.innerHTML", cards)
        self.assertEqual(4, page.count(">[ESC] Cancel</button>"))
        self.assertIn('/cancel`, {method:"POST"}', page)
        self.assertIn("setRetargetControlsLocked(true)", page)


if __name__ == "__main__":
    unittest.main()
