from __future__ import annotations

import hashlib
import json
import re
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, BinaryIO, Iterable

from server.content_hash import (
    CANONICAL_JSON_SHA256,
    CANONICAL_TEXT_SHA256,
    MUJOCO_ASSET_BUNDLE_SHA256,
    canonical_text_sha256,
    repository_asset_sha256,
    sha256_file,
)


CONTRACT_VERSION = "1.2"
SUPPORTED_CONTRACT_VERSIONS = {"1.0", "1.1", CONTRACT_VERSION}
MANIFEST_NAME = "request.json"
RESULT_MANIFEST_NAME = "result.json"
RESULT_FORMAT = "meva_ik_result_zip_v2"
MANIFEST_JSON_HASH = CANONICAL_JSON_SHA256
MODEL_TEXT_HASH = CANONICAL_TEXT_SHA256
ASSET_BUNDLE_HASH = MUJOCO_ASSET_BUNDLE_SHA256
SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$")
ALLOWED_STAGES = {"primary", "main"}
ALLOWED_BACKENDS = {"remote_python", "remote_native", "local_native"}


class IKContractError(ValueError):
    pass


@dataclass(frozen=True)
class IKRequest:
    schema_version: str
    backend: str
    stage: str
    client_job_id: str
    robot: dict[str, str]
    config_path: str
    files: tuple[dict[str, Any], ...]
    iteration_diagnostics: bool = False

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "IKRequest":
        schema_version = str(raw.get("schema_version") or "")
        if schema_version not in SUPPORTED_CONTRACT_VERSIONS:
            raise IKContractError("Unsupported IK contract schema_version")
        backend = str(raw.get("backend") or "")
        stage = str(raw.get("stage") or "")
        client_job_id = str(raw.get("client_job_id") or "")
        if backend not in ALLOWED_BACKENDS:
            raise IKContractError(f"Unsupported backend: {backend}")
        if stage not in ALLOWED_STAGES:
            raise IKContractError(f"Unsupported stage: {stage}")
        if not SAFE_ID_RE.fullmatch(client_job_id):
            raise IKContractError("Invalid client_job_id")
        robot = raw.get("robot")
        if not isinstance(robot, dict):
            raise IKContractError("robot identity is required")
        normalized_robot = {
            "manufacturer": str(robot.get("manufacturer") or ""),
            "robot_id": str(robot.get("robot_id") or ""),
            "variant": str(robot.get("variant") or ""),
        }
        if not all(SAFE_ID_RE.fullmatch(value) for value in normalized_robot.values()):
            raise IKContractError("Invalid robot identity")
        for key in ("manifest_sha256", "model_sha256", "asset_bundle_sha256"):
            digest = str(robot.get(key) or "").lower()
            if not re.fullmatch(r"[0-9a-f]{64}", digest):
                raise IKContractError(f"Invalid robot {key}")
            normalized_robot[key] = digest
        for key, expected in (
            ("model_hash_algorithm", MODEL_TEXT_HASH),
            ("asset_bundle_hash_algorithm", ASSET_BUNDLE_HASH),
        ):
            algorithm = str(robot.get(key) or "")
            if schema_version == CONTRACT_VERSION and algorithm != expected:
                raise IKContractError(f"Unsupported robot {key}")
            if algorithm:
                normalized_robot[key] = algorithm
        offset_policy = str(robot.get("offset_policy") or "missing")
        if offset_policy not in {"approved", "none", "missing"}:
            raise IKContractError("Invalid robot offset_policy")
        normalized_robot["offset_policy"] = offset_policy
        if offset_policy == "approved":
            for key in ("offset_asset_sha256", "offset_fingerprint_sha256"):
                digest = str(robot.get(key) or "").lower()
                if not re.fullmatch(r"[0-9a-f]{64}", digest):
                    raise IKContractError(f"Invalid robot {key}")
                normalized_robot[key] = digest
            algorithm = str(robot.get("offset_algorithm") or "")
            if not SAFE_ID_RE.fullmatch(algorithm):
                raise IKContractError("Invalid robot offset_algorithm")
            normalized_robot["offset_algorithm"] = algorithm
            asset_hash_algorithm = str(robot.get("offset_asset_hash_algorithm") or "")
            if schema_version == CONTRACT_VERSION and asset_hash_algorithm != MANIFEST_JSON_HASH:
                raise IKContractError("Unsupported robot offset_asset_hash_algorithm")
            if asset_hash_algorithm:
                normalized_robot["offset_asset_hash_algorithm"] = asset_hash_algorithm
        manifest_json_sha256 = str(robot.get("manifest_json_sha256") or "").lower()
        if manifest_json_sha256:
            if not re.fullmatch(r"[0-9a-f]{64}", manifest_json_sha256):
                raise IKContractError("Invalid robot manifest_json_sha256")
            if robot.get("manifest_hash_algorithm") != MANIFEST_JSON_HASH:
                raise IKContractError("Unsupported robot manifest_hash_algorithm")
            normalized_robot["manifest_json_sha256"] = manifest_json_sha256
            normalized_robot["manifest_hash_algorithm"] = MANIFEST_JSON_HASH
        config_path = _safe_archive_path(str(raw.get("config_path") or ""))
        raw_files = raw.get("files")
        if not isinstance(raw_files, list) or not raw_files:
            raise IKContractError("files must be a non-empty array")
        files: list[dict[str, Any]] = []
        seen_roles: set[str] = set()
        seen_paths: set[str] = set()
        for item in raw_files:
            if not isinstance(item, dict):
                raise IKContractError("Invalid file descriptor")
            role = str(item.get("role") or "")
            path = _safe_archive_path(str(item.get("path") or ""))
            digest = str(item.get("sha256") or "").lower()
            size = item.get("size")
            if not SAFE_ID_RE.fullmatch(role) or role in seen_roles:
                raise IKContractError(f"Invalid or duplicate file role: {role}")
            if path in seen_paths or not re.fullmatch(r"[0-9a-f]{64}", digest):
                raise IKContractError(f"Invalid file descriptor: {role}")
            if not isinstance(size, int) or isinstance(size, bool) or size < 0:
                raise IKContractError(f"Invalid file size: {role}")
            files.append({"role": role, "path": path, "sha256": digest, "size": size})
            seen_roles.add(role)
            seen_paths.add(path)
        if config_path not in seen_paths:
            raise IKContractError("config_path is not declared in files")
        required = {"config", "source"} if stage == "primary" else {
            "config", "primary_motion", "primary_target"
        }
        missing = required - seen_roles
        if missing:
            raise IKContractError(f"Missing required file roles: {', '.join(sorted(missing))}")
        return cls(
            schema_version=schema_version,
            backend=backend,
            stage=stage,
            client_job_id=client_job_id,
            robot=normalized_robot,
            config_path=config_path,
            files=tuple(files),
            iteration_diagnostics=bool(raw.get("iteration_diagnostics", False)),
        )

    def file_for_role(self, role: str) -> dict[str, Any]:
        return next(item for item in self.files if item["role"] == role)


