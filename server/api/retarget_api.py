from __future__ import annotations

import csv
import json
import math
import re
import shutil
import subprocess
import sys
import threading
import uuid
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Literal

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel, Field

from server.retarget_config_store import (
    ConfigNameCollision,
    ConfigStoreError,
    list_configs as list_shared_configs,
    load_config as load_shared_config,
    runtime_config as merge_runtime_config,
    save_user_config,
    workspace_root,
)
from server.robot_registry import (
    RobotRegistryError,
    RobotVariant,
    apply_variant_to_runtime_config,
    public_catalog,
    resolve_variant,
    validate_retarget_config,
    variant_retargeting_metadata,
)


router = APIRouter(prefix="/api/retarget", tags=["retarget"])

RUN_RE = re.compile(r"^\d{10}$")
CAPSULE_RE = re.compile(r"^\d{10}$")
MAIN_ID_RE = re.compile(r"^(\d{10})-(\d{2})$")
PROGRESS_RE = re.compile(r"^\[(\d+)/(\d+)\] frame (\d+)")
JOBS: dict[str, dict[str, Any]] = {}
JOBS_LOCK = threading.Lock()


def repo_root() -> Path:
    # server/api/retarget_api.py -> repo root
    return Path(__file__).resolve().parents[2]


def _registered_variant(
    robot_variant: str,
    *,
    manufacturer: str | None = None,
    robot_id: str | None = None,
) -> RobotVariant:
    try:
        return resolve_variant(
            robot_variant,
            manufacturer_id=manufacturer,
            robot_id=robot_id,
            root=repo_root(),
        )
    except RobotRegistryError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


def _runtime_robot_config(config: dict[str, Any], record: RobotVariant) -> dict[str, Any]:
    return apply_variant_to_runtime_config(config, record, root=repo_root())


def _assert_config_robot(config: dict[str, Any], record: RobotVariant) -> None:
    robot = config.get("robot")
    if not isinstance(robot, dict):
        raise HTTPException(status_code=400, detail="Config robot identity is required")
    actual = (
        str(robot.get("manufacturer") or ""),
        str(robot.get("model") or ""),
        str(robot.get("variant") or ""),
    )
    expected = (record.manufacturer_id, record.robot_id, record.variant_id)
    if actual != expected:
        raise HTTPException(
            status_code=400,
            detail=(
                "Config Robot identity mismatch: "
                f"expected {expected[0]}/{expected[1]}/{expected[2]}, "
                f"found {actual[0]}/{actual[1]}/{actual[2]}"
            ),
        )


def _validate_retarget_config_or_http(
    record: RobotVariant, config: dict[str, Any]
) -> dict[str, Any]:
    try:
        return validate_retarget_config(record, config)
    except RobotRegistryError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


def robot_dir(
    capsule_id: str,
    robot_variant: str,
    user_id: str = "local_user",
) -> Path:
    return (
        workspace_root()
        / "users"
        / user_id
        / "capsules"
        / capsule_id
        / "retarget"
        / robot_variant
    )


def default_config_path(
    capsule_id: str,
    robot_variant: str,
    user_id: str = "local_user",
) -> Path:
    return robot_dir(capsule_id, robot_variant, user_id) / "config.json"


def main_default_config_path(
    capsule_id: str,
    robot_variant: str,
    user_id: str = "local_user",
) -> Path:
    return robot_dir(capsule_id, robot_variant, user_id) / "main_config.json"


def main_run_config_path(
    capsule_id: str,
    robot_variant: str,
    run_id: str,
    user_id: str = "local_user",
) -> Path:
    return (
        robot_dir(capsule_id, robot_variant, user_id)
        / run_id
        / f"{run_id}_main_config.json"
    )


