from __future__ import annotations

import json
import math
import re
import shutil
import subprocess
import sys
import threading
import uuid
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from server.api.retarget_artifact_api import (
    JOBS,
    JOBS_LOCK,
    MAIN_ID_RE,
    RUN_RE,
    _cleanup_main_staging,
    _main_primary_frame_count,
    _publish_main_artifact_set,
    _publish_main_failure_artifacts,
    _publish_primary_failure_artifacts,
    allocate_main_id,
    allocate_run_id,
    atomic_write_json,
    load_json,
    main_results_dir,
    resolve_main_result_dir,
    robot_dir,
    run_config_path,
    selected_frame_count,
)
from server.api.retarget_config_api import _normalize_ground_contact_estimation
from server.api.retarget_robot_api import (
    _registered_variant,
    _runtime_robot_config,
    repo_root,
)


router = APIRouter()
PROGRESS_RE = re.compile(r"^\[(\d+)/(\d+)\] frame (\d+)")


def update_job(job_id: str, **values: Any) -> None:
    with JOBS_LOCK:
        if job_id in JOBS:
            JOBS[job_id].update(values)

class RunRequest(BaseModel):
    capsule_id: str
    robot_variant: str = "g1_29dof"
    user_id: str = "local_user"
    source: str = "new"  # "new" or existing run ID
    overwrite: bool = False
    config: dict[str, Any]
    iteration_diagnostics: bool = False
    note: str = Field(default="", max_length=2000)

class MainRunRequest(BaseModel):
    capsule_id: str
    run_id: str
    main_id: str = "new"
    robot_variant: str = "g1_29dof"
    user_id: str = "local_user"
    config: dict[str, Any]
    note: str = Field(default="", max_length=2000)

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

    # User-editable fields come from the current UI request, while Robot model
    # metadata always comes from the current manifest.  Saved configs and open
    # browser pages may contain an older embedded robot.ui/retargeting snapshot;
    # allowing that snapshot through makes newly added skeleton/semantics data
    # impossible to use even after rerunning Primary.
    variant = _registered_variant(req.robot_variant)
    cfg = _runtime_robot_config(deepcopy(req.config), variant)
    cfg["note"] = req.note.strip()
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
    variant = _registered_variant(req.robot_variant)
    cfg = _runtime_robot_config(deepcopy(req.config), variant)
    cfg["note"] = req.note.strip()
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

@router.get("/job/{job_id}")
def get_retarget_job(job_id: str):
    with JOBS_LOCK:
        job = JOBS.get(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found")
        return dict(job)

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

    variant = _registered_variant(req.robot_variant)
    cfg = _runtime_robot_config(deepcopy(req.config), variant)
    cfg["note"] = req.note.strip()
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
