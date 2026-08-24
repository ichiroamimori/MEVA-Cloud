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
import xml.etree.ElementTree as ET
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel, Field


router = APIRouter(prefix="/api/retarget", tags=["retarget"])

RUN_RE = re.compile(r"^\d{10}$")
MAIN_ID_RE = re.compile(r"^(\d{10})-(\d{2})$")
PROGRESS_RE = re.compile(r"^\[(\d+)/(\d+)\] frame (\d+)")
JOBS: dict[str, dict[str, Any]] = {}
JOBS_LOCK = threading.Lock()


def repo_root() -> Path:
    # server/api/retarget_api.py -> repo root
    return Path(__file__).resolve().parents[2]


def robot_dir(
    capsule_id: str,
    robot_variant: str,
    user_id: str = "local_user",
) -> Path:
    return (
        repo_root()
        / "workspace"
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
    """Read the four contact GEOMs directly from the configured MJCF, in XML order."""
    mjcf = config.get("robot", {}).get("mjcf")
    if not mjcf:
        return {"left": [], "right": []}
    xml_path = (repo_root() / str(mjcf)).resolve()
    try:
        root = ET.parse(xml_path).getroot()
    except (OSError, ET.ParseError):
        return {"left": [], "right": []}

    mapped = {
        str(item.get("source_segment")): str(item.get("target_link"))
        for item in config.get("mappings", [])
        if item.get("source_segment") and item.get("target_link")
    }
    bodies = {
        "left": mapped.get("LeftFoot", "left_ankle_roll_link"),
        "right": mapped.get("RightFoot", "right_ankle_roll_link"),
    }
    result: dict[str, list[dict[str, Any]]] = {"left": [], "right": []}
    for side, body_name in bodies.items():
        body = root.find(f".//body[@name='{body_name}']")
        if body is None:
            continue
        contact_geoms = [
            geom for geom in body.findall("geom")
            if geom.get("mesh") is None and geom.get("size") is not None
        ]
        for index, geom in enumerate(contact_geoms):
            name = geom.get("name")
            pos = geom.get("pos", "0 0 0")
            size = geom.get("size", "")
            display = name if name else f'geom pos="{pos}" size="{size}"'
            result[side].append({
                "index": index,
                "name": name,
                "display": display,
                "pos": pos,
                "size": size,
            })
    return result


def _robot_foot_to_ground_offset(config: dict[str, Any]) -> float | None:
    """Derive Foot-origin-to-ground distance from existing spherical sole GEOMs."""
    offsets: list[float] = []
    for items in _sole_geom_descriptors(config).values():
        bottoms: list[float] = []
        for item in items:
            try:
                z = float(str(item["pos"]).split()[2])
                radius = float(str(item["size"]).split()[0])
            except (KeyError, IndexError, TypeError, ValueError):
                continue
            bottoms.append(z - radius)
        if bottoms:
            offsets.append(-min(bottoms))
    if not offsets:
        return None
    value = round(float(sum(offsets) / len(offsets)), 12)
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
        if (run / f"{run_id}_primary.pkl").exists() or (run / "primary.pkl").exists():
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
    """Read the precomputed frame count without scanning the MEVA CSV."""
    path = (
        repo_root() / "workspace" / "users" / user_id
        / "capsules" / capsule_id / "metadata.json"
    )
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))["meva_source"][
            "frame_count"
        ]
        frame_count = int(value)
        return frame_count if frame_count >= 0 else None
    except (KeyError, TypeError, ValueError, json.JSONDecodeError, OSError):
        return None



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


@router.get("/context")
def get_context(
    capsule_id: str,
    robot_variant: str = "g1_29dof",
    user_id: str = "local_user",
):
    rdir = robot_dir(capsule_id, robot_variant, user_id)
    cfg_path = default_config_path(capsule_id, robot_variant, user_id)

    default_config = None
    if cfg_path.exists():
        default_config = load_json(cfg_path)
        _normalize_ground_contact_estimation(default_config)

    total_frames = metadata_frame_count(capsule_id, user_id)
    if total_frames is None and default_config:
        # Backward compatibility for capsules created before metadata included
        # meva_source.frame_count.
        total_frames = count_source_frames(default_config)

    model_metadata = {"joints": [], "joint_symmetry": {}, "body_symmetry": {}, "collision_pairs": []}
    if default_config:
        try:
            from server.retarget.robot_model_info import robot_model_metadata
            model_metadata = robot_model_metadata(repo_root(), default_config)
        except Exception as exc:
            model_metadata["warning"] = f"{type(exc).__name__}: {exc}"
    return {
        "capsule_id": capsule_id,
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
                (run / f"{run_id}_primary.pkl").exists() or (run / "primary.pkl").exists()
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
    cfg["config_name"] = "Robot Standard Main"
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
    primary_path = run / f"{run_id}_primary.pkl"
    if not primary_path.exists() and not (run / "primary.pkl").exists():
        raise HTTPException(status_code=409, detail=f"Primary PKL not found for run {run_id}")

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
    return {
        "run_id": run_id,
        "main_id": main_id,
        "main_ids": main_ids,
        "legacy_main_exists": legacy_cfg_path.exists(),
        "config": cfg,
        "primary_done": True,
        "main_done": main_id != "new" and main_path.exists(),
        "main_csv_exists": main_id != "new" and main_csv_path.exists(),
        "run_main_config_exists": main_id != "new",
        "main_default_config_exists": default_main_cfg_path.exists(),
        "sole_geoms": _sole_geom_descriptors(cfg),
    }


@router.post("/main/default")
def save_main_default(req: DefaultConfigRequest):
    cfg = deepcopy(req.config)
    cfg["config_name"] = str(cfg.get("config_name") or "Robot Standard Main")
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
    primary_path = run / f"{run_id}_primary.pkl"
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
        "primary_done": primary_path.exists() or (run / "primary.pkl").exists(),
        "main_done": main_path.exists() or nested_main_done,
        "main_csv_exists": main_csv_path.exists() or nested_csv_done,
    }


