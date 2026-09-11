from __future__ import annotations

import json
import tempfile
import time
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from server.ik_contract import (
    IKContractError,
    extract_request_archive,
    file_descriptor,
    read_request_manifest,
    write_request_archive,
)
from server.remote_ik_client import build_request_archive, extract_result_archive
from server.ik_execution import IKExecutionResult
import server.remote_ik_worker as worker
from fastapi import HTTPException


class RemoteIKContractTest(unittest.TestCase):
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
            source = directory / "motion.csv"
            source.write_text("frame,value\n0,1\n", encoding="utf-8")
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
            self.assertEqual("inputs/source.csv", manifest["files"][1]["path"])
            self.assertNotIn(str(root), json.dumps(manifest))
            request = read_request_manifest(archive)
            extracted = directory / "extracted"
            extract_request_archive(archive, extracted, request, max_uncompressed_bytes=1024 * 1024)
            self.assertEqual(source.read_bytes(), (extracted / "inputs/source.csv").read_bytes())
            packaged_config = json.loads((extracted / "inputs/config.json").read_text(encoding="utf-8"))
            self.assertEqual("package://source", packaged_config["source"]["file"])

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
            with zipfile.ZipFile(archive, "w") as output:
                output.writestr("../escape.txt", "bad")
            with self.assertRaisesRegex(Exception, "unsafe path"):
                extract_result_archive(archive, directory / "out")
            self.assertFalse((directory / "escape.txt").exists())

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

            def fake_run(request, package, execution, repository, progress):
                output = execution / "2609110001"
                output.mkdir(parents=True)
                progress(1, 1, 0)
                (output / "result.npz").write_bytes(b"result")
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
                    self.assertEqual(b"result", result_archive.read("result.npz"))


if __name__ == "__main__":
    unittest.main()