def _sole_geom_descriptors(config: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Expose the manifest-defined Foot support points to the existing UI."""
    robot = config.get("robot", {})
    contacts = robot.get("foot_contacts") if isinstance(robot, dict) else None
    if not isinstance(contacts, dict):
        contacts = None
    if contacts is None:
        try:
            variant = resolve_variant(
                str(robot.get("variant") or ""),
                manufacturer_id=str(robot.get("manufacturer") or "") or None,
                robot_id=str(robot.get("model") or "") or None,
                root=repo_root(),
            )
            value = variant_retargeting_metadata(variant).get("foot_contacts")
            contacts = value if isinstance(value, dict) else None
        except RobotRegistryError:
            contacts = None
    result: dict[str, list[dict[str, Any]]] = {"left": [], "right": []}
    if contacts is None:
        return result
    for side in ("left", "right"):
        definition = contacts.get(side)
        if not isinstance(definition, dict):
            continue
        points = definition.get("support_points")
        if not isinstance(points, list):
            continue
        for index, point in enumerate(points):
            if not isinstance(point, dict):
                continue
            position = point.get("local_position")
            if not isinstance(position, list) or len(position) != 3:
                continue
            name = str(point.get("name") or f"support_{index + 1}")
            result[side].append({
                "index": index,
                "name": name,
                "display": f"{side}_{name}",
                "pos": " ".join(f"{float(value):g}" for value in position),
                "size": "",
                "body": str(definition.get("body") or ""),
                "generation_method": str(
                    definition.get("generation_method") or "explicit"
                ),
            })
    return result


def _manifest_robot_foot_to_ground_offset(config: dict[str, Any]) -> float | None:
    """Read the installer-confirmed Robot Foot offset from manifest metadata."""
    robot = config.get("robot", {})
    contacts = robot.get("foot_contacts") if isinstance(robot, dict) else None
    if not isinstance(contacts, dict):
        try:
            variant = resolve_variant(
                str(robot.get("variant") or ""),
                manufacturer_id=str(robot.get("manufacturer") or "") or None,
                robot_id=str(robot.get("model") or "") or None,
                root=repo_root(),
            )
            value = variant_retargeting_metadata(variant).get("foot_contacts")
            contacts = value if isinstance(value, dict) else None
        except RobotRegistryError:
            contacts = None
    if not isinstance(contacts, dict):
        return None
    try:
        value = float(contacts["robot_foot_to_ground_offset_m"])
    except (KeyError, TypeError, ValueError):
        return None
    return value if math.isfinite(value) and value >= 0.0 else None


def main_results_dir(
    capsule_id: str,
    robot_variant: str,
    run_id: str,
    user_id: str = "local_user",
) -> Path:
    """Preferred directory containing new Main result directories."""
    return robot_dir(capsule_id, robot_variant, user_id) / run_id


def resolve_main_result_dir(
    capsule_id: str,
    robot_variant: str,
    run_id: str,
    main_id: str,
    user_id: str = "local_user",
    *,
    must_exist: bool = True,
) -> Path:
    run = main_results_dir(capsule_id, robot_variant, run_id, user_id)
    preferred = run / main_id
    legacy = run / "main" / main_id
    if preferred.is_dir():
        return preferred
    if legacy.is_dir():
        return legacy
    if must_exist:
        raise HTTPException(status_code=404, detail=f"Main result not found: {main_id}")
    return preferred


def list_main_result_ids(path: Path, run_id: str) -> list[str]:
    """List both new <Primary>/<Main ID> and legacy <Primary>/main/<Main ID>."""
    if not path.exists():
        return []
    prefix = f"{run_id}-"
    result: set[str] = set()
    for parent in (path, path / "main"):
        if not parent.is_dir():
            continue
        result.update(
            p.name for p in parent.iterdir()
            if p.is_dir() and MAIN_ID_RE.fullmatch(p.name) and p.name.startswith(prefix)
        )
    return sorted(result, reverse=True)


def allocate_main_id(path: Path, run_id: str) -> str:
    nums = [int(x.rsplit("-", 1)[1]) for x in list_main_result_ids(path, run_id)]
    number = max(nums) + 1 if nums else 1
    if number > 99:
        raise HTTPException(status_code=409, detail=f"Main ID range exhausted for {run_id}")
    return f"{run_id}-{number:02d}"


def main_result_json_path(
    capsule_id: str,
    robot_variant: str,
    run_id: str,
    main_id: str,
    user_id: str = "local_user",
) -> Path:
    return resolve_main_result_dir(
        capsule_id, robot_variant, run_id, main_id, user_id, must_exist=False
    ) / f"{main_id}_main_config.json"


def list_primary_run_ids(path: Path) -> list[str]:
    out: list[str] = []
    for run_id in list_run_ids(path):
        run = path / run_id
        if (
            (run / f"{run_id}_primary.npz").exists()
            or (run / f"{run_id}_primary.pkl").exists()
            or (run / "primary.pkl").exists()
            or (run / f"{run_id}_primary_viewer.bin").exists()
        ):
            out.append(run_id)
    return out


def atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    tmp.replace(path)


def list_run_ids(path: Path) -> list[str]:
    if not path.exists():
        return []
    out = [
        p.name
        for p in path.iterdir()
        if p.is_dir() and RUN_RE.fullmatch(p.name)
    ]
    return sorted(out, reverse=True)


def allocate_run_id(path: Path) -> str:
    prefix = datetime.now().strftime("%y%m%d")
    nums: list[int] = []
    if path.exists():
        for p in path.iterdir():
            if not p.is_dir():
                continue
            m = re.fullmatch(prefix + r"(\d{4})", p.name)
            if m:
                nums.append(int(m.group(1)))
    # Preserve the convention already used by primary_retarget.py.
    n = max(nums) + 1 if nums else 1
    return f"{prefix}{n:04d}"



def count_source_frames(cfg: dict[str, Any]) -> int | None:
    try:
        source = cfg["source"]
        rel = source["file"]
        path = (repo_root() / rel).resolve()
        header_row = int(source.get("header_row_1based", 1))
        if not path.exists():
            return None
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            for _ in range(max(0, header_row - 1)):
                next(reader, None)
            next(reader, None)  # header itself
            return sum(1 for _ in reader)
    except Exception:
        return None


def metadata_frame_count(
    capsule_id: str,
    user_id: str = "local_user",
) -> int | None:
    """Read the source frame count without scanning a large MEVA CSV."""
    path = (
        workspace_root() / "users" / user_id
        / "capsules" / capsule_id / "metadata.json"
    )
    if not path.exists():
        return None
    try:
        metadata = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    source = metadata.get("meva_source") or {}
    try:
        frame_count = int(source["frame_count"])
        if frame_count >= 0:
            return frame_count
    except (KeyError, TypeError, ValueError):
        pass

    # Older Capsule metadata did not include frame_count. A same-stem BVH has
    # the authoritative frame count in its small header and avoids rescanning a
    # potentially hundreds-of-megabytes CSV whenever the page is opened.
    source_file = str(source.get("file") or "").replace("\\", "/").strip("/")
    relative = Path(source_file)
    if not source_file or relative.is_absolute() or ".." in relative.parts:
        return None
    bvh_path = (path.parent / relative).with_suffix(".bvh")
    try:
        with bvh_path.open("r", encoding="utf-8-sig", errors="replace") as stream:
            for _ in range(1000):
                line = stream.readline()
                if not line:
                    break
                match = re.fullmatch(r"\s*Frames:\s*(\d+)\s*", line)
                if match:
                    return int(match.group(1))
    except OSError:
        pass
    return None


def capsule_metadata(
    capsule_id: str,
    user_id: str = "local_user",
) -> dict[str, Any]:
    """Return Capsule metadata without trusting client-supplied display values."""
    path = (
        workspace_root() / "users" / user_id
        / "capsules" / capsule_id / "metadata.json"
    )
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return {}



def selected_frame_count(cfg: dict[str, Any]) -> int | None:
    try:
        fr = cfg.get("frame_range", {})
        start = int(fr.get("start", 0))
        stop = fr.get("stop")
        if stop is None:
            return None
        stop = int(stop)
        source_fps = float(cfg.get("source", {}).get("sampling_rate_hz", 100.0))
        target_fps = float(cfg.get("sampling", {}).get("rate_fps", 30.0))
        if source_fps <= 0.0 or target_fps <= 0.0:
            return None
        return max(0, int(math.ceil((stop - start) * target_fps / source_fps - 1e-12)))
    except Exception:
        return None


def _main_artifact_names(main_id: str) -> tuple[str, ...]:
    return (
        f"{main_id}_main_target.npz",
        f"{main_id}_main.npz",
        f"{main_id}_main_config.json",
        f"{main_id}_main.pkl",
        f"{main_id}_main_viewer.bin",
    )


def _main_primary_frame_count(path: Path) -> int:
    if path.suffix.lower() == ".pkl":
        import pickle

        with path.open("rb") as stream:
            motion = pickle.load(stream)
        return int(len(motion["root_pos"]))
    import numpy as np

    with np.load(path, allow_pickle=False) as archive:
        return int(len(archive["frame"]))


def _main_artifact_frame_counts(path: Path, main_id: str) -> dict[str, int]:
    """Read the frame count of each self-contained Main artifact."""
    import pickle
    import struct

    import numpy as np

    target_path = path / f"{main_id}_main_target.npz"
    motion_path = path / f"{main_id}_main.npz"
    config_path = path / f"{main_id}_main_config.json"
    viewer_path = path / f"{main_id}_main_viewer.bin"
    pickle_path = path / f"{main_id}_main.pkl"
    missing = [
        name for name in _main_artifact_names(main_id)
        if not (path / name).is_file()
    ]
    if missing:
        raise RuntimeError(f"Incomplete Main artifact set: {', '.join(missing)}")
    with np.load(target_path, allow_pickle=False) as archive:
        target_frames = int(len(archive["frame"]))
    with np.load(motion_path, allow_pickle=False) as archive:
        motion_frames = int(len(archive["frame"]))
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    if str(cfg.get("main_id")) != main_id:
        raise RuntimeError(
            f"Main config ID mismatch: expected {main_id}, got {cfg.get('main_id')}"
        )
    config_frames = int(cfg.get("main_runtime_context", {}).get("frame_count", -1))
    with viewer_path.open("rb") as stream:
        raw_header = stream.read(16)
    if len(raw_header) != 16 or raw_header[:8] != b"MEVAVW02":
        raise RuntimeError("Invalid Main Viewer BIN header")
    _, header_length = struct.unpack("<II", raw_header[8:16])
    with viewer_path.open("rb") as stream:
        stream.seek(16)
        viewer_header = json.loads(stream.read(header_length).decode("utf-8"))
    if str(viewer_header.get("stage")) != "main":
        raise RuntimeError("Main Viewer BIN has a non-Main stage")
    viewer_frames = int(viewer_header.get("frame_count", viewer_header.get("frames", -1)))
    with pickle_path.open("rb") as stream:
        gmr = pickle.load(stream)
    pickle_frames = int(len(gmr["root_pos"]))
    return {
        "target": target_frames,
        "motion": motion_frames,
        "config": config_frames,
        "viewer": viewer_frames,
        "pkl": pickle_frames,
    }


def _validate_main_artifact_set(
    path: Path, main_id: str, *, expected_frames: int | None = None,
    generation_id: str | None = None,
) -> int:
    counts = _main_artifact_frame_counts(path, main_id)
    unique = set(counts.values())
    if len(unique) != 1 or next(iter(unique)) < 0:
        raise RuntimeError(f"Main artifact frame-count mismatch: {counts}")
    frame_count = next(iter(unique))
    if expected_frames is not None and frame_count != expected_frames:
        raise RuntimeError(
            f"Main artifact frame count is {frame_count}; current Primary has "
            f"{expected_frames} frames"
        )
    if generation_id is not None:
        cfg = json.loads(
            (path / f"{main_id}_main_config.json").read_text(encoding="utf-8")
        )
        if str(cfg.get("artifact_generation_id")) != generation_id:
            raise RuntimeError("Main artifact generation ID mismatch")
        import struct

        with (path / f"{main_id}_main_viewer.bin").open("rb") as stream:
            fixed = stream.read(16)
            _, header_length = struct.unpack("<II", fixed[8:16])
            viewer_header = json.loads(stream.read(header_length).decode("utf-8"))
        if str(viewer_header.get("artifact_generation_id")) != generation_id:
            raise RuntimeError("Main Viewer generation ID mismatch")
    return frame_count


def _cleanup_main_staging(path: Path, main_id: str) -> None:
    for name in (
        *_main_artifact_names(main_id),
        f"{main_id}_error.log",
        f"{main_id}_main_diagnostics.csv",
        f"{main_id}_main_targets.csv",
        f"{main_id}_main_validation.json",
    ):
        (path / name).unlink(missing_ok=True)
    try:
        path.rmdir()
    except (FileNotFoundError, OSError):
        pass


def _publish_main_artifact_set(
    staging: Path, destination: Path, main_id: str, *,
    expected_frames: int, generation_id: str,
) -> tuple[Path, list[str]]:
    """Validate all five files, then publish Viewer last as the set marker."""
    _validate_main_artifact_set(
        staging, main_id, expected_frames=expected_frames,
        generation_id=generation_id,
    )
    destination.mkdir(parents=True, exist_ok=True)
    publish_order = (
        f"{main_id}_main_target.npz",
        f"{main_id}_main.npz",
        f"{main_id}_main_config.json",
        f"{main_id}_main.pkl",
        f"{main_id}_main_viewer.bin",
    )
    for name in publish_order:
        (staging / name).replace(destination / name)
    _validate_main_artifact_set(
        destination, main_id, expected_frames=expected_frames,
        generation_id=generation_id,
    )
    return destination, list(publish_order)


def _publish_main_failure_artifacts(
    staging: Path, destination: Path, main_id: str, log_lines: list[str],
) -> tuple[Path, list[str]]:
    """Publish only the reproducibility snapshot, partial Viewer, and error log."""
    config_name = f"{main_id}_main_config.json"
    viewer_name = f"{main_id}_main_viewer.bin"
    error_name = f"{main_id}_error.log"
    if not (staging / config_name).exists():
        raise RuntimeError("Failed Main did not leave its config snapshot")
    if not (staging / error_name).exists():
        (staging / error_name).write_text(
            "Main retarget failed.\n\n" + "\n".join(log_lines[-120:]) + "\n",
            encoding="utf-8",
        )
    destination.mkdir(parents=True, exist_ok=True)
    # A retry of the same Main ID must never leave a previously successful
    # NPZ/PKL set beside the new failed status.
    for name in (*_main_artifact_names(main_id), error_name):
        (destination / name).unlink(missing_ok=True)
    publish_order = [config_name]
    if (staging / viewer_name).exists():
        publish_order.append(viewer_name)
    publish_order.append(error_name)
    for name in publish_order:
        (staging / name).replace(destination / name)
    return destination, publish_order


def _publish_primary_failure_artifacts(
    rdir: Path, run_id: str, request_path: Path, log_lines: list[str],
) -> tuple[Path, list[str]]:
    """Leave the same diagnostic-only contract used by a failed Main."""
    run = rdir / run_id
    run.mkdir(parents=True, exist_ok=True)
    config_name = f"{run_id}_primary_config.json"
    viewer_name = f"{run_id}_primary_viewer.bin"
    error_name = f"{run_id}_error.log"
    config_path = run / config_name
    if not config_path.exists():
        snapshot = load_json(request_path)
        snapshot["schema_version"] = str(snapshot.get("schema_version") or "1.0")
        snapshot["name"] = str(
            snapshot.get("name") or snapshot.get("config_name") or "Primary Standard"
        )
        snapshot["run_status"] = "failed"
        atomic_write_json(config_path, snapshot)
    error_path = run / error_name
    if not error_path.exists():
        error_path.write_text(
            "Primary retarget failed.\n\n" + "\n".join(log_lines[-120:]) + "\n",
            encoding="utf-8",
        )
    for name in (
        f"{run_id}_primary_target.npz", f"{run_id}_primary.npz",
        f"{run_id}_primary.pkl",
    ):
        (run / name).unlink(missing_ok=True)
    (rdir / f".{run_id}_primary_target.npz").unlink(missing_ok=True)
    files = [config_name]
    if (run / viewer_name).exists():
        files.append(viewer_name)
    files.append(error_name)
    return run, files


def update_job(job_id: str, **values: Any) -> None:
    with JOBS_LOCK:
        if job_id in JOBS:
            JOBS[job_id].update(values)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Could not read JSON: {path.name}: {exc}",
        ) from exc


def run_config_path(
    capsule_id: str,
    robot_variant: str,
    run_id: str,
    user_id: str = "local_user",
) -> Path:
    run = robot_dir(capsule_id, robot_variant, user_id) / run_id

    preferred = run / f"{run_id}_primary_config.json"
    if preferred.exists():
        return preferred

    # Backward compatibility with older runs.
    for legacy in (run / f"{run_id}_config.json", run / "config.json"):
        if legacy.exists():
            return legacy

    raise HTTPException(
        status_code=404,
        detail=f"Config snapshot not found for run {run_id}",
    )


class DefaultConfigRequest(BaseModel):
    capsule_id: str
    robot_variant: str = "g1_29dof"
    user_id: str = "local_user"
    config: dict[str, Any]


class SharedConfigSaveRequest(BaseModel):
    capsule_id: str
    name: str = Field(min_length=1, max_length=200)
    source_type: str = "meva"
    manufacturer: str = "unitree"
    robot_variant: str = "g1_29dof"
    user_id: str = "local_user"
    stage: Literal["primary", "main"] = "primary"
    run_id: str | None = None
    selected_scope: Literal["xenoma", "user"] | None = None
    selected_filename: str | None = None
    overwrite: bool = False
    config: dict[str, Any]


class RunRequest(BaseModel):
    capsule_id: str
    robot_variant: str = "g1_29dof"
    user_id: str = "local_user"
    source: str = "new"  # "new" or existing run ID
    overwrite: bool = False
    config: dict[str, Any]
    iteration_diagnostics: bool = False


class MainRunRequest(BaseModel):
    capsule_id: str
    run_id: str
    main_id: str = "new"
    robot_variant: str = "g1_29dof"
    user_id: str = "local_user"
    config: dict[str, Any]


class MainDeleteSelection(BaseModel):
    primary_run_id: str
    main_id: str


class DataManagementDeleteRequest(BaseModel):
    capsule_id: str
    robot_variant: str = "g1_29dof"
    user_id: str = "local_user"
    primary_run_ids: list[str] = Field(default_factory=list)
    main_results: list[MainDeleteSelection] = Field(default_factory=list)


def _capsule_runtime_context(
    capsule_id: str,
    robot_variant: str,
    user_id: str = "local_user",
) -> dict[str, Any]:
    """Build only the Capsule-specific fields merged into a Shared Config."""
    if not CAPSULE_RE.fullmatch(capsule_id) or user_id != "local_user":
        raise HTTPException(status_code=404, detail="Capsule not found")
    capsules = (workspace_root() / "users" / user_id / "capsules").resolve()
    capsule = (capsules / capsule_id).resolve()
    if capsule.parent != capsules or not capsule.is_dir():
        raise HTTPException(status_code=404, detail="Capsule not found")

    existing_path = default_config_path(capsule_id, robot_variant, user_id)
    existing: dict[str, Any] = {}
    if existing_path.exists():
        existing = load_json(existing_path)
    existing_source = deepcopy(existing.get("source") or {})

    metadata_path = capsule / "metadata.json"
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=409, detail="Capsule metadata is unavailable") from exc
    source_metadata = metadata.get("meva_source") or {}
    source_relative = str(source_metadata.get("file") or "").replace("\\", "/").strip("/")
    logical_prefix = Path("workspace") / "users" / user_id / "capsules" / capsule_id
    logical_prefix_text = logical_prefix.as_posix() + "/"
    existing_file = str(existing_source.get("file") or "").replace("\\", "/")
    if not source_relative and existing_file.startswith(logical_prefix_text):
        source_relative = existing_file[len(logical_prefix_text):]
    relative_path = Path(source_relative)
    if not source_relative or relative_path.is_absolute() or ".." in relative_path.parts:
        raise HTTPException(status_code=409, detail="Capsule MEVA source is unavailable")
    source_file = capsule / relative_path
    if not source_file.is_file():
        raise HTTPException(status_code=409, detail="Capsule MEVA source is unavailable")

    source: dict[str, Any] = {
        "type": "meva_csv",
        "file": (logical_prefix / relative_path).as_posix(),
        "header_row_1based": int(
            source_metadata.get("header_row_1based")
            or source_metadata.get("header_row")
            or existing_source.get("header_row_1based")
            or 8
        ),
        "sampling_rate_hz": float(
            source_metadata.get("sampling_rate_hz")
            or existing_source.get("sampling_rate_hz")
            or 100.0
        ),
        "quaternion_order": str(
            source_metadata.get("quaternion_order")
            or existing_source.get("quaternion_order")
            or "wxyz"
        ),
        "quaternion_columns": str(
            source_metadata.get("quaternion_columns")
            or existing_source.get("quaternion_columns")
            or "{segment}_q_gs_{component}"
        ),
    }
    bvh_relative = source_metadata.get("bvh")
    if not bvh_relative:
        same_stem = relative_path.with_suffix(".bvh")
        if (capsule / same_stem).is_file():
            bvh_relative = same_stem.as_posix()
        else:
            bvh_file = next((path for path in (capsule / "meva").glob("*.bvh")), None)
            if bvh_file:
                bvh_relative = bvh_file.relative_to(capsule).as_posix()
    if bvh_relative:
        bvh_path = Path(str(bvh_relative).replace("\\", "/").strip("/"))
        if not bvh_path.is_absolute() and ".." not in bvh_path.parts:
            source["bvh"] = (logical_prefix / bvh_path).as_posix()
    return {
        "capsule_id": capsule_id,
        "source": source,
        "frame_range": deepcopy(
            existing.get("frame_range")
            or {"start": 0, "stop": None, "step": 1}
        ),
        "sampling": deepcopy(
            existing.get("sampling")
            or {"rate_fps": 30.0}
        ),
        "output": deepcopy(existing.get("output") or {}),
    }


def _shared_error(exc: ConfigStoreError, status_code: int = 400) -> HTTPException:
    return HTTPException(status_code=status_code, detail=str(exc))


@router.get("/robots")
def get_robot_catalog():
    try:
        return public_catalog(repo_root())
    except RobotRegistryError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/configs")
def get_shared_configs(
    source_type: str = "meva",
    manufacturer: str = "unitree",
    robot_variant: str = "g1_29dof",
    user_id: str = "local_user",
    stage: Literal["primary", "main"] = "primary",
):
    _registered_variant(robot_variant, manufacturer=manufacturer)
    try:
        configs = list_shared_configs(
            source_type=source_type,
            manufacturer=manufacturer,
            robot_variant=robot_variant,
            user_id=user_id,
            stage=stage,
        )
    except ConfigStoreError as exc:
        raise _shared_error(exc) from exc
    return {"configs": [record.as_dict() for record in configs]}


@router.get("/configs/load")
def get_shared_config(
    capsule_id: str,
    scope: Literal["xenoma", "user"],
    filename: str,
    source_type: str = "meva",
    manufacturer: str = "unitree",
    robot_variant: str = "g1_29dof",
    user_id: str = "local_user",
    stage: Literal["primary", "main"] = "primary",
    run_id: str | None = None,
):
    variant = _registered_variant(robot_variant, manufacturer=manufacturer)
    if stage == "main":
        if not CAPSULE_RE.fullmatch(capsule_id) or user_id != "local_user":
            raise HTTPException(status_code=404, detail="Capsule not found")
        if not run_id or not RUN_RE.fullmatch(run_id):
            raise HTTPException(status_code=400, detail="A Primary run_id is required for Main config")
    try:
        record, shared = load_shared_config(
            scope=scope,
            filename=filename,
            source_type=source_type,
            manufacturer=manufacturer,
            robot_variant=robot_variant,
            user_id=user_id,
            stage=stage,
        )
        if stage == "main":
            assert run_id is not None
            primary = load_json(run_config_path(capsule_id, robot_variant, run_id, user_id))
            runtime = _overlay_main_defaults(primary, shared)
            runtime["schema_version"] = str(shared.get("schema_version") or "1.0")
            runtime["name"] = record.name
            runtime["config_name"] = record.name
            runtime["retarget_stage"] = "main"
        else:
            runtime = merge_runtime_config(
                shared,
                _capsule_runtime_context(capsule_id, robot_variant, user_id),
            )
        runtime = _runtime_robot_config(runtime, variant)
        _validate_retarget_config_or_http(variant, runtime)
    except ConfigStoreError as exc:
        raise _shared_error(exc, 404) from exc
    return {
        "config": runtime,
        "shared_config": shared,
        "selection": record.as_dict(),
    }


@router.post("/configs")
def save_shared_config(req: SharedConfigSaveRequest):
    variant = _registered_variant(req.robot_variant, manufacturer=req.manufacturer)
    _assert_config_robot(req.config, variant)
    _validate_retarget_config_or_http(variant, req.config)
    try:
        primary: dict[str, Any] | None = None
        if req.stage == "main":
            if not CAPSULE_RE.fullmatch(req.capsule_id) or req.user_id != "local_user":
                raise HTTPException(status_code=404, detail="Capsule not found")
            if not req.run_id or not RUN_RE.fullmatch(req.run_id):
                raise HTTPException(
                    status_code=400,
                    detail="A Primary run_id is required for Main config",
                )
            # Validate the Config path components and the Primary snapshot before
            # writing the User Config, so a failed Main save has no side effects.
            list_shared_configs(
                source_type=req.source_type,
                manufacturer=req.manufacturer,
                robot_variant=req.robot_variant,
                user_id=req.user_id,
                stage="main",
            )
            primary = load_json(run_config_path(
                req.capsule_id, req.robot_variant, req.run_id, req.user_id
            ))
        record, shared = save_user_config(
            req.config,
            name=req.name,
            source_type=req.source_type,
            manufacturer=req.manufacturer,
            robot_variant=req.robot_variant,
            selected_scope=req.selected_scope,
            selected_filename=req.selected_filename,
            overwrite=req.overwrite,
            user_id=req.user_id,
            stage=req.stage,
        )
        if req.stage == "main":
            assert primary is not None
            runtime = _overlay_main_defaults(primary, shared)
            runtime["schema_version"] = str(shared.get("schema_version") or "1.0")
            runtime["name"] = record.name
            runtime["config_name"] = record.name
            runtime["retarget_stage"] = "main"
            runtime = _runtime_robot_config(runtime, variant)
            atomic_write_json(
                main_default_config_path(req.capsule_id, req.robot_variant, req.user_id),
                runtime,
            )
        else:
            runtime = merge_runtime_config(
                shared,
                _capsule_runtime_context(req.capsule_id, req.robot_variant, req.user_id),
            )
            # Preserve the existing per-Capsule runtime default path for Primary and
            # older clients. It is a composed runtime document, not a Shared Config.
            atomic_write_json(
                default_config_path(req.capsule_id, req.robot_variant, req.user_id),
                _runtime_robot_config(runtime, variant),
            )
        runtime = _runtime_robot_config(runtime, variant)
    except ConfigNameCollision as exc:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "CONFIG_NAME_COLLISION",
                "message": str(exc),
                "filename": exc.filename,
            },
        ) from exc
    except ConfigStoreError as exc:
        raise _shared_error(exc) from exc
    return {
        "ok": True,
        "config": runtime,
        "shared_config": shared,
        "selection": record.as_dict(),
    }


@router.get("/context")
def get_context(
    capsule_id: str,
    robot_variant: str = "g1_29dof",
    manufacturer: str | None = None,
    robot_id: str | None = None,
    user_id: str = "local_user",
):
    variant = _registered_variant(
        robot_variant, manufacturer=manufacturer, robot_id=robot_id
    )
    rdir = robot_dir(capsule_id, robot_variant, user_id)
    cfg_path = default_config_path(capsule_id, robot_variant, user_id)

    default_config = None
    if cfg_path.exists():
        default_config = _runtime_robot_config(load_json(cfg_path), variant)
        _normalize_ground_contact_estimation(default_config)
    else:
        # A newly uploaded Capsule has no per-Capsule config file. Compose the
        # read-only Xenoma default in memory without creating one on upload/open.
        try:
            _, shared_default = load_shared_config(
                scope="xenoma",
                filename="primary_standard.json",
                source_type="meva",
                manufacturer=variant.manufacturer_id,
                robot_variant=robot_variant,
                user_id=user_id,
                stage="primary",
            )
            default_config = merge_runtime_config(
                shared_default,
                _capsule_runtime_context(capsule_id, robot_variant, user_id),
            )
            default_config = _runtime_robot_config(default_config, variant)
            _normalize_ground_contact_estimation(default_config)
        except ConfigStoreError:
            default_config = None

    metadata = capsule_metadata(capsule_id, user_id)
    total_frames = metadata_frame_count(capsule_id, user_id)
    if total_frames is None and default_config:
        # Backward compatibility for capsules created before metadata included
        # meva_source.frame_count.
        total_frames = count_source_frames(default_config)

    model_metadata = {
        "joints": [], "bodies": [], "groups": [], "actuated_dof_count": 0,
        "joint_symmetry": {}, "body_symmetry": {}, "collision_pairs": [],
    }
    try:
        # Robot structure belongs to the registered Runtime Model, not to a
        # Retargeting Config.  It must therefore be available before the first
        # Primary/Main standard Config is installed.
        model_config = {
            "robot": variant.runtime_robot(repo_root()),
        }
        from server.retarget.robot_model_info import robot_model_metadata
        model_metadata = robot_model_metadata(repo_root(), model_config)
        if int(model_metadata.get("actuated_dof_count", 0)) != int(variant.variant["dof"]):
            raise ValueError(
                f"Robot manifest DOF mismatch: manufacturer={variant.manufacturer_id}, "
                f"robot={variant.robot_id}, variant={variant.variant_id}, "
                f"manifest={variant.variant['dof']}, model={model_metadata.get('actuated_dof_count')}"
            )
        if default_config:
            _validate_retarget_config_or_http(variant, default_config)
    except HTTPException:
        raise
    except Exception as exc:
        model_metadata["warning"] = f"{type(exc).__name__}: {exc}"
    source_metadata = metadata.get("meva_source") or {}
    config_source = (default_config or {}).get("source") or {}
    source_fps = float(
        source_metadata.get("sampling_rate_hz")
        or config_source.get("sampling_rate_hz")
        or 100.0
    )
    robot = deepcopy((default_config or {}).get("robot") or {})
    return {
        "capsule_id": capsule_id,
        "capsule": {
            "id": capsule_id,
            "title": str(metadata.get("title") or capsule_id),
        },
        "source": {
            "type": str(source_metadata.get("type") or "meva"),
            "frame_count": total_frames,
            "sampling_rate_hz": source_fps,
        },
        "robot": robot,
        "robot_registration": {
            "manufacturer_id": variant.manufacturer_id,
            "manufacturer_name": variant.manufacturer_name,
            "robot_id": variant.robot_id,
            "robot_name": variant.robot_name,
            "variant": variant.public_dict(),
        },
        "robot_variant": robot_variant,
        "default_config_exists": cfg_path.exists(),
        "default_config": default_config,
        "runs": list_run_ids(rdir),
        "primary_runs": list_primary_run_ids(rdir),
        "total_frames": total_frames,
        "max_frame": (total_frames - 1) if total_frames and total_frames > 0 else None,
        "robot_model": model_metadata,
    }


@router.get("/data-management")
def get_data_management(
    capsule_id: str,
    robot_variant: str = "g1_29dof",
    user_id: str = "local_user",
):
    """Return the same filesystem-backed result set used by VIEW DATA."""
    rdir = robot_dir(capsule_id, robot_variant, user_id)
    primaries = []
    for run_id in list_primary_run_ids(rdir):
        run = rdir / run_id
        mains = []
        for main_id in list_main_result_ids(run, run_id):
            result_dir = resolve_main_result_dir(
                capsule_id, robot_variant, run_id, main_id, user_id
            )
            mains.append({
                "main_id": main_id,
                "primary_run_id": run_id,
                "layout": "legacy" if result_dir.parent.name.lower() == "main" else "current",
                "pkl_exists": (result_dir / f"{main_id}_main.pkl").exists(),
            })
        primaries.append({
            "run_id": run_id,
            "pkl_exists": (
                (run / f"{run_id}_primary.npz").exists()
                or (run / f"{run_id}_primary.pkl").exists()
                or (run / "primary.pkl").exists()
            ),
            "mains": mains,
        })
    return {"source_of_truth": "filesystem_result_artifacts", "primaries": primaries}


@router.post("/data-management/delete")
def delete_data_management_results(req: DataManagementDeleteRequest):
    rdir = robot_dir(req.capsule_id, req.robot_variant, req.user_id)
    primary_ids = set(req.primary_run_ids)
    for run_id in primary_ids:
        if not RUN_RE.fullmatch(run_id):
            raise HTTPException(status_code=400, detail=f"Invalid run_id: {run_id}")
    main_selections = {(item.primary_run_id, item.main_id) for item in req.main_results}
    for run_id, main_id in main_selections:
        if (
            not RUN_RE.fullmatch(run_id)
            or not MAIN_ID_RE.fullmatch(main_id)
            or not main_id.startswith(f"{run_id}-")
        ):
            raise HTTPException(status_code=400, detail=f"Invalid Main selection: {main_id}")

    with JOBS_LOCK:
        active = [
            job for job in JOBS.values()
            if job.get("status") in {"queued", "running"}
            and (
                job.get("run_id") in primary_ids
                or (job.get("run_id"), job.get("main_id")) in main_selections
            )
        ]
    if active:
        raise HTTPException(status_code=409, detail="A selected result is still being calculated")

    deleted: list[str] = []
    # Main selections beneath a selected Primary are removed by the Primary cascade.
    for run_id, main_id in sorted(main_selections):
        if run_id in primary_ids:
            continue
        result_dir = resolve_main_result_dir(
            req.capsule_id, req.robot_variant, run_id, main_id, req.user_id
        )
        run = (rdir / run_id).resolve()
        resolved = result_dir.resolve()
        if resolved.parent not in {run, (run / "main").resolve()}:
            raise HTTPException(status_code=400, detail="Unsafe Main result path")
        shutil.rmtree(resolved)
        deleted.append(main_id)

    for run_id in sorted(primary_ids):
        run = (rdir / run_id).resolve()
        if not run.is_dir() or run.parent != rdir.resolve():
            raise HTTPException(status_code=404, detail=f"Primary result not found: {run_id}")
        child_ids = list_main_result_ids(run, run_id)
        shutil.rmtree(run)
        deleted.extend(child_ids)
        deleted.append(run_id)
    return {"deleted": deleted}


@router.get("/viewer/validation")
def get_viewer_validation(
    capsule_id: str,
    run_id: str,
    stage: Literal["primary", "main"] = "primary",
    main_id: str = "legacy",
    robot_variant: str = "g1_29dof",
    user_id: str = "local_user",
):
    if not RUN_RE.fullmatch(run_id):
        raise HTTPException(status_code=400, detail="Invalid run_id")
    if stage == "main" and main_id != "legacy":
        if not MAIN_ID_RE.fullmatch(main_id) or not main_id.startswith(f"{run_id}-"):
            raise HTTPException(status_code=400, detail="Invalid main_id")
    from server.retarget.validation_data import validation_metadata_path
    run = robot_dir(capsule_id, robot_variant, user_id) / run_id
    path = validation_metadata_path(run, run_id, stage, main_id)
    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Precomputed {stage} validation data not found; rerun {stage.title()}.",
        )
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Invalid validation metadata: {exc}") from exc


@router.get("/viewer/file/validation")
def get_viewer_validation_file(
    capsule_id: str,
    run_id: str,
    asset: str,
    stage: Literal["primary", "main"] = "primary",
    main_id: str = "legacy",
    robot_variant: str = "g1_29dof",
    user_id: str = "local_user",
):
    if not RUN_RE.fullmatch(run_id):
        raise HTTPException(status_code=400, detail="Invalid run_id")
    if stage == "main" and main_id != "legacy":
        if not MAIN_ID_RE.fullmatch(main_id) or not main_id.startswith(f"{run_id}-"):
            raise HTTPException(status_code=400, detail="Invalid main_id")
    from server.retarget.validation_data import validation_metadata_path
    run = robot_dir(capsule_id, robot_variant, user_id) / run_id
    metadata_path = validation_metadata_path(run, run_id, stage, main_id)
    if not metadata_path.exists():
        raise HTTPException(status_code=404, detail="Precomputed validation data not found")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    filename = metadata.get("files", {}).get(asset)
    if not filename or Path(filename).name != filename:
        raise HTTPException(status_code=400, detail="Unknown validation asset")
    path = metadata_path.parent / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Validation asset not found: {filename}")
    return FileResponse(
        path,
        media_type="text/csv; charset=utf-8",
        filename=filename,
        headers={"Cache-Control": "no-store, no-cache, must-revalidate"},
    )


@router.get("/main-targets/file")
def get_main_targets_file(
    capsule_id: str,
    run_id: str,
    main_id: str = "legacy",
    robot_variant: str = "g1_29dof",
    user_id: str = "local_user",
):
    if not RUN_RE.fullmatch(run_id):
        raise HTTPException(status_code=400, detail="Invalid run_id")
    if main_id == "legacy":
        path = robot_dir(capsule_id, robot_variant, user_id) / run_id / f"{run_id}_main_targets.csv"
    else:
        if not MAIN_ID_RE.fullmatch(main_id) or not main_id.startswith(f"{run_id}-"):
            raise HTTPException(status_code=400, detail="Invalid main_id")
        path = resolve_main_result_dir(
            capsule_id, robot_variant, run_id, main_id, user_id
        ) / f"{main_id}_main_targets.csv"
    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Main target CSV not found for run {run_id}",
        )
    return FileResponse(
        path,
        media_type="text/csv; charset=utf-8",
        filename=path.name,
        headers={"Cache-Control": "no-store, no-cache, must-revalidate"},
    )


def _overlay_main_defaults(primary_cfg: dict[str, Any], overlay: dict[str, Any] | None) -> dict[str, Any]:
    cfg = deepcopy(primary_cfg)
    cfg["config_name"] = "Main Standard"
    cfg["main"] = {
        "gcp_smoothing_ms": 150.0,
        "gcp_min_offset": 0.2,
        "gcp_max_offset": 0.99,
        "gcp_power_number": 2.0,
        "flying_min_percent": 0.0,
        "flying_max_percent": 0.0,
        "ground_contact_height_correction": {
            "full_correction_height_m": 0.02,
            "no_correction_height_m": 0.04,
            "sole_position_weights": {
                "left": [{"x": 0.0, "y": 0.0, "z": 1.0} for _ in range(4)],
                "right": [{"x": 0.0, "y": 0.0, "z": 1.0} for _ in range(4)],
            },
        },
        "global_contact_anchoring": {
            "enabled": True,
        },
    }
    if overlay:
        if overlay.get("config_name"):
            cfg["config_name"] = str(overlay["config_name"])
        # Main defaults are independent from the selected Primary run.  Apply
        # only common IK configuration, never Primary source/output identity.
        for key in (
            "mappings",
            "root",
            "world_alignment",
            "temporal_regularization",
            "interframe_joint_velocity_limit",
            "interframe_joint_acceleration_limit",
            "joint_limit_avoidance",
            "self_collision_avoidance",
            "spatial_constraints",
            "solver",
        ):
            if key in overlay:
                cfg[key] = deepcopy(overlay[key])
        if isinstance(overlay.get("main"), dict):
            overlay_main = deepcopy(overlay["main"])
            overlay_height = overlay_main.pop("ground_contact_height_correction", None)
            for legacy_key in (
                "geom_flatness_threshold_m",
                "gcp_contact_threshold",
                "robot_foot_ground_height_m",
                "g1_foot_ground_height_m",
                "gcp_offset",
                "gcp_multiplier",
            ):
                overlay_main.pop(legacy_key, None)
            cfg["main"].update(overlay_main)
            if isinstance(overlay_height, dict):
                cfg["main"]["ground_contact_height_correction"].update(overlay_height)
    anchoring = cfg["main"].get("global_contact_anchoring", {})
    cfg["main"]["global_contact_anchoring"] = {
        "enabled": bool(anchoring.get("enabled", True))
    }
    cfg["main"].setdefault("flying_min_percent", 0.0)
    cfg["main"].setdefault("flying_max_percent", 0.0)
    return cfg


@router.get("/main-config")
def get_main_config(
    capsule_id: str,
    run_id: str,
    main_id: str = "new",
    robot_variant: str = "g1_29dof",
    user_id: str = "local_user",
):
    if not RUN_RE.fullmatch(run_id):
        raise HTTPException(status_code=400, detail="Invalid run_id")

    run = robot_dir(capsule_id, robot_variant, user_id) / run_id
    primary_path = run / f"{run_id}_primary.npz"
    if not primary_path.exists():
        primary_path = next((path for path in (
            run / f"{run_id}_primary.pkl", run / "primary.pkl"
        ) if path.exists()), primary_path)
    if not primary_path.exists():
        raise HTTPException(status_code=409, detail=f"Primary motion not found for run {run_id}")

    primary_cfg = load_json(run_config_path(capsule_id, robot_variant, run_id, user_id))
    legacy_cfg_path = main_run_config_path(capsule_id, robot_variant, run_id, user_id)
    default_main_cfg_path = main_default_config_path(capsule_id, robot_variant, user_id)
    results_dir = main_results_dir(capsule_id, robot_variant, run_id, user_id)
    main_ids = list_main_result_ids(results_dir, run_id)

    if main_id == "legacy":
        if not legacy_cfg_path.exists():
            raise HTTPException(status_code=404, detail="Legacy Main config not found")
        cfg = load_json(legacy_cfg_path)
        main_path = run / f"{run_id}_main.pkl"
        main_csv_path = run / f"{run_id}_main_targets.csv"
    elif main_id == "new":
        overlay = load_json(default_main_cfg_path) if default_main_cfg_path.exists() else None
        cfg = _overlay_main_defaults(primary_cfg, overlay)
        main_path = Path()
        main_csv_path = Path()
    else:
        if not MAIN_ID_RE.fullmatch(main_id) or not main_id.startswith(f"{run_id}-"):
            raise HTTPException(status_code=400, detail="Invalid main_id")
        cfg_path = main_result_json_path(capsule_id, robot_variant, run_id, main_id, user_id)
        if not cfg_path.exists():
            for fallback in (cfg_path.parent / "main.json", cfg_path.parent / f"{main_id}_main.json"):
                if fallback.exists():
                    cfg_path = fallback
                    break
        cfg = load_json(cfg_path)
        result_dir = cfg_path.parent
        main_path = result_dir / f"{main_id}_main.pkl"
        main_csv_path = result_dir / f"{main_id}_main_targets.csv"
    main_done = main_id != "new" and main_path.exists()
    generation_id = cfg.get("artifact_generation_id") if isinstance(cfg, dict) else None
    if main_done and generation_id and main_id != "legacy":
        try:
            _validate_main_artifact_set(
                main_path.parent,
                main_id,
                expected_frames=_main_primary_frame_count(primary_path),
                generation_id=str(generation_id),
            )
        except RuntimeError:
            main_done = False
    return {
        "run_id": run_id,
        "main_id": main_id,
        "main_ids": main_ids,
        "legacy_main_exists": legacy_cfg_path.exists(),
        "config": cfg,
        "primary_done": True,
        "main_done": main_done,
        "main_csv_exists": main_id != "new" and main_csv_path.exists(),
        "run_main_config_exists": main_id != "new",
        "main_default_config_exists": default_main_cfg_path.exists(),
        "sole_geoms": _sole_geom_descriptors(cfg),
    }


@router.post("/main/default")
def save_main_default(req: DefaultConfigRequest):
    cfg = deepcopy(req.config)
    robot = cfg.get("robot", {})
    variant = _registered_variant(
        req.robot_variant,
        manufacturer=str(robot.get("manufacturer") or "") or None,
        robot_id=str(robot.get("model") or "") or None,
    )
    cfg = _runtime_robot_config(cfg, variant)
    _validate_retarget_config_or_http(variant, cfg)
    cfg["config_name"] = str(cfg.get("config_name") or "Main Standard")
    cfg.setdefault("main", {})
    cfg.pop("main_id", None)
    cfg.pop("primary_run_id", None)
    cfg.pop("main_calibration", None)
    cfg.pop("ground_contact_estimation", None)
    path = main_default_config_path(req.capsule_id, req.robot_variant, req.user_id)
    atomic_write_json(path, cfg)
    return {
        "ok": True,
        "path": str(path.relative_to(repo_root())).replace("\\", "/"),
    }


@router.get("/run-config")
def get_run_config(
    capsule_id: str,
    run_id: str,
    robot_variant: str = "g1_29dof",
    user_id: str = "local_user",
):
    if not RUN_RE.fullmatch(run_id):
        raise HTTPException(status_code=400, detail="Invalid run_id")

    path = run_config_path(
        capsule_id,
        robot_variant,
        run_id,
        user_id,
    )
    run = robot_dir(capsule_id, robot_variant, user_id) / run_id
    primary_path = run / f"{run_id}_primary.npz"
    main_path = run / f"{run_id}_main.pkl"
    main_csv_path = run / f"{run_id}_main_targets.csv"
    nested_ids = list_main_result_ids(run, run_id)
    nested_main_done = any(
        resolve_main_result_dir(
            capsule_id, robot_variant, run_id, main_id, user_id
        ).joinpath(f"{main_id}_main.pkl").exists()
        for main_id in nested_ids
    )
    nested_csv_done = any(
        resolve_main_result_dir(
            capsule_id, robot_variant, run_id, main_id, user_id
        ).joinpath(f"{main_id}_main_targets.csv").exists()
        for main_id in nested_ids
    )
    return {
        "run_id": run_id,
        "config": load_json(path),
        "primary_done": primary_path.exists() or any((run / name).exists() for name in (
            f"{run_id}_primary.pkl", "primary.pkl"
        )),
        "main_done": main_path.exists() or nested_main_done,
        "main_csv_exists": main_csv_path.exists() or nested_csv_done,
    }


@router.post("/default")
def save_default(req: DefaultConfigRequest):
    cfg = deepcopy(req.config)
    robot = cfg.get("robot", {})
    variant = _registered_variant(
        req.robot_variant,
        manufacturer=str(robot.get("manufacturer") or "") or None,
        robot_id=str(robot.get("model") or "") or None,
    )
    cfg = _runtime_robot_config(cfg, variant)
    _validate_retarget_config_or_http(variant, cfg)
    cfg.pop("frame_range", None)
    _normalize_ground_contact_estimation(cfg)
    cfg.setdefault("output", {})
    cfg["output"]["run_id"] = "auto"
    cfg["output"].pop("overwrite_existing", None)

    path = default_config_path(
        req.capsule_id,
        req.robot_variant,
        req.user_id,
    )
    atomic_write_json(path, cfg)

    return {
        "ok": True,
        "path": str(path.relative_to(repo_root())).replace("\\", "/"),
    }


def _normalize_ground_contact_estimation(cfg: dict[str, Any]) -> dict[str, Any]:
    """Normalize fixed Foot-origin-to-ground offsets; no contact estimation."""
    legacy = dict(cfg.get("ground_contact_estimation", {}))
    offsets = cfg.setdefault("foot_to_ground_offset", {})
    meva_height = float(offsets.get("meva_m", 0.030))
    manifest_robot = _manifest_robot_foot_to_ground_offset(cfg)
    robot_height = float(
        manifest_robot
        if manifest_robot is not None
        else offsets.get("robot_m", legacy.get("robot_foot_ground_height_m", 0.035))
    )
    if not all(math.isfinite(value) and value >= 0.0 for value in (meva_height, robot_height)):
        raise HTTPException(
            status_code=400,
            detail="Foot-to-ground offsets must be finite and non-negative",
        )
    offsets.update({
        "meva_m": meva_height,
        "robot_m": robot_height,
        "robot_source": "robot_manifest" if manifest_robot is not None else "config_fallback",
    })
    cfg.pop("ground_contact_estimation", None)
    return offsets



def _prepare_run(req: RunRequest) -> tuple[str, Path, list[str], Path, bool]:
    rdir = robot_dir(
        req.capsule_id,
        req.robot_variant,
        req.user_id,
    )
    rdir.mkdir(parents=True, exist_ok=True)

    if req.source == "new":
        run_id = allocate_run_id(rdir)
        overwrite = False
    else:
        run_id = req.source
        if not RUN_RE.fullmatch(run_id):
            raise HTTPException(status_code=400, detail="Invalid source run ID")
        if not (rdir / run_id).exists():
            raise HTTPException(status_code=404, detail=f"Run not found: {run_id}")
        if not req.overwrite:
            raise HTTPException(
                status_code=409,
                detail={
                    "code": "OVERWRITE_CONFIRMATION_REQUIRED",
                    "message": f"{run_id} already exists.",
                    "run_id": run_id,
                },
            )
        overwrite = True

    # The request is the run snapshot assembled from current UI values. Do not
    # overlay the persistent default after this point.
    cfg = deepcopy(req.config)
    _normalize_ground_contact_estimation(cfg)
    cfg.setdefault("output", {})
    cfg["output"]["run_id"] = run_id
    cfg["output"]["overwrite_existing"] = overwrite
    cfg["output"].pop("pkl_name", None)
    cfg["output"]["save_diagnostics_csv"] = bool(req.iteration_diagnostics)
    cfg["output"]["save_debug_artifacts"] = bool(req.iteration_diagnostics)

    request_path = rdir / f".{run_id}_request_config.json"
    atomic_write_json(request_path, cfg)

    script = repo_root() / "server" / "retarget" / "primary_retarget.py"
    cmd = [sys.executable, "-u", str(script), str(request_path)]
    if req.iteration_diagnostics:
        cmd.append("--iteration-diagnostics")

    return run_id, rdir, cmd, request_path, overwrite


def _run_job(
    job_id: str,
    run_id: str,
    rdir: Path,
    cmd: list[str],
    cleanup_path: Path | None,
    overwrite: bool,
    finalize: Callable[[], tuple[Path, list[str]]] | None = None,
    failure_finalize: Callable[[list[str]], tuple[Path, list[str]]] | None = None,
    cleanup: Callable[[], None] | None = None,
) -> None:
    try:
        with JOBS_LOCK:
            initial_total = JOBS.get(job_id, {}).get("total")
        update_job(
            job_id,
            status="running",
            message=(
                f"Preparing... 0 / {initial_total} frames"
                if initial_total is not None
                else "Preparing..."
            ),
        )
        proc = subprocess.Popen(
            cmd,
            cwd=str(repo_root()),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )

        log_lines: list[str] = []
        assert proc.stdout is not None

        for line in proc.stdout:
            line = line.rstrip()
            if line:
                log_lines.append(line)
                if len(log_lines) > 500:
                    log_lines = log_lines[-500:]

            m = PROGRESS_RE.match(line.strip())
            if m:
                done = int(m.group(1))
                total = int(m.group(2))
                source_frame = int(m.group(3))
                update_job(
                    job_id,
                    processed=done,
                    total=total,
                    source_frame=source_frame,
                    progress=(done / total) if total else 0.0,
                    message=f"{done} / {total} frames",
                )

        returncode = proc.wait()

        if returncode != 0:
            files: list[str] = []
            if failure_finalize is not None:
                _, files = failure_finalize(log_lines)
            update_job(
                job_id,
                status="failed",
                message="Retarget failed",
                error="\n".join(log_lines[-120:]),
                files=files,
            )
            return

        if finalize is not None:
            run_path, files = finalize()
        else:
            run_path = rdir / run_id
            files = sorted(
                p.name for p in run_path.iterdir() if p.is_file()
            ) if run_path.exists() else []

        update_job(
            job_id,
            status="done",
            progress=1.0,
            message="Completed",
            files=files,
            overwritten=overwrite,
        )
    except Exception as exc:
        update_job(
            job_id,
            status="failed",
            message="Retarget failed",
            error=f"{type(exc).__name__}: {exc}",
        )
    finally:
        if cleanup_path is not None:
            cleanup_path.unlink(missing_ok=True)
        if cleanup is not None:
            try:
                cleanup()
            except Exception:
                pass


@router.post("/run-start")
def run_retarget_start(req: RunRequest):
    run_id, rdir, cmd, request_path, overwrite = _prepare_run(req)

    job_id = uuid.uuid4().hex
    with JOBS_LOCK:
        initial_total = selected_frame_count(req.config)
        JOBS[job_id] = {
            "job_id": job_id,
            "run_id": run_id,
            "status": "queued",
            "progress": 0.0,
            "processed": 0,
            "total": initial_total,
            "source_frame": None,
            "message": (
                f"0 / {initial_total} frames"
                if initial_total is not None
                else "Preparing..."
            ),
            "overwritten": overwrite,
        }

    thread = threading.Thread(
        target=_run_job,
        args=(job_id, run_id, rdir, cmd, request_path, overwrite),
        kwargs={
            "failure_finalize": lambda log_lines: _publish_primary_failure_artifacts(
                rdir, run_id, request_path, log_lines,
            ),
        },
        daemon=True,
    )
    thread.start()

    return JOBS[job_id]


@router.post("/main/run-start")
def run_main_start(req: MainRunRequest):
    if not RUN_RE.fullmatch(req.run_id):
        raise HTTPException(status_code=400, detail="Invalid run_id")

    rdir = robot_dir(req.capsule_id, req.robot_variant, req.user_id)
    run = rdir / req.run_id
    if not run.is_dir():
        raise HTTPException(status_code=404, detail=f"Run not found: {req.run_id}")

    primary_path = run / f"{req.run_id}_primary.npz"
    if not primary_path.exists():
        primary_path = next((path for path in (
            run / f"{req.run_id}_primary.pkl", run / "primary.pkl"
        ) if path.exists()), primary_path)
    if not primary_path.exists():
        raise HTTPException(
            status_code=409,
            detail=f"Primary motion not found for run {req.run_id}",
        )

    # Main follows the same run-snapshot rule as Primary. Capsule runtime
    # fields always come from the current Primary snapshot, never from an old
    # Main snapshot selected for Retry.
    cfg = deepcopy(req.config)
    primary_cfg = load_json(
        run_config_path(req.capsule_id, req.robot_variant, req.run_id, req.user_id)
    )
    for key in (
        "capsule_id", "source", "frame_range", "sampling",
        "foot_to_ground_offset",
    ):
        if key in primary_cfg:
            cfg[key] = deepcopy(primary_cfg[key])
    _normalize_ground_contact_estimation(cfg)
    cfg["config_name"] = str(cfg.get("config_name") or "Main Standard")
    main_cfg = cfg.setdefault("main", {})
    smoothing_ms = float(main_cfg.get("gcp_smoothing_ms", 150.0))
    gcp_min_offset = float(main_cfg.get("gcp_min_offset", 0.2))
    gcp_max_offset = float(main_cfg.get("gcp_max_offset", 0.99))
    gcp_power_number = float(main_cfg.get(
        "gcp_power_number",
        main_cfg.get("gcp_multiplier", 2.0),
    ))
    if not math.isfinite(smoothing_ms) or smoothing_ms < 0.0:
        raise HTTPException(status_code=400, detail="Average time must be finite and non-negative")
    if not (
        math.isfinite(gcp_min_offset)
        and math.isfinite(gcp_max_offset)
        and 0.0 <= gcp_min_offset < gcp_max_offset <= 1.0
    ):
        raise HTTPException(
            status_code=400,
            detail="GCP offsets require 0 <= min_offset < max_offset <= 1",
        )
    if not math.isfinite(gcp_power_number) or gcp_power_number <= 0.0:
        raise HTTPException(status_code=400, detail="gcp_power_number must be finite and greater than zero")
    height_cfg = main_cfg.setdefault("ground_contact_height_correction", {})
    full_height = float(height_cfg.get("full_correction_height_m", 0.02))
    none_height = float(height_cfg.get("no_correction_height_m", 0.04))
    if not (
        math.isfinite(full_height)
        and math.isfinite(none_height)
        and 0.0 <= full_height < none_height
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "ground_contact_height_correction requires 0 <= "
                "full_correction_height_m < no_correction_height_m"
            ),
        )
    weights = height_cfg.get("sole_position_weights", {})
    for side in ("left", "right"):
        side_weights = weights.get(side, []) if isinstance(weights, dict) else []
        if len(side_weights) != 4:
            raise HTTPException(status_code=400, detail=f"{side} sole requires four position weight rows")
        for values in side_weights:
            try:
                xyz_weights = [float(values[axis]) for axis in ("x", "y", "z")]
            except (KeyError, TypeError, ValueError):
                raise HTTPException(status_code=400, detail="Sole position weights require numeric x/y/z")
            if not all(math.isfinite(value) and value >= 0.0 for value in xyz_weights):
                raise HTTPException(status_code=400, detail="Sole position weights must be finite and non-negative")
    flying_min = float(main_cfg.get("flying_min_percent", 0.0))
    flying_max = float(main_cfg.get("flying_max_percent", 0.0))
    if not (
        math.isfinite(flying_min)
        and math.isfinite(flying_max)
        and 0.0 <= flying_min <= flying_max <= 100.0
    ):
        raise HTTPException(
            status_code=400,
            detail="Flying percentages require 0 <= min <= max <= 100",
        )
    main_cfg["flying_min_percent"] = flying_min
    main_cfg["flying_max_percent"] = flying_max
    anchoring_cfg = main_cfg.setdefault("global_contact_anchoring", {})
    anchoring_cfg.clear()
    anchoring_cfg["enabled"] = bool(
        req.config.get("main", {}).get("global_contact_anchoring", {}).get("enabled", True)
    )
    main_cfg["gcp_smoothing_ms"] = smoothing_ms
    main_cfg["gcp_min_offset"] = gcp_min_offset
    main_cfg["gcp_max_offset"] = gcp_max_offset
    main_cfg["gcp_power_number"] = gcp_power_number
    main_cfg.pop("geom_flatness_threshold_m", None)
    main_cfg.pop("gcp_contact_threshold", None)
    main_cfg.pop("robot_foot_ground_height_m", None)
    main_cfg.pop("g1_foot_ground_height_m", None)
    main_cfg.pop("gcp_offset", None)
    main_cfg.pop("gcp_multiplier", None)

    results_dir = main_results_dir(req.capsule_id, req.robot_variant, req.run_id, req.user_id)
    if req.main_id == "new":
        main_id = allocate_main_id(results_dir, req.run_id)
        overwrite = False
    else:
        main_id = req.main_id
        if not MAIN_ID_RE.fullmatch(main_id) or not main_id.startswith(f"{req.run_id}-"):
            raise HTTPException(status_code=400, detail="Invalid main_id")
        resolve_main_result_dir(
            req.capsule_id, req.robot_variant, req.run_id, main_id, req.user_id
        )
        overwrite = True

    cfg["primary_run_id"] = req.run_id
    cfg["main_id"] = main_id
    job_id = uuid.uuid4().hex
    cfg["artifact_generation_id"] = job_id
    expected_frames = _main_primary_frame_count(primary_path)
    final_dir = resolve_main_result_dir(
        req.capsule_id, req.robot_variant, req.run_id, main_id, req.user_id,
        must_exist=False,
    )
    staging_dir = run / f".{main_id}.{job_id}.staging"
    staging_dir.mkdir(parents=False, exist_ok=False)
    cfg_path = staging_dir / f"{main_id}_main_config.json"
    atomic_write_json(cfg_path, cfg)

    script = repo_root() / "server" / "retarget" / "main_retarget.py"
    cmd = [sys.executable, "-u", str(script), str(cfg_path)]

    with JOBS_LOCK:
        initial_total = expected_frames
        JOBS[job_id] = {
            "job_id": job_id,
            "run_id": req.run_id,
            "main_id": main_id,
            "stage": "main",
            "status": "queued",
            "progress": 0.0,
            "processed": 0,
            "total": initial_total,
            "source_frame": None,
            "message": (
                f"0 / {initial_total} frames"
                if initial_total is not None
                else "Preparing..."
            ),
            "overwritten": overwrite,
        }

    thread = threading.Thread(
        target=_run_job,
        args=(job_id, main_id, run, cmd, None, overwrite),
        kwargs={
            "finalize": lambda: _publish_main_artifact_set(
                staging_dir, final_dir, main_id,
                expected_frames=expected_frames, generation_id=job_id,
            ),
            "failure_finalize": lambda log_lines: _publish_main_failure_artifacts(
                staging_dir, final_dir, main_id, log_lines,
            ),
            "cleanup": lambda: _cleanup_main_staging(staging_dir, main_id),
        },
        daemon=True,
    )
    thread.start()
    return JOBS[job_id]


@router.get("/main/file")
def get_main_file(
    capsule_id: str,
    run_id: str,
    main_id: str = "legacy",
    kind: Literal["csv", "npz", "pkl"] = "csv",
    robot_variant: str = "g1_29dof",
    user_id: str = "local_user",
):
    if not RUN_RE.fullmatch(run_id):
        raise HTTPException(status_code=400, detail="Invalid run_id")
    run = robot_dir(capsule_id, robot_variant, user_id) / run_id
    result_dir = run
    file_id = run_id
    if main_id != "legacy":
        if not MAIN_ID_RE.fullmatch(main_id) or not main_id.startswith(f"{run_id}-"):
            raise HTTPException(status_code=400, detail="Invalid main_id")
        result_dir = resolve_main_result_dir(
            capsule_id, robot_variant, run_id, main_id, user_id
        )
        file_id = main_id
    if kind == "pkl":
        path = result_dir / f"{file_id}_main.pkl"
        media_type = "application/octet-stream"
    elif kind == "npz":
        path = result_dir / f"{file_id}_main.npz"
        media_type = "application/octet-stream"
    else:
        path = result_dir / f"{file_id}_main_targets.csv"
        media_type = "text/csv; charset=utf-8"
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Main {kind.upper()} not found for run {run_id}")
    return FileResponse(
        path,
        media_type=media_type,
        filename=path.name,
        headers={"Cache-Control": "no-store, no-cache, must-revalidate"},
    )


@router.get("/job/{job_id}")
def get_retarget_job(job_id: str):
    with JOBS_LOCK:
        job = JOBS.get(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found")
        return dict(job)



@router.post("/viewer/prepare")
def prepare_viewer(
    capsule_id: str,
    run_id: str,
    main_id: str = "legacy",
    robot_variant: str = "g1_29dof",
    user_id: str = "local_user",
):
    meva_only = run_id == "new"
    if not meva_only and not RUN_RE.fullmatch(run_id):
        raise HTTPException(status_code=400, detail="Invalid run_id")

    rdir = robot_dir(capsule_id, robot_variant, user_id)

    if meva_only:
        variant = _registered_variant(robot_variant)
        capsule_default = default_config_path(capsule_id, robot_variant, user_id)
        if capsule_default.exists():
            cfg = _runtime_robot_config(load_json(capsule_default), variant)
        else:
            try:
                _, shared_default = load_shared_config(
                    scope="xenoma", filename="primary_standard.json",
                    source_type="meva", manufacturer=variant.manufacturer_id,
                    robot_variant=robot_variant, user_id=user_id, stage="primary",
                )
                cfg = merge_runtime_config(
                    shared_default,
                    _capsule_runtime_context(capsule_id, robot_variant, user_id),
                )
                cfg = _runtime_robot_config(cfg, variant)
            except ConfigStoreError as exc:
                raise _shared_error(exc, 404) from exc
        run_dir = None
    else:
        run_dir = rdir / run_id
        if not run_dir.exists():
            raise HTTPException(status_code=404, detail=f"Run not found: {run_id}")
        cfg = load_json(run_config_path(
            capsule_id, robot_variant, run_id, user_id
        ))

    try:
        from server.retarget.viewer_data import generate_meva_viewer_bin

        sources = {}
        meva_bin = generate_meva_viewer_bin(
            repo_root(), capsule_id, cfg, user_id
        )
        sources["meva"] = {
            "label": "MEVA",
            "kind": "meva",
            "url": (
                f"/api/retarget/viewer/file/meva"
                f"?capsule_id={capsule_id}&robot_variant={robot_variant}"
                f"&run_id={run_id}&user_id={user_id}"
                f"&rev={meva_bin.stat().st_mtime_ns}"
            ),
            "file": meva_bin.name,
            "storage": "capsule_cache",
        }

        # New Primary and Main runs both have a persisted, self-contained
        # Viewer BIN. Canonical NPZ / legacy PKL remain read-only fallbacks.
        if not meva_only:
            for stage, label in (("primary", "Primary"), ("main", "Main")):
                stage_dir = run_dir
                file_id = run_id
                if stage == "main" and main_id != "legacy":
                    if not MAIN_ID_RE.fullmatch(main_id) or not main_id.startswith(f"{run_id}-"):
                        continue
                    stage_dir = resolve_main_result_dir(
                        capsule_id, robot_variant, run_id, main_id, user_id
                    )
                    file_id = main_id
                viewer_path = stage_dir / f"{file_id}_{stage}_viewer.bin"
                motion_path = stage_dir / f"{file_id}_{stage}.npz"
                if not motion_path.exists():
                    legacy_candidates = [stage_dir / f"{file_id}_{stage}.pkl"]
                    if stage == "primary":
                        legacy_candidates.append(run_dir / "primary.pkl")
                    legacy = next((path for path in legacy_candidates if path.exists()), None)
                    if legacy is not None:
                        motion_path = legacy
                source_path = viewer_path if viewer_path.exists() else motion_path
                if not source_path.exists():
                    continue
                stage_cfg = cfg
                if stage == "main":
                    for candidate in (
                        stage_dir / f"{file_id}_main_config.json",
                        stage_dir / "main.json",
                        stage_dir / f"{file_id}_main.json",
                    ):
                        if candidate.exists():
                            stage_cfg = load_json(candidate)
                            break
                    generation_id = stage_cfg.get("artifact_generation_id")
                    if (
                        viewer_path.exists()
                        and generation_id
                        and str(stage_cfg.get("run_status", "complete")) != "partial"
                    ):
                        primary_motion = run_dir / f"{run_id}_primary.npz"
                        if not primary_motion.exists():
                            primary_motion = next((candidate for candidate in (
                                run_dir / f"{run_id}_primary.pkl",
                                run_dir / "primary.pkl",
                            ) if candidate.exists()), primary_motion)
                        _validate_main_artifact_set(
                            stage_dir, file_id,
                            expected_frames=_main_primary_frame_count(primary_motion),
                            generation_id=str(generation_id),
                        )
                sources[stage] = {
                    "label": label,
                    "kind": "retarget",
                    "url": (
                        f"/api/retarget/viewer/file/retarget"
                        f"?capsule_id={capsule_id}&robot_variant={robot_variant}"
                        f"&run_id={run_id}&stage={stage}&user_id={user_id}"
                        f"&main_id={main_id}"
                        f"&rev={source_path.stat().st_mtime_ns}"
                    ),
                    "file": source_path.name,
                    "storage": (
                        f"{stage}_viewer_bin" if viewer_path.exists()
                        else "motion_on_demand"
                    ),
                    # Display-only limits used for physical-value tooltips and
                    # ratio coloring. These are the exact run snapshot values;
                    # Viewer never writes them back or changes IK behavior.
                    "joint_motion_limits": {
                        "velocity": deepcopy(stage_cfg.get(
                            "interframe_joint_velocity_limit", {}
                        )),
                        "acceleration": deepcopy(stage_cfg.get(
                            "interframe_joint_acceleration_limit", {}
                        )),
                    },
                }
        primary_post = None
        if not meva_only:
            primary_post_path = run_dir / f"{run_id}_primary_post.csv"
            primary_post_metadata_path = run_dir / f"{run_id}_primary_post.json"
            if not primary_post_path.exists():
                legacy_path = run_dir / f"{run_id}_main_input.csv"
                if legacy_path.exists():
                    primary_post_path = legacy_path
                    primary_post_metadata_path = run_dir / f"{run_id}_main_input.json"
            if primary_post_path.exists():
                primary_post = {
                    "url": (
                        f"/api/retarget/viewer/file/primary-post"
                        f"?capsule_id={capsule_id}&robot_variant={robot_variant}"
                        f"&run_id={run_id}&user_id={user_id}"
                        f"&rev={primary_post_path.stat().st_mtime_ns}"
                    ),
                    "file": primary_post_path.name,
                    "metadata": (
                        load_json(primary_post_metadata_path)
                        if primary_post_metadata_path.exists() else {}
                    ),
                }
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "VIEWER_PREPARE_FAILED",
                "message": f"{type(exc).__name__}: {exc}",
            },
        ) from exc

    available_stages = [x for x in ("meva", "primary", "main") if x in sources]
    return {
        "ok": True,
        "run_id": run_id,
        "meva_only": meva_only,
        "available_stages": available_stages,
        "sources": sources,
        "primary_post": primary_post,
        # Compatibility for cached viewers; the payload is Primary-post data.
        "main_input": primary_post,
        # Legacy fields kept for compatibility with older cached HTML.
        "retarget_url": sources.get("primary", {}).get("url"),
        "meva_url": sources["meva"]["url"],
        "retarget_file": sources.get("primary", {}).get("file"),
        "meva_file": sources["meva"]["file"],
    }


@router.get("/viewer/file/main-input")
@router.get("/viewer/file/primary-post")
def get_primary_post_file(
    capsule_id: str,
    run_id: str,
    robot_variant: str = "g1_29dof",
    user_id: str = "local_user",
):
    if not RUN_RE.fullmatch(run_id):
        raise HTTPException(status_code=400, detail="Invalid run_id")
    run = robot_dir(capsule_id, robot_variant, user_id) / run_id
    path = run / f"{run_id}_primary_post.csv"
    if not path.exists():
        legacy = run / f"{run_id}_main_input.csv"
        if legacy.exists():
            path = legacy
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Primary post data not found for run {run_id}")
    return FileResponse(
        path,
        media_type="text/csv; charset=utf-8",
        filename=path.name,
        headers={"Cache-Control": "no-store, no-cache, must-revalidate"},
    )


@router.get("/viewer/file/retarget")
def get_retarget_viewer_file(
    capsule_id: str,
    run_id: str,
    stage: Literal["primary", "main"] = "primary",
    main_id: str = "legacy",
    robot_variant: str = "g1_29dof",
    user_id: str = "local_user",
):
    if not RUN_RE.fullmatch(run_id):
        raise HTTPException(status_code=400, detail="Invalid run_id")
    run = robot_dir(capsule_id, robot_variant, user_id) / run_id
    result_dir = run
    file_id = run_id
    if stage == "main" and main_id != "legacy":
        if not MAIN_ID_RE.fullmatch(main_id) or not main_id.startswith(f"{run_id}-"):
            raise HTTPException(status_code=400, detail="Invalid main_id")
        result_dir = resolve_main_result_dir(
            capsule_id, robot_variant, run_id, main_id, user_id
        )
        file_id = main_id
    path = result_dir / f"{file_id}_{stage}_viewer.bin"
    if path.exists():
        if stage == "main" and main_id != "legacy":
            config_path = result_dir / f"{main_id}_main_config.json"
            if config_path.exists():
                stage_cfg = load_json(config_path)
                generation_id = stage_cfg.get("artifact_generation_id")
                if (
                    generation_id
                    and str(stage_cfg.get("run_status", "complete")) != "partial"
                ):
                    primary_motion = run / f"{run_id}_primary.npz"
                    if not primary_motion.exists():
                        primary_motion = next((candidate for candidate in (
                            run / f"{run_id}_primary.pkl", run / "primary.pkl"
                        ) if candidate.exists()), primary_motion)
                    try:
                        _validate_main_artifact_set(
                            result_dir, main_id,
                            expected_frames=_main_primary_frame_count(primary_motion),
                            generation_id=str(generation_id),
                        )
                    except RuntimeError as exc:
                        raise HTTPException(status_code=409, detail=str(exc)) from exc
        return FileResponse(
            path,
            media_type="application/octet-stream",
            filename=path.name,
            headers={"Cache-Control": "no-store, no-cache, must-revalidate"},
        )
    try:
        from server.retarget.viewer_data import build_retarget_viewer_bytes
        payload = build_retarget_viewer_bytes(
            repo_root(), capsule_id, robot_variant, run_id, user_id,
            stage=stage, main_id=main_id,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"{stage} motion viewer conversion failed: {type(exc).__name__}: {exc}",
        ) from exc
    return Response(
        content=payload,
        media_type="application/octet-stream",
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate",
            "X-MEVA-Viewer-Source": f"{stage}.npz-or-legacy-pkl",
        },
    )


@router.get("/viewer/file/meva")
def get_meva_viewer_file(
    capsule_id: str,
    run_id: str,
    robot_variant: str = "g1_29dof",
    user_id: str = "local_user",
):
    if run_id == "new":
        cfg = load_json(default_config_path(
            capsule_id, robot_variant, user_id
        ))
    else:
        if not RUN_RE.fullmatch(run_id):
            raise HTTPException(status_code=400, detail="Invalid run_id")
        cfg = load_json(run_config_path(
            capsule_id, robot_variant, run_id, user_id
        ))
    path = (
        repo_root() / "workspace" / "users" / user_id / "capsules"
        / capsule_id / "meva" / f"{capsule_id}_meva_viewer.bin"
    )
    try:
        from server.retarget.viewer_data import generate_meva_viewer_bin
        # Always pass through the generator. It performs a cheap format/block
        # check and rebuilds stale MEVA viewer binaries when required.
        path = generate_meva_viewer_bin(
            repo_root(), capsule_id, cfg, user_id
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"{type(exc).__name__}: {exc}",
        ) from exc
    return FileResponse(
        path,
        media_type="application/octet-stream",
        filename=path.name,
        headers={"Cache-Control": "public, max-age=31536000, immutable"},
    )


@router.post("/run")
def run_retarget(req: RunRequest):
    rdir = robot_dir(
        req.capsule_id,
        req.robot_variant,
        req.user_id,
    )
    rdir.mkdir(parents=True, exist_ok=True)

    if req.source == "new":
        run_id = allocate_run_id(rdir)
        overwrite = False
    else:
        run_id = req.source
        if not RUN_RE.fullmatch(run_id):
            raise HTTPException(status_code=400, detail="Invalid source run ID")
        if not (rdir / run_id).exists():
            raise HTTPException(status_code=404, detail=f"Run not found: {run_id}")
        if not req.overwrite:
            raise HTTPException(
                status_code=409,
                detail={
                    "code": "OVERWRITE_CONFIRMATION_REQUIRED",
                    "message": f"{run_id} already exists.",
                    "run_id": run_id,
                },
            )
        overwrite = True

    cfg = deepcopy(req.config)
    _normalize_ground_contact_estimation(cfg)
    cfg.setdefault("output", {})
    cfg["output"]["run_id"] = run_id
    cfg["output"]["overwrite_existing"] = overwrite
    cfg["output"].pop("pkl_name", None)
    cfg["output"]["save_diagnostics_csv"] = bool(req.iteration_diagnostics)
    cfg["output"]["save_debug_artifacts"] = bool(req.iteration_diagnostics)

    # Temporary request config stays beside the robot default so that
    # primary_retarget.py creates the run directory beneath the same folder.
    request_path = rdir / f".{run_id}_request_config.json"
    atomic_write_json(request_path, cfg)

    script = repo_root() / "server" / "retarget" / "primary_retarget.py"
    cmd = [sys.executable, "-u", str(script), str(request_path)]
    if req.iteration_diagnostics:
        cmd.append("--iteration-diagnostics")

    try:
        proc = subprocess.run(
            cmd,
            cwd=str(repo_root()),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    finally:
        # The run keeps its own <run_id>_primary_config.json snapshot.
        request_path.unlink(missing_ok=True)

    if proc.returncode != 0:
        # Keep the browser response, but also surface the real traceback
        # in the uvicorn/PowerShell console for easier debugging.
        if proc.stdout:
            print(proc.stdout, flush=True)
        if proc.stderr:
            print(proc.stderr, flush=True)

        raise HTTPException(
            status_code=500,
            detail={
                "code": "RETARGET_FAILED",
                "run_id": run_id,
                "stdout": proc.stdout[-12000:],
                "stderr": proc.stderr[-12000:],
            },
        )

    run_path = rdir / run_id
    files = []
    if run_path.exists():
        files = sorted(p.name for p in run_path.iterdir() if p.is_file())

    return {
        "ok": True,
        "run_id": run_id,
        "overwritten": overwrite,
        "files": files,
        "stdout": proc.stdout[-12000:],
    }