@router.post("/default")
def save_default(req: DefaultConfigRequest):
    cfg = deepcopy(req.config)
    cfg.pop("frame_range", None)
    _normalize_ground_contact_estimation(cfg)
    cfg.setdefault("output", {})
    cfg["output"]["run_id"] = "auto"
    cfg["output"].pop("overwrite_existing", None)

    # Offset cache for this capsule + robot.
    cfg.setdefault("offsets", {})
    cfg["offsets"]["file"] = "offsets.json"

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
    automatic_robot = _robot_foot_to_ground_offset(cfg)
    robot_height = float(
        automatic_robot
        if automatic_robot is not None
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
        "robot_source": "robot_collision_geometry" if automatic_robot is not None else "config_fallback",
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
    cfg["output"]["pkl_name"] = f"{run_id}_primary.pkl"
    cfg["output"]["save_diagnostics_csv"] = True

    cfg.setdefault("offsets", {})
    cfg["offsets"]["file"] = "offsets.json"

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
            update_job(
                job_id,
                status="failed",
                message="Retarget failed",
                error="\n".join(log_lines[-120:]),
            )
            return

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

    primary_path = run / f"{req.run_id}_primary.pkl"
    if not primary_path.exists() and not (run / "primary.pkl").exists():
        raise HTTPException(
            status_code=409,
            detail=f"Primary PKL not found for run {req.run_id}",
        )

    # Main follows the same run-snapshot rule as Primary. Persistent defaults
    # are only used while opening a new form, never after the Run request.
    cfg = deepcopy(req.config)
    _normalize_ground_contact_estimation(cfg)
    cfg["config_name"] = str(cfg.get("config_name") or "Robot Standard Main")
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
    cfg.setdefault("offsets", {})
    cfg["offsets"]["file"] = f"{main_id}_offsets.json"
    cfg_path = main_result_json_path(
        req.capsule_id, req.robot_variant, req.run_id, main_id, req.user_id
    )
    atomic_write_json(cfg_path, cfg)

    script = repo_root() / "server" / "retarget" / "main_retarget.py"
    cmd = [sys.executable, "-u", str(script), str(cfg_path)]

    main_path = cfg_path.parent / f"{main_id}_main.pkl"
    job_id = uuid.uuid4().hex
    with JOBS_LOCK:
        initial_total = selected_frame_count(cfg)
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
        args=(job_id, main_id, cfg_path.parent.parent, cmd, None, overwrite),
        daemon=True,
    )
    thread.start()
    return JOBS[job_id]


@router.get("/main/file")
def get_main_file(
    capsule_id: str,
    run_id: str,
    main_id: str = "legacy",
    kind: Literal["csv", "pkl"] = "csv",
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
        cfg = load_json(default_config_path(
            capsule_id, robot_variant, user_id
        ))
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

        # Primary/Main viewer data are generated directly from PKL on request.
        # No per-stage *_viewer.bin file is created.
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
                pkl_path = stage_dir / f"{file_id}_{stage}.pkl"
                if stage == "primary" and not pkl_path.exists():
                    legacy = run_dir / "primary.pkl"
                    if legacy.exists():
                        pkl_path = legacy
                if not pkl_path.exists():
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
                sources[stage] = {
                    "label": label,
                    "kind": "retarget",
                    "url": (
                        f"/api/retarget/viewer/file/retarget"
                        f"?capsule_id={capsule_id}&robot_variant={robot_variant}"
                        f"&run_id={run_id}&stage={stage}&user_id={user_id}"
                        f"&main_id={main_id}"
                        f"&rev={pkl_path.stat().st_mtime_ns}"
                    ),
                    "file": pkl_path.name,
                    "storage": "pkl_on_demand",
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
            detail=f"{stage} PKL viewer conversion failed: {type(exc).__name__}: {exc}",
        ) from exc
    return Response(
        content=payload,
        media_type="application/octet-stream",
        headers={
            "Cache-Control": "public, max-age=31536000, immutable",
            "X-MEVA-Viewer-Source": f"{stage}.pkl",
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
    cfg["output"]["pkl_name"] = f"{run_id}_primary.pkl"
    cfg["output"]["save_diagnostics_csv"] = True

    # Keep offset cache short and robot-level.
    cfg.setdefault("offsets", {})
    cfg["offsets"]["file"] = "offsets.json"

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
