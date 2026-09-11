from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from server.api import retarget_run_api as api
from server.api.retarget_artifact_api import JOBS, JOBS_LOCK
from server.remote_ik_client import RemoteIKError, configured_backend


class RemoteIKCloudDispatchTest(unittest.TestCase):
    def tearDown(self) -> None:
        with JOBS_LOCK:
            JOBS.clear()

    def test_default_backend_preserves_local_python(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            self.assertEqual("local_python", configured_backend())

    def test_remote_primary_result_is_published_and_source_path_restored(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            request_path = root / ".2609110001_request_config.json"
            local_source = "workspace/users/user/capsules/capsule/meva/source.csv"
            request_path.write_text(json.dumps({
                "source": {"file": local_source},
                "output": {"run_id": "2609110001"},
            }), encoding="utf-8")
            received = root / ".received"
            destination = root / "2609110001"
            job_id = "cloud-job"
            with JOBS_LOCK:
                JOBS[job_id] = {"job_id": job_id, "status": "queued", "progress": 0.0}

            def fake_execute(**kwargs):
                received.mkdir()
                (received / "2609110001_primary_config.json").write_text(json.dumps({
                    "source": {"file": "workspace/remote_ik_worker/jobs/remote/package/source.csv"},
                    "output": {"run_id": "2609110001"},
                }), encoding="utf-8")
                (received / "2609110001_primary.npz").write_bytes(b"npz")
                kwargs["status_callback"]({
                    "job_id": "remote-job", "status": "running", "progress": 0.5,
                    "processed": 1, "total": 2, "source_frame": 1, "message": "1 / 2 frames",
                })
                return {"job_id": "remote-job", "status": "completed", "elapsed_sec": 1.25}

            with patch.object(api, "execute_remote_job", side_effect=fake_execute):
                api._run_remote_job(
                    job_id,
                    stage="primary",
                    config_path=request_path,
                    result_staging=received,
                    primary_directory=None,
                    iteration_diagnostics=False,
                    receive_finalize=lambda: api._receive_remote_primary(
                        received, destination, request_path, overwrite=False,
                    ),
                    success_finalize=lambda: api._existing_primary_result(destination),
                    failure_finalize=lambda logs: (destination, []),
                )

            job = JOBS[job_id]
            self.assertEqual("done", job["status"])
            self.assertEqual("remote-job", job["remote_job_id"])
            self.assertEqual(1.0, job["progress"])
            saved = json.loads(
                (destination / "2609110001_primary_config.json").read_text(encoding="utf-8")
            )
            self.assertEqual(local_source, saved["source"]["file"])
            self.assertFalse(request_path.exists())

    def test_remote_error_code_is_exposed_to_existing_job_status(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            config = root / "config.json"
            config.write_text("{}", encoding="utf-8")
            job_id = "failed-job"
            with JOBS_LOCK:
                JOBS[job_id] = {"job_id": job_id, "status": "queued", "progress": 0.0}
            with patch.object(
                api, "execute_remote_job",
                side_effect=RemoteIKError(
                    "robot_model_load_failure", "MJCF revision differs",
                    remote_job_id="remote-failed",
                ),
            ):
                api._run_remote_job(
                    job_id,
                    stage="primary",
                    config_path=config,
                    result_staging=root / "received",
                    primary_directory=None,
                    iteration_diagnostics=False,
                    success_finalize=lambda: (root, []),
                    failure_finalize=lambda logs: (root, ["error.log"]),
                )
            self.assertEqual("failed", JOBS[job_id]["status"])
            self.assertEqual("robot_model_load_failure", JOBS[job_id]["error_code"])
            self.assertEqual("remote-failed", JOBS[job_id]["remote_job_id"])


if __name__ == "__main__":
    unittest.main()
