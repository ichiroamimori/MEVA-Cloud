from __future__ import annotations

import xml.etree.ElementTree as ET
from functools import lru_cache
from pathlib import Path, PurePosixPath
from urllib.parse import urlencode

from server.robot_registry import RobotRegistryError, RobotVariant


class RobotBrowserViewerError(ValueError):
    pass


def _safe_relative(root: Path, path: Path, label: str) -> str:
    root = root.resolve()
    path = path.resolve()
    try:
        relative = path.relative_to(root)
    except ValueError as exc:
        raise RobotBrowserViewerError(f"Unsafe {label}: {path}") from exc
    if not path.is_file():
        raise RobotBrowserViewerError(f"Missing Robot asset: {relative.as_posix()}")
    return relative.as_posix()


def _asset_path(root: Path, relative: PurePosixPath, label: str) -> tuple[Path, str]:
    if relative.is_absolute() or ".." in relative.parts:
        raise RobotBrowserViewerError(f"Unsafe {label}: {relative}")
    path = root.joinpath(*relative.parts)
    return path, _safe_relative(root, path, label)


@lru_cache(maxsize=32)
def _collect_cached(root_string: str, model_relative: str, model_mtime_ns: int) -> tuple[str, ...]:
    del model_mtime_ns  # Part of the key so an edited root MJCF invalidates the cache.
    root = Path(root_string)
    model_relative_path = PurePosixPath(model_relative)
    pending = [model_relative_path]
    visited_xml: set[str] = set()
    assets: set[str] = set()
    compiler_dirs = {"asset": PurePosixPath(), "mesh": PurePosixPath(), "texture": PurePosixPath()}

    while pending:
        xml_relative = pending.pop()
        xml_path, xml_key = _asset_path(root, xml_relative, "MJCF XML")
        if xml_key in visited_xml:
            continue
        visited_xml.add(xml_key)
        assets.add(xml_key)
        try:
            document = ET.parse(xml_path)
        except (OSError, ET.ParseError) as exc:
            raise RobotBrowserViewerError(f"Could not read MJCF XML {xml_key}: {exc}") from exc

        compiler = document.find("compiler")
        if compiler is not None:
            asset_dir = PurePosixPath(compiler.get("assetdir", "").replace("\\", "/"))
            compiler_dirs["asset"] = asset_dir
            compiler_dirs["mesh"] = asset_dir / PurePosixPath(
                compiler.get("meshdir", "").replace("\\", "/")
            )
            compiler_dirs["texture"] = asset_dir / PurePosixPath(
                compiler.get("texturedir", "").replace("\\", "/")
            )

        for element in document.iter():
            raw_file = element.get("file")
            if not raw_file:
                continue
            file_relative = PurePosixPath(raw_file.replace("\\", "/"))
            if element.tag == "include":
                include_relative = xml_relative.parent / file_relative
                _, include_key = _asset_path(root, include_relative, "included MJCF XML")
                pending.append(PurePosixPath(include_key))
                continue
            directory = compiler_dirs.get(
                "mesh" if element.tag == "mesh" else "texture" if element.tag == "texture" else "asset"
            )
            asset_path, asset_key = _asset_path(root, directory / file_relative, "Robot asset")
            del asset_path
            assets.add(asset_key)

    return tuple(sorted(assets))


def browser_viewer_asset_paths(record: RobotVariant) -> tuple[str, ...]:
    root = record.robot_directory.resolve()
    try:
        model_relative = record.model_path.resolve().relative_to(root).as_posix()
    except (ValueError, RobotRegistryError) as exc:
        raise RobotBrowserViewerError("Robot model is outside its registered directory") from exc
    return _collect_cached(str(root), model_relative, record.model_path.stat().st_mtime_ns)


def browser_viewer_config(record: RobotVariant, *, motion_query: dict[str, str] | None = None) -> dict:
    paths = browser_viewer_asset_paths(record)
    identity = {
        "manufacturer": record.manufacturer_id,
        "robot_id": record.robot_id,
        "robot_variant": record.variant_id,
    }
    common_query = {
        "manufacturer": record.manufacturer_id,
        "robot_id": record.robot_id,
        "robot_variant": record.variant_id,
    }
    files = []
    for relative in paths:
        query = urlencode({**common_query, "path": relative})
        path = record.robot_directory / Path(relative)
        files.append({
            "path": relative,
            "url": f"/api/retarget/robots/viewer/browser/asset?{query}",
            "size": path.stat().st_size,
        })
    model_relative = record.model_path.resolve().relative_to(record.robot_directory.resolve()).as_posix()
    motion_url = None
    if motion_query:
        motion_url = "/api/retarget/viewer/file/retarget?" + urlencode(motion_query)
    standing_pose = record.variant.get("standing_pose")
    poses = record.variant.get("poses")
    if standing_pose is None and isinstance(poses, dict):
        standing_pose = poses.get("standing")
    return {
        "schema_version": "1.0",
        "robot": {
            **identity,
            "manufacturer_name": record.manufacturer_name,
            "robot_name": record.robot_name,
            "variant_name": str(record.variant["name"]),
        },
        "model_path": model_relative,
        "files": files,
        "initial_pose": record.variant.get("initial_pose", {"type": "model_default"}),
        "standing_pose": standing_pose,
        "motion_url": motion_url,
    }


def resolve_browser_asset(record: RobotVariant, relative: str) -> Path:
    normalized = PurePosixPath(relative.replace("\\", "/"))
    _, key = _asset_path(record.robot_directory, normalized, "Robot asset")
    if key not in set(browser_viewer_asset_paths(record)):
        raise RobotBrowserViewerError(f"Asset is not referenced by the selected MJCF: {key}")
    return record.robot_directory.joinpath(*PurePosixPath(key).parts)
