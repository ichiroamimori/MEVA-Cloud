from __future__ import annotations

import json
import hashlib
import tempfile
import threading
import time
import unittest
import warnings
import zipfile
from pathlib import Path
from unittest.mock import patch

from server.ik_contract import (
    IKContractError,
    IKRequest,
    MANIFEST_JSON_HASH,
    RESULT_FORMAT,
    RESULT_MANIFEST_NAME,
    canonical_json_sha256,
    extract_request_archive,
    file_descriptor,
    read_request_manifest,
    robot_manifest_matches,
    sha256_file,
    write_request_archive,
    write_result_archive,
)
from server.remote_ik_client import build_request_archive, extract_result_archive
from server.remote_ik_client import configured_backend
from server.ik_execution import IKExecutionResult
from server.ik_execution import IKExecutionError, _prepare_config, _validated_output_ids
from server.retarget.viewer_data import _serialize_bin
import numpy as np
import server.remote_ik_worker as worker
from fastapi import HTTPException


class RemoteIKContractTest(unittest.TestCase):
    @staticmethod
    def _main_request() -> IKRequest:
        return IKRequest.from_dict({
            "schema_version": "1.0", "backend": "remote_python", "stage": "main",
            "client_job_id": "cloud-main-job",
            "robot": {"manufacturer": "unitree", "robot_id": "g1", "variant": "g1_29dof",
                      "manifest_sha256": "1" * 64, "model_sha256": "2" * 64,
                      "asset_bundle_sha256": "3" * 64},
            "config_path": "inputs/config.json",
            "files": [
                {"role": "config", "path": "inputs/config.json", "size": 0, "sha256": "4" * 64},
                {"role": "primary_motion", "path": "inputs/primary.npz", "size": 0, "sha256": "5" * 64},
                {"role": "primary_target", "path": "inputs/target.npz", "size": 0, "sha256": "6" * 64},
            ],
        })

    def test_result_manifest_verifies_files_and_does_not_extract_pickle(self) -> None:
        main_id = "2609110001-01"
        with tempfile.TemporaryDirectory() as name:
            directory = Path(name)
            output = directory / "worker-output"
            output.mkdir()
            for filename in (
                f"{main_id}_main.npz",
                f"{main_id}_main_config.json",
                f"{main_id}_main_target.npz",
                f"{main_id}_main_viewer.bin",
            ):
                (output / filename).write_bytes(filename.encode("utf-8"))
            (output / f"{main_id}_main.pkl").write_bytes(b"untrusted pickle bytes")
            archive = directory / "result.zip"
            write_result_archive(output, archive, self._main_request(), status="completed")

            extracted = directory / "extracted"
            names = extract_result_archive(
                archive, extracted, stage="main",
                client_job_id="cloud-main-job", artifact_id=main_id,
            )
            self.assertIn(f"{main_id}_main.pkl", names)
            self.assertFalse((extracted / f"{main_id}_main.pkl").exists())
            self.assertTrue((extracted / f"{main_id}_main.npz").exists())

    def test_worker_rejects_unsafe_output_ids_before_path_creation(self) -> None:
        primary = worker.IKRequest.from_dict({
            "schema_version": "1.0", "backend": "remote_python", "stage": "primary",
            "client_job_id": "job-id",
            "robot": {"manufacturer": "unitree", "robot_id": "g1", "variant": "g1_29dof",
                      "manifest_sha256": "1" * 64, "model_sha256": "2" * 64,
                      "asset_bundle_sha256": "3" * 64},
            "config_path": "inputs/config.json",
            "files": [
                {"role": "config", "path": "inputs/config.json", "size": 0, "sha256": "4" * 64},
                {"role": "source", "path": "inputs/source.csv", "size": 0, "sha256": "5" * 64},
            ],
        })
        with self.assertRaisesRegex(IKExecutionError, "Invalid Primary"):
            _validated_output_ids(primary, {"output": {"run_id": "../../escape"}})
    def test_request_backend_overrides_server_default(self) -> None:
        with patch.dict("os.environ", {"MEVA_IK_BACKEND": "remote_python"}):
            self.assertEqual("remote_python", configured_backend())
            self.assertEqual("local_python", configured_backend("local_python"))

    def test_manifest_json_hash_ignores_formatting_and_line_endings(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            directory = Path(name)
            compact = directory / "compact.json"
            formatted = directory / "formatted.json"
            changed = directory / "changed.json"
            compact.write_bytes(b'{"name":"G1","pose":{"qpos":[0,1]}}\n')
            formatted.write_bytes(
                b'{\r\n  "pose": { "qpos": [ 0, 1 ] },\r\n  "name": "G1"\r\n}\r\n'
            )
            changed.write_bytes(b'{"name":"G1","pose":{"qpos":[0,2]}}')

            self.assertEqual(
                canonical_json_sha256(compact),
                canonical_json_sha256(formatted),
            )
            self.assertNotEqual(
                canonical_json_sha256(compact),
                canonical_json_sha256(changed),
            )
            identity = {
                "manifest_sha256": sha256_file(compact),
                "manifest_json_sha256": canonical_json_sha256(compact),
            }
            self.assertNotEqual(identity["manifest_sha256"], sha256_file(formatted))
            self.assertTrue(robot_manifest_matches(formatted, identity))
            self.assertFalse(robot_manifest_matches(changed, identity))

    def test_worker_job_endpoints_require_configured_token(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(HTTPException) as missing:
                worker._authorize(None)
            self.assertEqual(503, missing.exception.status_code)
        with patch.dict("os.environ", {"MEVA_IK_WORKER_TOKEN": "secret"}):
            worker._authorize("Bearer secret")
            with self.assertRaises(HTTPException) as invalid:
                worker._authorize("Bearer wrong")
            self.assertEqual(401, invalid.exception.status_code)

    def test_primary_package_has_logical_paths_and_valid_checksums(self) -> None:
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(dir=root / "workspace") as name:
            directory = Path(name)
            source = directory / "motion.bin"
            source.write_bytes(b"versioned meva bin")
            config = directory / "config.json"
            config.write_text(json.dumps({
                "robot": {"manufacturer": "unitree", "model": "g1", "variant": "g1_29dof"},
                "source": {"file": source.relative_to(root).as_posix()},
                "output": {"run_id": "2609110001"},
            }), encoding="utf-8")
            archive = directory / "request.zip"
            manifest = build_request_archive(
                destination=archive, repository_root=root, stage="primary",
                client_job_id="cloud-job-1", config_path=config,
            )
            self.assertEqual("inputs/source.bin", manifest["files"][1]["path"])
            self.assertEqual(RESULT_FORMAT, manifest["result"]["format"])
            self.assertEqual(MANIFEST_JSON_HASH, manifest["robot"]["manifest_hash_algorithm"])
            self.assertEqual(64, len(manifest["robot"]["manifest_json_sha256"]))
            self.assertNotIn(str(root), json.dumps(manifest))
            request = read_request_manifest(archive)
            extracted = directory / "extracted"
            extract_request_archive(archive, extracted, request, max_uncompressed_bytes=1024 * 1024)
            self.assertEqual(source.read_bytes(), (extracted / "inputs/source.bin").read_bytes())
            packaged_config = json.loads((extracted / "inputs/config.json").read_text(encoding="utf-8"))
            self.assertEqual("package://source", packaged_config["source"]["file"])

    def test_worker_uses_capsule_id_without_bvh_from_primary_bin(self) -> None:
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(dir=root / "workspace") as name:
            directory = Path(name)
            source = directory / "motion.bin"
            source.write_bytes(_serialize_bin(
                {
                    "kind": "meva", "capsule_id": "2609110001", "fps": 100.0,
                    "segment_names": ["Pelvis"], "joint_names": ["dummy"],
                    "quaternion_order": "wxyz", "gcp_names": ["left_ff"],
                },
                {
                    "source_frame": np.array([0], dtype=np.int32),
                    "segment_pos": np.zeros((1, 1, 3), dtype=np.float32),
                    "segment_quat": np.array([[[1, 0, 0, 0]]], dtype=np.float32),
                    "joint_pos": np.zeros((1, 1, 3), dtype=np.float32),
                    "gcp": np.zeros((1, 1), dtype=np.float32),
                },
            ))
            config = directory / "config.json"
            config.write_text(json.dumps({
                "capsule_id": "9999999999",
                "robot": {"manufacturer": "unitree", "model": "g1", "variant": "g1_29dof"},
                "source": {"file": source.relative_to(root).as_posix()},
                "output": {"run_id": "2609110001"},
            }), encoding="utf-8")
            archive = directory / "request.zip"
            build_request_archive(
                destination=archive, repository_root=root, stage="primary",
                client_job_id="cloud-job-bin", config_path=config,
            )
            request = read_request_manifest(archive)
            package = directory / "package"
            extract_request_archive(
                archive, package, request, max_uncompressed_bytes=16 * 1024 * 1024,
            )
            execution = directory / "execution"
            execution.mkdir()
            prepared, _ = _prepare_config(request, package, execution, root)
            worker_config = json.loads(prepared.read_text(encoding="utf-8"))
            self.assertEqual(worker_config["capsule_id"], "2609110001")
            self.assertNotIn("bvh", worker_config["source"])

    def test_checksum_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            directory = Path(name)
            config = directory / "config.json"
            source = directory / "source.csv"
            config.write_text("{}", encoding="utf-8")
            source.write_text("x", encoding="utf-8")
            files = [
                file_descriptor("config", "inputs/config.json", config),
                file_descriptor("source", "inputs/source.csv", source),
            ]
            files[1]["sha256"] = "0" * 64
            manifest = {
                "schema_version": "1.0", "backend": "remote_python", "stage": "primary",
                "client_job_id": "job-1",
                "robot": {"manufacturer": "unitree", "robot_id": "g1", "variant": "g1_29dof",
                          "manifest_sha256": "1" * 64, "model_sha256": "2" * 64,
                          "asset_bundle_sha256": "3" * 64},
                "config_path": "inputs/config.json", "files": files,
            }
            archive = directory / "request.zip"
            write_request_archive(archive, manifest, (
                ("inputs/config.json", config), ("inputs/source.csv", source),
            ))
            with self.assertRaisesRegex(IKContractError, "Checksum mismatch"):
                extract_request_archive(
                    archive, directory / "out", read_request_manifest(archive),
                    max_uncompressed_bytes=1024,
                )

    def test_result_zip_rejects_parent_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            directory = Path(name)
            archive = directory / "result.zip"
            payload = b"bad"
            result_manifest = {
                "schema_version": "1.0", "format": RESULT_FORMAT,
                "stage": "primary", "status": "failed",
                "client_job_id": "cloud-job", "artifact_id": "2609110001",
                "files": [{
                    "path": "../escape.txt", "size": len(payload),
                    "sha256": hashlib.sha256(payload).hexdigest(),
                }],
            }
            with zipfile.ZipFile(archive, "w") as output:
                output.writestr(RESULT_MANIFEST_NAME, json.dumps(result_manifest))
                output.writestr("../escape.txt", payload)
            with self.assertRaisesRegex(Exception, "Unsafe package path"):
                extract_result_archive(
                    archive, directory / "out", stage="primary",
                    client_job_id="cloud-job", artifact_id="2609110001",
                )
            self.assertFalse((directory / "escape.txt").exists())

    def test_result_zip_rejects_checksum_duplicate_and_undeclared_files(self) -> None:
        main_id = "2609110001-01"
        with tempfile.TemporaryDirectory() as name:
            directory = Path(name)
            output = directory / "worker-output"
            output.mkdir()
            for filename in (
                f"{main_id}_main.npz",
                f"{main_id}_main_config.json",
                f"{main_id}_main_target.npz",
                f"{main_id}_main.pkl",
                f"{main_id}_main_viewer.bin",
            ):
                (output / filename).write_bytes(filename.encode("utf-8"))
            archive = directory / "result.zip"
            write_result_archive(output, archive, self._main_request(), status="completed")

            with zipfile.ZipFile(archive, "a") as modified:
                modified.writestr(f"{main_id}_payload.exe", b"unexpected")
            with self.assertRaisesRegex(Exception, "file set"):
                extract_result_archive(
                    archive, directory / "undeclared", stage="main",
                    client_job_id="cloud-main-job", artifact_id=main_id,
                )

            archive.unlink()
            write_result_archive(output, archive, self._main_request(), status="completed")
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                with zipfile.ZipFile(archive, "a") as modified:
                    modified.writestr(f"{main_id}_main.npz", b"tampered")
            with self.assertRaisesRegex(Exception, "duplicate file names"):
                extract_result_archive(
                    archive, directory / "tampered", stage="main",
                    client_job_id="cloud-main-job", artifact_id=main_id,
                )

            archive.unlink()
            write_result_archive(output, archive, self._main_request(), status="completed")
            with zipfile.ZipFile(archive) as source:
                entries = {
                    info.filename: source.read(info)
                    for info in source.infolist()
                    if not info.is_dir()
                }
            manifest = json.loads(entries[RESULT_MANIFEST_NAME])
            manifest["files"][0]["sha256"] = "0" * 64
            entries[RESULT_MANIFEST_NAME] = json.dumps(manifest).encode("utf-8")
            checksum_archive = directory / "checksum.zip"
            with zipfile.ZipFile(checksum_archive, "w") as modified:
                for filename, payload in entries.items():
                    modified.writestr(filename, payload)
            with self.assertRaisesRegex(Exception, "checksum mismatch"):
                extract_result_archive(
                    checksum_archive, directory / "checksum", stage="main",
                    client_job_id="cloud-main-job", artifact_id=main_id,
                )

    def test_worker_submit_status_and_result_are_asynchronous(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            directory = Path(name)
            config = directory / "config.json"
            source = directory / "source.csv"
            config.write_text("{}", encoding="utf-8")
            source.write_text("frame\n0\n", encoding="utf-8")
            files = [
                file_descriptor("config", "inputs/config.json", config),
                file_descriptor("source", "inputs/source.csv", source),
            ]
            manifest = {
                "schema_version": "1.0", "backend": "remote_python", "stage": "primary",
                "client_job_id": "cloud-job-2",
                "robot": {"manufacturer": "unitree", "robot_id": "g1", "variant": "g1_29dof",
                          "manifest_sha256": "1" * 64, "model_sha256": "2" * 64,
                          "asset_bundle_sha256": "3" * 64},
                "config_path": "inputs/config.json", "files": files,
            }
            archive = directory / "request.zip"
            write_request_archive(archive, manifest, (
                ("inputs/config.json", config), ("inputs/source.csv", source),
            ))
            service = worker.RemoteIKService(directory / "worker")

            def fake_run(
                request, package, execution, repository, progress, **_kwargs,
            ):
                output = execution / "2609110001"
                output.mkdir(parents=True)
                progress(1, 1, 0)
                for filename in (
                    "2609110001_primary.npz",
                    "2609110001_primary_config.json",
                    "2609110001_primary_target.npz",
                    "2609110001_primary_viewer.bin",
                ):
                    (output / filename).write_bytes(b"result")
                return IKExecutionResult(output, ("ok",))

            incoming = directory / "incoming.zip"
            incoming.write_bytes(archive.read_bytes())
            with patch.object(worker, "run_python_ik", side_effect=fake_run):
                submitted = service.submit(incoming, read_request_manifest(incoming))
                job_id = submitted["job_id"]
                deadline = time.monotonic() + 3
                status = submitted
                while status["status"] in {"queued", "running"} and time.monotonic() < deadline:
                    time.sleep(0.01)
                    status = service.status(job_id)
                self.assertEqual("completed", status["status"])
                self.assertEqual(1.0, status["progress"])
                with zipfile.ZipFile(service.result_path(job_id)) as result_archive:
                    self.assertEqual(
                        b"result", result_archive.read("2609110001_primary.npz")
                    )
                    self.assertIn(RESULT_MANIFEST_NAME, result_archive.namelist())
                job_directory = service.jobs_root / job_id
                self.assertFalse((job_directory / "request.zip").exists())
                self.assertFalse((job_directory / "package").exists())
                self.assertFalse((job_directory / "execution").exists())

    def test_worker_restores_interrupted_job_as_failed(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name) / "worker"
            job_id = "a" * 32
            job_dir = root / "jobs" / job_id
            job_dir.mkdir(parents=True)
            (job_dir / "status.json").write_text(json.dumps({
                "job_id": job_id,
                "status": "running",
                "submitted_at": "2026-09-13T00:00:00+00:00",
                "finished_at": None,
                "result_available": False,
            }), encoding="utf-8")
            service = worker.RemoteIKService(root)
            restored = service.status(job_id)
            self.assertEqual("failed", restored["status"])
            self.assertEqual("worker_restarted", restored["error"]["code"])

    def test_worker_can_cancel_a_queued_job(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            service = worker.RemoteIKService(Path(name) / "worker")
            job_id = "b" * 32
            job_dir = service.jobs_root / job_id
            job_dir.mkdir()
            with service.lock:
                service.jobs[job_id] = {
                    "job_id": job_id, "status": "queued", "finished_at": None,
                }
                service.cancel_events[job_id] = threading.Event()
                service._persist(job_id)
            cancelled = service.cancel(job_id)
            self.assertEqual("cancelled", cancelled["status"])
            self.assertTrue(service.cancel_events[job_id].is_set())


if __name__ == "__main__":
    unittest.main()
