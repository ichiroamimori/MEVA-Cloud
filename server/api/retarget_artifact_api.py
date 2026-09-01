from __future__ import annotations

import csv
import json
import math
import re
import shutil
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from server.retarget_config_store import workspace_root
from server.api.retarget_robot_api import repo_root


router = APIRouter()

RUN_RE = re.compile(r"^\d{10}$")
MAIN_ID_RE = re.compile(r"^(\d{10})-(\d{2})$")
JOBS: dict[str, dict[str, Any]] = {}
JOBS_LOCK = threading.Lock()


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

class MainDeleteSelection(BaseModel):
    primary_run_id: str
    main_id: str

class DataManagementDeleteRequest(BaseModel):
    capsule_id: str
    robot_variant: str = "g1_29dof"
    user_id: str = "local_user"
    primary_run_ids: list[str] = Field(default_factory=list)
    main_results: list[MainDeleteSelection] = Field(default_factory=list)

@router.get("/data-management")
def get_data_management(
    capsule_id: str,
    robot_variant: str = "g1_29dof",
    user_id: str = "local_user",
):
    """Return the same filesystem-backed result set used by VIEW DATA."""
    rdir = robot_dir(capsule_id, robot_variant, user_id)

    def config_note(path: Path) -> str:
        if not path.is_file():
            return ""
        try:
            note = str(load_json(path).get("note") or "").strip()
        except HTTPException:
            return ""
        return note[:2000]

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
                "note": config_note(result_dir / f"{main_id}_main_config.json"),
                "layout": "legacy" if result_dir.parent.name.lower() == "main" else "current",
                "pkl_exists": (result_dir / f"{main_id}_main.pkl").exists(),
            })
        primaries.append({
            "run_id": run_id,
            "note": config_note(run / f"{run_id}_primary_config.json"),
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