def _safe_archive_path(value: str) -> str:
    path = PurePosixPath(value.replace("\\", "/"))
    if (
        not value or "\x00" in value or ":" in value or path.is_absolute()
        or ".." in path.parts or path.parts[0] in {"", "."}
    ):
        raise IKContractError(f"Unsafe package path: {value!r}")
    return path.as_posix()


def canonical_json_sha256(path: Path) -> str:
    """Hash JSON values rather than formatting or checkout line endings."""
    try:
        value = json.loads(
            path.read_text(encoding="utf-8-sig"),
            parse_constant=lambda token: (_ for _ in ()).throw(
                ValueError(f"non-standard JSON constant: {token}")
            ),
        )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise IKContractError(f"Could not canonicalize JSON manifest: {exc}") from exc
    canonical = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def canonical_value_sha256(value: Any) -> str:
    canonical = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def robot_manifest_matches(path: Path, identity: dict[str, str]) -> bool:
    """Compare a robot manifest using the newest hash understood by both peers."""
    semantic_digest = identity.get("manifest_json_sha256")
    if semantic_digest:
        return canonical_json_sha256(path) == semantic_digest
    return sha256_file(path) == identity.get("manifest_sha256")


def mujoco_asset_fingerprint(
    model_path: Path,
    asset_root: Path,
    *,
    canonicalize_text: bool = True,
) -> str:
    """Hash the selected MJCF and files it names without packaging those assets."""
    root = asset_root.resolve()
    pending = [model_path.resolve()]
    files: set[Path] = set()
    while pending:
        xml_path = pending.pop()
        if xml_path in files:
            continue
        try:
            xml_root = ET.parse(xml_path).getroot()
        except (OSError, ET.ParseError) as exc:
            raise IKContractError(f"Could not inspect MuJoCo XML assets: {exc}") from exc
        files.add(xml_path)
        compiler = xml_root.find("compiler")
        asset_dir = compiler.get("assetdir", "") if compiler is not None else ""
        mesh_dir = compiler.get("meshdir", "") if compiler is not None else ""
        texture_dir = compiler.get("texturedir", "") if compiler is not None else ""
        for include in xml_root.iter("include"):
            if include.get("file"):
                pending.append((xml_path.parent / include.get("file")).resolve())
        for element in xml_root.iter():
            value = element.get("file")
            if not value or element.tag == "include":
                continue
            subdir = mesh_dir if element.tag in {"mesh", "skin"} else (
                texture_dir if element.tag in {"texture", "hfield"} else ""
            )
            files.add((xml_path.parent / asset_dir / subdir / value).resolve())
    digest = hashlib.sha256()
    for path in sorted(files, key=lambda item: item.as_posix().lower()):
        try:
            relative = path.relative_to(root).as_posix()
        except ValueError as exc:
            raise IKContractError(f"MuJoCo asset escapes robot directory: {path}") from exc
        if not path.is_file():
            raise IKContractError(f"MuJoCo asset is missing: {relative}")
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        content_digest = (
            repository_asset_sha256(path) if canonicalize_text else sha256_file(path)
        )
        digest.update(bytes.fromhex(content_digest))
    return digest.hexdigest()


