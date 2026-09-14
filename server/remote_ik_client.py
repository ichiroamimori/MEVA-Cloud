from __future__ import annotations

import http.client
import json
import os
import ssl
import tempfile
import threading
import time
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlsplit

from server.ik_contract import (
    CONTRACT_VERSION,
    ASSET_BUNDLE_HASH,
    IKContractError,
    MANIFEST_JSON_HASH,
    MODEL_TEXT_HASH,
    canonical_json_sha256,
    canonical_text_sha256,
    canonical_value_sha256,
    extract_result_archive as extract_verified_result_archive,
    file_descriptor,
    mujoco_asset_fingerprint,
    sha256_file,
    write_request_archive,
    RESULT_FORMAT,
)
from server.robot_registry import resolve_variant


class RemoteIKError(RuntimeError):
    def __init__(self, code: str, message: str, *, remote_job_id: str | None = None):
        super().__init__(message)
        self.code = code
        self.remote_job_id = remote_job_id


def configured_backend(requested: str | None = None) -> str:
    backend = (
        requested
        if requested is not None
        else os.environ.get("MEVA_IK_BACKEND", "local_python")
    ).strip().lower()
    if backend not in {"local_python", "remote_python"}:
        raise RuntimeError(
            f"Unsupported MEVA_IK_BACKEND={backend!r}; this release supports local_python and remote_python"
        )
    return backend


def _robot_identity(config: dict[str, Any], repository_root: Path) -> dict[str, str]:
    robot = config.get("robot")
    if not isinstance(robot, dict):
        raise RemoteIKError("config_error", "Config robot identity is missing")
    identity = {
        "manufacturer": str(robot.get("manufacturer") or ""),
        "robot_id": str(robot.get("model") or ""),
        "variant": str(robot.get("variant") or ""),
    }
    if not all(identity.values()):
        raise RemoteIKError("config_error", "Config robot identity is incomplete")
    try:
        record = resolve_variant(
            identity["variant"], manufacturer_id=identity["manufacturer"],
            robot_id=identity["robot_id"], root=repository_root,
        )
    except Exception as exc:
        raise RemoteIKError("robot_model_load_failure", str(exc)) from exc
    identity["manifest_sha256"] = sha256_file(record.manifest_path)
    identity["manifest_json_sha256"] = canonical_json_sha256(record.manifest_path)
    identity["manifest_hash_algorithm"] = MANIFEST_JSON_HASH
    identity["model_sha256"] = canonical_text_sha256(record.model_path)
    identity["model_hash_algorithm"] = MODEL_TEXT_HASH
    identity["asset_bundle_sha256"] = mujoco_asset_fingerprint(
        record.model_path, record.robot_directory,
    )
    identity["asset_bundle_hash_algorithm"] = ASSET_BUNDLE_HASH
    identity["offset_policy"] = record.meva_offset_policy
    if record.meva_offset_policy == "missing":
        raise RemoteIKError(
            "robot_model_load_failure",
            "Robot manifest does not declare a production MEVA Offset policy",
        )
    if record.meva_offset_policy == "approved":
        path = record.approved_meva_offset_path
        if path is None or not path.is_file():
            raise RemoteIKError(
                "robot_model_load_failure", "Approved MEVA Offset asset is missing"
            )
        try:
            asset = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RemoteIKError(
                "robot_model_load_failure", f"Invalid approved MEVA Offset asset: {exc}"
            ) from exc
        identity["offset_asset_sha256"] = canonical_json_sha256(path)
        identity["offset_asset_hash_algorithm"] = MANIFEST_JSON_HASH
        identity["offset_fingerprint_sha256"] = canonical_value_sha256(
            asset.get("fingerprint")
        )
        identity["offset_algorithm"] = str(asset.get("algorithm") or "")
    return identity


