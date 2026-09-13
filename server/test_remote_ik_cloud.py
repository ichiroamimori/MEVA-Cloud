from __future__ import annotations

import json
import pickle
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

from server.api import retarget_run_api as api
from server.api.retarget_artifact_api import JOBS, JOBS_LOCK
from server.remote_ik_client import RemoteIKError, configured_backend
from server.retarget.motion_io import save_motion_npz


class RemoteIKCloudDispatchTest(unittest.TestCase):
    def tearDown(self) -> None:
        with JOBS_LOCK:
            JOBS.clear()
            api.JOB_CANCEL_EVENTS.clear()

    def test_default_backend_preserves_local_python(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            self.assertEqual("local_python", configured_backend())

    def test_cloud_cancel_marks_queued_job_and_sets_event(self) -> None:
        with tempfile.TemporaryDirectory() as name, patch.object(
            api, "CLOUD_JOB_ROOT", Path(name)
        ):
            job_id = "c" * 32
            api._register_job(job_id, {
                "job_id": job_id, "run_id": "2609110001", "status": "queued",
                "progress": 0.0, "submitted_at": api._utc_now(),
                "finished_at": None,
            })
            cancelled = api.cancel_retarget_job(job_id)
            self.assertEqual("cancelled", cancelled["status"])
            self.assertTrue(api.JOB_CANCEL_EVENTS[job_id].is_set())
            stored = json.loads((Path(name) / f"{job_id}.json").read_text(encoding="utf-8"))
            self.assertEqual("cancelled", stored["status"])

    def test_cloud_restore_marks_interrupted_job_failed(self) -> None:
        with tempfile.TemporaryDirectory() as name, patch.object(
            api, "CLOUD_JOB_ROOT", Path(name)
        ):
            job_id = "d" * 32
            (Path(name) / f"{job_id}.json").write_text(json.dumps({
                "job_id": job_id, "run_id": "2609110001", "backend": "remote_python",
                "status": "running", "submitted_at": api._utc_now(),
                "finished_at": None,
            }), encoding="utf-8")
            api._restore_cloud_jobs()
            self.assertEqual("failed", JOBS[job_id]["status"])
            self.assertEqual("cloud_restarted", JOBS[job_id]["error_code"])

    def test_primary_request_can_select_local_when_server_default_is_remote(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            request = api.RunRequest(
                capsule_id="2609110001",
                robot_variant="g1_29dof",
                config={},
                backend="local_python",
            )
            prepared = (
                "2609110001", root, ["python", "primary_retarget.py"],
                root / ".request.json", False, None,
            )
            prepared[3].write_text(json.dumps({"source": {}}), encoding="utf-8")
            with (
                patch.dict("os.environ", {"MEVA_IK_BACKEND": "remote_python"}),
                patch.object(api, "_prepare_run", return_value=prepared),
                patch.object(api.threading, "Thread") as thread_class,
            ):
                job = api.run_retarget_start(request)

            self.assertEqual("local_python", job["backend"])
            self.assertIs(api._run_job, thread_class.call_args.kwargs["target"])
            thread_class.return_value.start.assert_called_once_with()

    def test_legacy_sync_endpoint_delegates_to_async_execution(self) -> None:
        completed = {
            "job_id": "job", "run_id": "2609110001", "status": "done",
            "files": ["2609110001_primary.npz"], "overwritten": False,
        }
        request = api.RunRequest(capsule_id="2609110001", config={})
        with patch.object(api, "run_retarget_start", return_value=completed) as start:
            with JOBS_LOCK:
                JOBS["job"] = dict(completed)
            result = api.run_retarget(request)
        start.assert_called_once_with(request)
        self.assertEqual("2609110001", result["run_id"])
        self.assertEqual(completed["files"], result["files"])

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

    def test_remote_main_pickle_is_rebuilt_from_canonical_npz(self) -> None:
        main_id = "2609110001-01"
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            staging = root / "received"
            destination = root / "destination"
            staging.mkdir()
            destination.mkdir()
            local_config = root / "request.json"
            local_config.write_text(json.dumps({
                "source": {"file": "workspace/users/local_user/capsules/source.csv"},
            }), encoding="utf-8")
            (staging / f"{main_id}_main_config.json").write_text(json.dumps({
                "source": {"file": "workspace/remote_ik_worker/package/source.csv"},
            }), encoding="utf-8")
            frames = 2
            save_motion_npz(
                staging / f"{main_id}_main.npz",
                {
                    "fps": 30.0,
                    "root_pos": np.zeros((frames, 3)),
                    "root_rot": np.tile([0.0, 0.0, 0.0, 1.0], (frames, 1)),
                    "dof_pos": np.zeros((frames, 1)),
                },
                joint_names=["joint"], root_rot_order="xyzw",
            )
            (staging / f"{main_id}_main_target.npz").write_bytes(b"target")
            (staging / f"{main_id}_main_viewer.bin").write_bytes(b"viewer")
            (staging / f"{main_id}_main.pkl").write_bytes(b"malicious remote pickle")

            with patch(
                "server.retarget.motion_io.pickle.load",
                side_effect=AssertionError("Remote pickle must not be loaded"),
            ):
                api._merge_remote_main_result(
                    staging, destination, local_config, main_id,
                )

            with (destination / f"{main_id}_main.pkl").open("rb") as stream:
                rebuilt = pickle.load(stream)
            self.assertEqual((frames, 3), rebuilt["root_pos"].shape)
            self.assertEqual((frames, 1), rebuilt["dof_pos"].shape)
            saved_config = json.loads(
                (destination / f"{main_id}_main_config.json").read_text(encoding="utf-8")
            )
            self.assertEqual(
                "workspace/users/local_user/capsules/source.csv",
                saved_config["source"]["file"],
            )


if __name__ == "__main__":
    unittest.main()