def file_descriptor(role: str, archive_path: str, source: Path) -> dict[str, Any]:
    return {
        "role": role,
        "path": _safe_archive_path(archive_path),
        "size": source.stat().st_size,
        "sha256": sha256_file(source),
    }


def write_request_archive(
    destination: Path,
    manifest: dict[str, Any],
    files: Iterable[tuple[str, Path]],
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(MANIFEST_NAME, json.dumps(manifest, ensure_ascii=False, indent=2))
        for archive_path, source in files:
            archive.write(source, _safe_archive_path(archive_path))


def read_request_manifest(archive_path: Path) -> IKRequest:
    try:
        with zipfile.ZipFile(archive_path) as archive:
            info = archive.getinfo(MANIFEST_NAME)
            if info.file_size > 1024 * 1024:
                raise IKContractError("IK request manifest exceeds 1 MiB")
            raw = json.loads(archive.read(MANIFEST_NAME).decode("utf-8"))
    except (KeyError, OSError, zipfile.BadZipFile, json.JSONDecodeError) as exc:
        raise IKContractError(f"Invalid IK request archive: {exc}") from exc
    if not isinstance(raw, dict):
        raise IKContractError("IK request manifest must be an object")
    return IKRequest.from_dict(raw)


def extract_request_archive(
    archive_path: Path,
    destination: Path,
    request: IKRequest,
    *,
    max_uncompressed_bytes: int,
) -> None:
    declared = {item["path"]: item for item in request.files}
    total = 0
    destination.mkdir(parents=True, exist_ok=False)
    try:
        with zipfile.ZipFile(archive_path) as archive:
            file_infos = [info for info in archive.infolist() if not info.is_dir()]
            members = {info.filename: info for info in file_infos}
            if len(members) != len(file_infos):
                raise IKContractError("Package contains duplicate file names")
            allowed = set(declared) | {MANIFEST_NAME}
            extras = set(members) - allowed
            missing = set(declared) - set(members)
            if extras or missing:
                raise IKContractError(
                    f"Package file set mismatch; missing={sorted(missing)}, extra={sorted(extras)}"
                )
            for name, descriptor in declared.items():
                info = members[name]
                total += info.file_size
                if info.file_size != descriptor["size"] or total > max_uncompressed_bytes:
                    raise IKContractError(f"Invalid or oversized package file: {name}")
                target = destination.joinpath(*PurePosixPath(name).parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                digest = hashlib.sha256()
                with archive.open(info) as source, target.open("wb") as output:
                    for chunk in iter(lambda: source.read(1024 * 1024), b""):
                        digest.update(chunk)
                        output.write(chunk)
                if digest.hexdigest() != descriptor["sha256"]:
                    raise IKContractError(f"Checksum mismatch: {name}")
    except Exception:
        # The caller owns cleanup; retaining no partially verified input is safer.
        import shutil
        shutil.rmtree(destination, ignore_errors=True)
        raise


def stream_to_file(stream: BinaryIO, destination: Path, *, max_bytes: int) -> int:
    size = 0
    with destination.open("wb") as output:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            size += len(chunk)
            if size > max_bytes:
                raise IKContractError("IK request archive exceeds the configured size limit")
            output.write(chunk)
    return size


def _result_artifact_id(stage: str, names: list[str]) -> str:
    suffix = "_primary_config.json" if stage == "primary" else "_main_config.json"
    candidates = [name[:-len(suffix)] for name in names if name.endswith(suffix)]
    pattern = re.compile(r"^\d{10}$") if stage == "primary" else re.compile(r"^\d{10}-\d{2}$")
    if len(candidates) != 1 or not pattern.fullmatch(candidates[0]):
        raise IKContractError(f"Remote {stage} result must contain one valid config snapshot")
    return candidates[0]


def _required_result_names(stage: str, artifact_id: str) -> set[str]:
    if stage == "primary":
        return {
            f"{artifact_id}_primary.npz",
            f"{artifact_id}_primary_config.json",
            f"{artifact_id}_primary_target.npz",
            f"{artifact_id}_primary_viewer.bin",
        }
    return {
        f"{artifact_id}_main.npz",
        f"{artifact_id}_main_config.json",
        f"{artifact_id}_main_target.npz",
        f"{artifact_id}_main.pkl",
        f"{artifact_id}_main_viewer.bin",
    }


def _allowed_result_names(stage: str, artifact_id: str) -> set[str]:
    validation_prefix = f"{artifact_id}_{stage}_validation"
    validation = {
        f"{validation_prefix}.json",
        f"{validation_prefix}_joint_limit_severity.csv",
        f"{validation_prefix}_joint_limit_actual_rad.csv",
        f"{validation_prefix}_joint_limit_margin_rad.csv",
        f"{validation_prefix}_self_collision_severity.csv",
        f"{validation_prefix}_self_collision_signed_distance_m.csv",
        f"{validation_prefix}_foot_geom_z_m.csv",
    }
    common = _required_result_names(stage, artifact_id) | validation | {
        f"{artifact_id}_error.log",
    }
    if stage == "primary":
        return common | {
            "diagnostics.csv",
            "orientation_residuals.csv",
            "iteration_orientation_residual_summary.csv",
            "iteration_joint_delta_summary.csv",
            "iteration_joint_delta_by_frame.csv",
            "iteration_acceleration_soft_limit.csv",
            "analytic_joint_targets.csv",
            f"{artifact_id}_primary_post.csv",
        }
    if stage == "main":
        return common | {
            f"{artifact_id}_main_diagnostics.csv",
            f"{artifact_id}_main_targets.csv",
        }
    raise IKContractError(f"Invalid Remote result stage: {stage}")


def _validate_result_file_names(
    stage: str, status: str, artifact_id: str, names: set[str],
) -> None:
    allowed = _allowed_result_names(stage, artifact_id)
    for name in names:
        safe = _safe_archive_path(name)
        path = PurePosixPath(safe)
        if len(path.parts) != 1:
            raise IKContractError("Remote result files must use a flat layout")
        if name not in allowed:
            raise IKContractError(f"Unexpected Remote result file: {name}")
    if status == "completed":
        missing = _required_result_names(stage, artifact_id) - names
        if missing:
            raise IKContractError(
                f"Remote {stage} result is incomplete: {', '.join(sorted(missing))}"
            )


def write_result_archive(
    source: Path,
    destination: Path,
    request: IKRequest,
    *,
    status: str,
) -> list[str]:
    if status not in {"completed", "failed"}:
        raise IKContractError(f"Invalid Remote result status: {status}")
    paths = sorted(path for path in source.rglob("*") if path.is_file())
    if not paths or len(paths) > 64:
        raise IKContractError("Remote result has an invalid number of files")
    names = [path.relative_to(source).as_posix() for path in paths]
    artifact_id = _result_artifact_id(request.stage, names)
    _validate_result_file_names(request.stage, status, artifact_id, set(names))
    descriptors = [
        {
            "path": name,
            "size": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for name, path in zip(names, paths, strict=True)
    ]
    manifest = {
        "schema_version": CONTRACT_VERSION,
        "format": RESULT_FORMAT,
        "stage": request.stage,
        "status": status,
        "client_job_id": request.client_job_id,
        "artifact_id": artifact_id,
        "files": descriptors,
    }
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            RESULT_MANIFEST_NAME,
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        )
        for name, path in zip(names, paths, strict=True):
            archive.write(path, name)
    return names


def extract_result_archive(
    archive_path: Path,
    destination: Path,
    *,
    expected_stage: str,
    expected_client_job_id: str,
    expected_artifact_id: str,
    max_uncompressed_bytes: int,
    expected_status: str | None = None,
    skip_pickle: bool = True,
) -> list[str]:
    if destination.exists():
        raise IKContractError(f"Result staging path already exists: {destination}")
    destination.mkdir(parents=True, exist_ok=False)
    try:
        with zipfile.ZipFile(archive_path) as archive:
            infos = [info for info in archive.infolist() if not info.is_dir()]
            members = {info.filename: info for info in infos}
            if len(members) != len(infos):
                raise IKContractError("Remote result contains duplicate file names")
            try:
                manifest_info = members[RESULT_MANIFEST_NAME]
            except KeyError as exc:
                raise IKContractError("Remote result manifest is missing") from exc
            if manifest_info.file_size > 1024 * 1024:
                raise IKContractError("Remote result manifest exceeds 1 MiB")
            try:
                manifest = json.loads(archive.read(manifest_info).decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise IKContractError("Remote result manifest is invalid JSON") from exc
            if not isinstance(manifest, dict):
                raise IKContractError("Remote result manifest must be an object")
            if (
                manifest.get("schema_version") != CONTRACT_VERSION
                or manifest.get("format") != RESULT_FORMAT
                or manifest.get("stage") != expected_stage
                or manifest.get("client_job_id") != expected_client_job_id
                or manifest.get("artifact_id") != expected_artifact_id
            ):
                raise IKContractError("Remote result identity does not match the submitted job")
            status = str(manifest.get("status") or "")
            if status not in {"completed", "failed"}:
                raise IKContractError("Remote result has an invalid status")
            if expected_status is not None and status != expected_status:
                raise IKContractError("Remote result status does not match the Remote job")
            raw_files = manifest.get("files")
            if not isinstance(raw_files, list) or not raw_files or len(raw_files) > 64:
                raise IKContractError("Remote result has an invalid file list")
            declared: dict[str, dict[str, Any]] = {}
            for item in raw_files:
                if not isinstance(item, dict):
                    raise IKContractError("Remote result has an invalid file descriptor")
                name = _safe_archive_path(str(item.get("path") or ""))
                size = item.get("size")
                digest = str(item.get("sha256") or "").lower()
                if (
                    name in declared
                    or not isinstance(size, int)
                    or isinstance(size, bool)
                    or size < 0
                    or not re.fullmatch(r"[0-9a-f]{64}", digest)
                ):
                    raise IKContractError(f"Invalid Remote result descriptor: {name}")
                declared[name] = {"size": size, "sha256": digest}
            _validate_result_file_names(
                expected_stage, status, expected_artifact_id, set(declared),
            )
            actual_names = set(members) - {RESULT_MANIFEST_NAME}
            if actual_names != set(declared):
                raise IKContractError("Remote result file set does not match its manifest")
            total = 0
            for name, descriptor in declared.items():
                info = members[name]
                total += info.file_size
                if info.file_size != descriptor["size"] or total > max_uncompressed_bytes:
                    raise IKContractError(f"Invalid or oversized Remote result file: {name}")
                digest = hashlib.sha256()
                target = destination.joinpath(*PurePosixPath(name).parts)
                output = None if skip_pickle and target.suffix.lower() == ".pkl" else target.open("wb")
                try:
                    with archive.open(info) as source:
                        for chunk in iter(lambda: source.read(1024 * 1024), b""):
                            digest.update(chunk)
                            if output is not None:
                                output.write(chunk)
                finally:
                    if output is not None:
                        output.close()
                if digest.hexdigest() != descriptor["sha256"]:
                    raise IKContractError(f"Remote result checksum mismatch: {name}")
            return sorted(declared)
    except (zipfile.BadZipFile, OSError) as exc:
        import shutil
        shutil.rmtree(destination, ignore_errors=True)
        raise IKContractError(f"Could not read Remote result archive: {exc}") from exc
    except Exception:
        import shutil
        shutil.rmtree(destination, ignore_errors=True)
        raise
