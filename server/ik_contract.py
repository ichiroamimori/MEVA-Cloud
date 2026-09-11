from __future__ import annotations

import hashlib
import json
import re
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, BinaryIO, Iterable


CONTRACT_VERSION = "1.0"
MANIFEST_NAME = "request.json"
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
        if raw.get("schema_version") != CONTRACT_VERSION:
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
            schema_version=CONTRACT_VERSION,
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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def mujoco_asset_fingerprint(model_path: Path, asset_root: Path) -> str:
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
        digest.update(bytes.fromhex(sha256_file(path)))
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