def build_request_archive(
    *,
    destination: Path,
    repository_root: Path,
    stage: str,
    client_job_id: str,
    config_path: Path,
    primary_directory: Path | None = None,
    iteration_diagnostics: bool = False,
) -> dict[str, Any]:
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RemoteIKError("config_error", f"Could not read IK config: {exc}") from exc
    if not isinstance(config, dict):
        raise RemoteIKError("config_error", "IK config must be an object")

    payload_sources: list[tuple[str, str, Path]] = []
    if stage == "primary":
        raw_source = str(config.get("source", {}).get("file") or "")
        source = (repository_root / raw_source).resolve()
        if not source.is_file():
            raise RemoteIKError("input_load_failure", f"MEVA input file not found: {raw_source}")
        if source.suffix.lower() != ".bin":
            raise RemoteIKError(
                "config_error", "Remote Primary requires the versioned MEVA BIN input",
            )
        payload_sources.append(("source", f"inputs/source{source.suffix.lower()}", source))
    elif stage == "main":
        if primary_directory is None:
            raise RemoteIKError("config_error", "Primary result directory is required for Main")
        run_id = str(config.get("primary_run_id") or "")
        motion = primary_directory / f"{run_id}_primary.npz"
        if not motion.is_file():
            motion = next((path for path in (
                primary_directory / f"{run_id}_primary.pkl",
                primary_directory / "primary.pkl",
            ) if path.is_file()), motion)
        target = primary_directory / f"{run_id}_primary_target.npz"
        if not motion.is_file():
            raise RemoteIKError("input_load_failure", f"Primary motion not found for {run_id}")
        if not target.is_file():
            raise RemoteIKError("input_load_failure", f"Primary target not found for {run_id}")
        payload_sources.extend((
            ("primary_motion", f"inputs/primary_motion{motion.suffix.lower()}", motion),
            ("primary_target", "inputs/primary_target.npz", target),
        ))
    else:
        raise RemoteIKError("invalid_request", f"Unsupported IK stage: {stage}")

    package_config = json.loads(json.dumps(config))
    if isinstance(package_config.get("source"), dict) and package_config["source"].get("file"):
        package_config["source"]["file"] = "package://source"
    packaged_config_path = destination.parent / f".{destination.stem}.package-config.json"
    packaged_config_path.write_text(
        json.dumps(package_config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    sources = [("config", "inputs/config.json", packaged_config_path), *payload_sources]
    try:
        descriptors = [
            file_descriptor(role, archive_path, source)
            for role, archive_path, source in sources
        ]
        manifest = {
            "schema_version": CONTRACT_VERSION,
            "backend": "remote_python",
            "stage": stage,
            "client_job_id": client_job_id,
            "robot": _robot_identity(config, repository_root),
            "config_path": "inputs/config.json",
            "iteration_diagnostics": bool(iteration_diagnostics),
            "files": descriptors,
            "result": {"format": RESULT_FORMAT},
        }
        write_request_archive(
            destination,
            manifest,
            ((archive_path, source) for _, archive_path, source in sources),
        )
        return manifest
    finally:
        packaged_config_path.unlink(missing_ok=True)


class RemoteIKClient:
    def __init__(self, base_url: str | None = None, token: str | None = None):
        self.base_url = (base_url or os.environ.get("MEVA_REMOTE_IK_URL", "")).rstrip("/")
        if not self.base_url:
            raise RemoteIKError("invalid_request", "MEVA_REMOTE_IK_URL is not configured")
        self.token = token if token is not None else os.environ.get("MEVA_REMOTE_IK_TOKEN", "")
        self.timeout = float(os.environ.get("MEVA_REMOTE_IK_HTTP_TIMEOUT_SEC", "60"))
        parsed = urlsplit(self.base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.query or parsed.fragment:
            raise RemoteIKError("invalid_request", "MEVA_REMOTE_IK_URL must be an HTTP(S) server URL")
        self.parsed = parsed

    def _connection(self) -> http.client.HTTPConnection:
        port = self.parsed.port or (443 if self.parsed.scheme == "https" else 80)
        if self.parsed.scheme == "https":
            return http.client.HTTPSConnection(
                self.parsed.hostname, port, timeout=self.timeout,
                context=ssl.create_default_context(),
            )
        return http.client.HTTPConnection(self.parsed.hostname, port, timeout=self.timeout)

    def _path(self, suffix: str) -> str:
        prefix = self.parsed.path.rstrip("/")
        return f"{prefix}{suffix}"

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def _json_response(self, connection: http.client.HTTPConnection) -> dict[str, Any]:
        response = connection.getresponse()
        body = response.read()
        if response.status >= 400:
            try:
                detail = json.loads(body.decode("utf-8")).get("detail", {})
                message = detail.get("message") if isinstance(detail, dict) else str(detail)
            except Exception:
                message = body.decode("utf-8", errors="replace")
            raise RemoteIKError("remote_http_error", f"Remote IK HTTP {response.status}: {message}")
        value = json.loads(body.decode("utf-8"))
        if not isinstance(value, dict):
            raise RemoteIKError("remote_protocol_error", "Remote IK returned invalid JSON")
        return value

    def submit(self, archive_path: Path) -> dict[str, Any]:
        connection = self._connection()
        try:
            connection.putrequest("POST", self._path("/api/v1/ik/jobs"))
            connection.putheader("Content-Type", "application/zip")
            connection.putheader("Content-Length", str(archive_path.stat().st_size))
            for name, value in self._headers().items():
                connection.putheader(name, value)
            connection.endheaders()
            with archive_path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    connection.send(chunk)
            return self._json_response(connection)
        except (OSError, http.client.HTTPException) as exc:
            raise RemoteIKError("input_upload_failure", f"Could not submit Remote IK job: {exc}") from exc
        finally:
            connection.close()

    def status(self, job_id: str) -> dict[str, Any]:
        connection = self._connection()
        try:
            connection.request(
                "GET", self._path(f"/api/v1/ik/jobs/{job_id}"), headers=self._headers(),
            )
            return self._json_response(connection)
        except (OSError, http.client.HTTPException) as exc:
            raise RemoteIKError("status_query_failure", f"Could not query Remote IK job: {exc}", remote_job_id=job_id) from exc
        finally:
            connection.close()

    def cancel(self, job_id: str) -> dict[str, Any]:
        connection = self._connection()
        try:
            connection.request(
                "POST",
                self._path(f"/api/v1/ik/jobs/{job_id}/cancel"),
                headers=self._headers(),
            )
            return self._json_response(connection)
        except (OSError, http.client.HTTPException) as exc:
            raise RemoteIKError(
                "cancel_failure",
                f"Could not cancel Remote IK job: {exc}",
                remote_job_id=job_id,
            ) from exc
        finally:
            connection.close()

    def download_result(self, job_id: str, destination: Path) -> None:
        connection = self._connection()
        try:
            connection.request(
                "GET", self._path(f"/api/v1/ik/jobs/{job_id}/result"), headers=self._headers(),
            )
            response = connection.getresponse()
            if response.status >= 400:
                body = response.read().decode("utf-8", errors="replace")
                raise RemoteIKError("result_download_failure", f"Remote result HTTP {response.status}: {body}")
            limit = int(os.environ.get("MEVA_IK_MAX_RESULT_ARCHIVE_BYTES", str(2 * 1024**3)))
            content_length = response.getheader("Content-Length")
            if content_length and int(content_length) > limit:
                raise RemoteIKError("result_download_failure", "Remote result archive is too large")
            size = 0
            with destination.open("wb") as output:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    size += len(chunk)
                    if size > limit:
                        raise RemoteIKError("result_download_failure", "Remote result archive is too large")
                    output.write(chunk)
        except (OSError, ValueError, http.client.HTTPException) as exc:
            raise RemoteIKError("result_download_failure", f"Could not download Remote IK result: {exc}") from exc
        finally:
            connection.close()


def extract_result_archive(
    archive_path: Path,
    destination: Path,
    *,
    stage: str,
    client_job_id: str,
    artifact_id: str,
    status: str | None = None,
) -> list[str]:
    try:
        return extract_verified_result_archive(
            archive_path,
            destination,
            expected_stage=stage,
            expected_client_job_id=client_job_id,
            expected_artifact_id=artifact_id,
            expected_status=status,
            max_uncompressed_bytes=int(
                os.environ.get("MEVA_IK_MAX_RESULT_UNCOMPRESSED_BYTES", str(4 * 1024**3))
            ),
        )
    except (IKContractError, ValueError) as exc:
        raise RemoteIKError("output_write_failure", str(exc)) from exc


def execute_remote_job(
    *,
    repository_root: Path,
    stage: str,
    client_job_id: str,
    config_path: Path,
    result_staging: Path,
    primary_directory: Path | None = None,
    iteration_diagnostics: bool = False,
    status_callback: Callable[[dict[str, Any]], None] | None = None,
    cancel_event: threading.Event | None = None,
) -> dict[str, Any]:
    if cancel_event is not None and cancel_event.is_set():
        raise RemoteIKError("cancelled", "Remote IK job was cancelled")
    try:
        local_config = json.loads(config_path.read_text(encoding="utf-8"))
        artifact_id = str(
            local_config.get("output", {}).get("run_id")
            if stage == "primary"
            else local_config.get("main_id")
        )
        if not artifact_id or artifact_id == "None":
            raise ValueError("Remote result artifact ID is missing")
    except (OSError, json.JSONDecodeError, AttributeError, TypeError, ValueError) as exc:
        raise RemoteIKError("config_error", f"Could not identify Remote result: {exc}") from exc
    transfer_root = repository_root / "workspace" / ".ik_transfer"
    transfer_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f"{client_job_id}-", dir=transfer_root) as temp_name:
        temp = Path(temp_name)
        request_archive = temp / "request.zip"
        build_request_archive(
            destination=request_archive,
            repository_root=repository_root,
            stage=stage,
            client_job_id=client_job_id,
            config_path=config_path,
            primary_directory=primary_directory,
            iteration_diagnostics=iteration_diagnostics,
        )
        client = RemoteIKClient()
        remote = client.submit(request_archive)
        remote_job_id = str(remote.get("job_id") or "")
        if not remote_job_id:
            raise RemoteIKError("remote_protocol_error", "Remote IK did not return job_id")
        if status_callback is not None:
            status_callback(remote)
        poll_seconds = max(0.2, float(os.environ.get("MEVA_REMOTE_IK_POLL_SEC", "2")))
        cancel_sent = False
        while remote.get("status") in {"queued", "running", "cancelling"}:
            if cancel_event is not None and cancel_event.is_set() and not cancel_sent:
                remote = client.cancel(remote_job_id)
                cancel_sent = True
            if status_callback is not None:
                status_callback(remote)
            if remote.get("status") not in {"queued", "running", "cancelling"}:
                break
            cancel_event.wait(poll_seconds) if cancel_event is not None else time.sleep(poll_seconds)
            remote = client.status(remote_job_id)
        if remote.get("result_available"):
            result_archive = temp / "result.zip"
            client.download_result(remote_job_id, result_archive)
            extract_result_archive(
                result_archive,
                result_staging,
                stage=stage,
                client_job_id=client_job_id,
                artifact_id=artifact_id,
                status=str(remote.get("status") or ""),
            )
        if status_callback is not None:
            status_callback(remote)
        if remote.get("status") != "completed":
            error = remote.get("error") if isinstance(remote.get("error"), dict) else {}
            raise RemoteIKError(
                str(error.get("code") or (
                    "cancelled" if remote.get("status") == "cancelled" else "ik_solver_failure"
                )),
                str(error.get("message") or (
                    "Remote IK job was cancelled"
                    if remote.get("status") == "cancelled" else "Remote IK failed"
                )),
                remote_job_id=remote_job_id,
            )
        return remote
