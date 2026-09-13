from __future__ import annotations

import json
import math
import os
import re
import shutil
import sys
import threading
import time
import uuid
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Literal

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
    release_id_reservation,
    robot_dir,
    run_config_path,
    selected_frame_count,
)
from server.api.retarget_config_api import (
    _capsule_runtime_context,
    _normalize_ground_contact_estimation,
)
from server.api.retarget_robot_api import (
    _registered_variant,
    _runtime_robot_config,
    repo_root,
)
from server.remote_ik_client import (
    RemoteIKError,
    configured_backend,
    execute_remote_job,
)
from server.managed_process import (
    ManagedProcessCancelled,
    ManagedProcessTimeout,
    run_managed_process,
)
from server.retarget_config_store import workspace_root
from server.retarget.motion_io import load_motion, save_gmr_pickle
from server.retarget.viewer_data import generate_meva_viewer_bin, read_viewer_bin


router = APIRouter()
PROGRESS_RE = re.compile(r"^\[(\d+)/(\d+)\] frame (\d+)")
JOB_ID_RE = re.compile(r"^[0-9a-f]{32}$")
CLOUD_JOB_ROOT = workspace_root() / "runtime" / "retarget_jobs"
CLOUD_JOB_TTL_SEC = float(
    os.environ.get("MEVA_CLOUD_IK_JOB_TTL_SEC", str(7 * 24 * 3600))
)
LOCAL_JOB_TIMEOUT_SEC = float(os.environ.get("MEVA_IK_JOB_TIMEOUT_SEC", "7200"))
JOB_CANCEL_EVENTS: dict[str, threading.Event] = {}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _persist_job_unlocked(job_id: str) -> None:
    if not JOB_ID_RE.fullmatch(job_id) or job_id not in JOBS:
        return
    CLOUD_JOB_ROOT.mkdir(parents=True, exist_ok=True)
    atomic_write_json(CLOUD_JOB_ROOT / f"{job_id}.json", JOBS[job_id])


def _restore_cloud_jobs() -> None:
    if not CLOUD_JOB_ROOT.is_dir():
        return
    cutoff = datetime.now(timezone.utc) - timedelta(seconds=CLOUD_JOB_TTL_SEC)
    for path in CLOUD_JOB_ROOT.glob("*.json"):
        if not JOB_ID_RE.fullmatch(path.stem):
            continue
        try:
            job = load_json(path)
            if job.get("job_id") != path.stem:
                continue
            if job.get("status") in {"queued", "running", "cancelling"}:
                job.update({
                    "status": "failed",
                    "message": "MEVA Cloud restarted during Retargeting",
                    "error": "cloud_restarted: MEVA Cloud restarted during Retargeting",
                    "error_code": "cloud_restarted",
                    "finished_at": _utc_now(),
                })
                atomic_write_json(path, job)
            finished_at = str(job.get("finished_at") or "")
            if finished_at and CLOUD_JOB_TTL_SEC > 0:
                finished = datetime.fromisoformat(finished_at)
                if finished.tzinfo is None:
                    finished = finished.replace(tzinfo=timezone.utc)
                if finished < cutoff:
                    path.unlink(missing_ok=True)
                    continue
            JOBS[path.stem] = job
            JOB_CANCEL_EVENTS[path.stem] = threading.Event()
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            continue


def update_job(job_id: str, **values: Any) -> None:
    with JOBS_LOCK:
        if job_id in JOBS:
            JOBS[job_id].update(values)
            _persist_job_unlocked(job_id)


def _register_job(job_id: str, job: dict[str, Any]) -> None:
    with JOBS_LOCK:
        JOBS[job_id] = job
        JOB_CANCEL_EVENTS[job_id] = threading.Event()
        _persist_job_unlocked(job_id)


_restore_cloud_jobs()

class RunRequest(BaseModel):
    capsule_id: str
    robot_variant: str = "g1_29dof"
    user_id: str = "local_user"
    source: str = "new"  # "new" or existing run ID
    overwrite: bool = False
    config: dict[str, Any]
    iteration_diagnostics: bool = False
    note: str = Field(default="", max_length=2000)
    backend: Literal["local_python", "remote_python"] | None = None

class MainRunRequest(BaseModel):
    capsule_id: str
    run_id: str
    main_id: str = "new"
    robot_variant: str = "g1_29dof"
    user_id: str = "local_user"
    config: dict[str, Any]
    note: str = Field(default="", max_length=2000)
    backend: Literal["local_python", "remote_python"] | None = None


@router.get("/compute-backend")
def get_compute_backend():
    return {
        "default_backend": configured_backend(),
        "available_backends": ["local_python", "remote_python"],
    }

def _prepare_run(
    req: RunRequest, job_id: str,
) -> tuple[str, Path, list[str], Path, bool, Path | None]:
    rdir = robot_dir(
        req.capsule_id,
        req.robot_variant,
        req.user_id,
    )
    rdir.mkdir(parents=True, exist_ok=True)

    reservation: Path | None = None
    if req.source == "new":
        run_id, reservation = allocate_run_id(rdir, job_id)
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
    try:
        variant = _registered_variant(req.robot_variant)
        cfg = _runtime_robot_config(deepcopy(req.config), variant)
        runtime_context = _capsule_runtime_context(
            req.capsule_id, req.robot_variant, req.user_id,
        )
        cfg["capsule_id"] = runtime_context["capsule_id"]
        cfg["source"] = deepcopy(runtime_context["source"])
        cfg["note"] = req.note.strip()
        _normalize_ground_contact_estimation(cfg)
        cfg.setdefault("output", {})
        cfg["output"]["run_id"] = run_id
        cfg["output"]["overwrite_existing"] = overwrite
        cfg["output"].pop("pkl_name", None)
        cfg["output"]["save_diagnostics_csv"] = bool(req.iteration_diagnostics)
        cfg["output"]["save_debug_artifacts"] = bool(req.iteration_diagnostics)

        # Local and Remote Primary use the same self-contained MEVA BIN.  The
        # Capsule metadata remains the source of the original CSV/BVH path,
        # while the compute boundary takes its Capsule identity and motion
        # payload from this versioned container.
        meva_bin = generate_meva_viewer_bin(
            repo_root(), req.capsule_id, cfg, req.user_id,
        )
        bin_header, _ = read_viewer_bin(meva_bin)
        if str(bin_header.get("capsule_id") or "") != req.capsule_id:
            raise HTTPException(status_code=409, detail="MEVA BIN Capsule ID mismatch")
        cfg["source"]["original_file"] = cfg["source"]["file"]
        try:
            bin_location = meva_bin.relative_to(repo_root()).as_posix()
        except ValueError:
            # Test/deployment workspace roots may be configured outside the
            # repository. pathlib resolves this absolute path correctly for
            # Local Compute; Remote packaging rewrites it to package://source.
            bin_location = str(meva_bin)
        cfg["source"]["file"] = bin_location
        frame_stop = cfg.get("frame_range", {}).get("stop")
        cfg["retarget_job"] = {
            "capsule_id": req.capsule_id,
            "start_frame": int(cfg.get("frame_range", {}).get("start", 0)),
            "end_frame": None if frame_stop is None else int(frame_stop) - 1,
            "config_id": cfg.get("config_id"),
            "config_version": cfg.get("version"),
            "target_robot": deepcopy(cfg.get("target_robot") or cfg.get("robot")),
        }

        request_path = rdir / f".{run_id}.{job_id}.request-config.json"
        atomic_write_json(request_path, cfg)

        cmd = [
            sys.executable, "-u", "-m", "server.retarget.primary_retarget",
            str(request_path),
        ]
        if req.iteration_diagnostics:
            cmd.append("--iteration-diagnostics")
    except Exception:
        release_id_reservation(reservation, job_id)
        raise

    return run_id, rdir, cmd, request_path, overwrite, reservation

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
    cancel_event = JOB_CANCEL_EVENTS.setdefault(job_id, threading.Event())
    try:
        if cancel_event.is_set():
            update_job(
                job_id, status="cancelled", message="Cancelled",
                finished_at=_utc_now(), error=None,
            )
            return
        with JOBS_LOCK:
            initial_total = JOBS.get(job_id, {}).get("total")
        update_job(
            job_id,
            status="running",
            started_at=_utc_now(),
            message=(
                f"Preparing... 0 / {initial_total} frames"
                if initial_total is not None
                else "Preparing..."
            ),
        )
        def process_line(line: str) -> None:
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

        returncode, log_lines = run_managed_process(
            cmd,
            cwd=repo_root(),
            cancel_event=cancel_event,
            timeout_sec=LOCAL_JOB_TIMEOUT_SEC,
            line_callback=process_line,
            log_limit=500,
        )

        if returncode != 0:
            files: list[str] = []
            if failure_finalize is not None:
                _, files = failure_finalize(log_lines)
            update_job(
                job_id,
                status="failed",
                message="Retarget failed",
                error="\n".join(log_lines[-120:]),
                error_code="ik_solver_failure",
                files=files,
                finished_at=_utc_now(),
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
            finished_at=_utc_now(),
        )
    except ManagedProcessCancelled:
        update_job(
            job_id, status="cancelled", message="Cancelled", error=None,
            finished_at=_utc_now(),
        )
    except ManagedProcessTimeout as exc:
        files: list[str] = []
        if failure_finalize is not None:
            try:
                _, files = failure_finalize([f"timeout: {exc}"])
            except Exception:
                files = []
        update_job(
            job_id, status="failed", message="Retarget timed out",
            error=f"timeout: {exc}", error_code="timeout", files=files,
            finished_at=_utc_now(),
        )
    except Exception as exc:
        update_job(
            job_id,
            status="failed",
            message="Retarget failed",
            error=f"{type(exc).__name__}: {exc}",
            error_code="unexpected_exception",
            finished_at=_utc_now(),
        )
    finally:
        if cleanup_path is not None:
            cleanup_path.unlink(missing_ok=True)
        if cleanup is not None:
            try:
                cleanup()
            except Exception:
                pass


def _replace_remote_primary_result(
    staging: Path, destination: Path, *, overwrite: bool,
) -> tuple[Path, list[str]]:
    if destination.exists():
        if not overwrite:
            raise FileExistsError(f"Retarget run already exists: {destination}")
        shutil.rmtree(destination)
    staging.replace(destination)
    files = sorted(path.name for path in destination.iterdir() if path.is_file())
    return destination, files


def _existing_primary_result(destination: Path) -> tuple[Path, list[str]]:
    if not destination.is_dir():
        raise FileNotFoundError(f"Remote Primary result was not received: {destination}")
    return destination, sorted(path.name for path in destination.iterdir() if path.is_file())


def _restore_received_source_path(received_config: Path, local_config: Path) -> None:
    received = json.loads(received_config.read_text(encoding="utf-8"))
    local = json.loads(local_config.read_text(encoding="utf-8"))
    if "source" in local:
        received["source"] = deepcopy(local["source"])
    atomic_write_json(received_config, received)


def _restore_remote_primary_config(destination: Path, request_path: Path) -> None:
    run_id = destination.name
    _restore_received_source_path(
        destination / f"{run_id}_primary_config.json", request_path,
    )


def _receive_remote_primary(
    staging: Path, destination: Path, request_path: Path, *, overwrite: bool,
) -> None:
    _replace_remote_primary_result(staging, destination, overwrite=overwrite)
    _restore_remote_primary_config(destination, request_path)


def _merge_remote_main_result(
    staging: Path, destination: Path, local_config: Path, main_id: str,
) -> None:
    received_configs = list(staging.glob("*_main_config.json"))
    if len(received_configs) != 1:
        raise RuntimeError("Remote Main result must contain one config snapshot")
    _restore_received_source_path(received_configs[0], local_config)
    motion_path = staging / f"{main_id}_main.npz"
    if not motion_path.is_file():
        raise RuntimeError("Remote Main result does not contain canonical motion NPZ")
    # Result extraction verifies but intentionally does not write Remote PKL.
    # Generate the compatibility PKL from the trusted canonical NPZ on Cloud.
    remote_pickle = staging / f"{main_id}_main.pkl"
    remote_pickle.unlink(missing_ok=True)
    save_gmr_pickle(remote_pickle, load_motion(motion_path))
    for path in staging.iterdir():
        if not path.is_file():
            raise RuntimeError(f"Unexpected nested Remote Main result: {path.name}")
        path.replace(destination / path.name)
    staging.rmdir()


def _run_remote_job(
    job_id: str,
    *,
    stage: str,
    config_path: Path,
    result_staging: Path,
    primary_directory: Path | None,
    iteration_diagnostics: bool,
    success_finalize: Callable[[], tuple[Path, list[str]]],
    failure_finalize: Callable[[list[str]], tuple[Path, list[str]]],
    receive_finalize: Callable[[], None] | None = None,
    cleanup: Callable[[], None] | None = None,
) -> None:
    remote_job_id: str | None = None
    cancel_event = JOB_CANCEL_EVENTS.setdefault(job_id, threading.Event())

    def status_update(remote: dict[str, Any]) -> None:
        nonlocal remote_job_id
        remote_job_id = str(remote.get("job_id") or remote_job_id or "") or None
        values = {
            key: remote[key]
            for key in ("progress", "processed", "total", "source_frame", "message")
            if key in remote
        }
        values["remote_job_id"] = remote_job_id
        values["remote_status"] = remote.get("status")
        update_job(job_id, **values)

    try:
        update_job(
            job_id, status="running", message="Uploading to Remote IK worker...",
            started_at=_utc_now(),
        )
        remote = execute_remote_job(
            repository_root=repo_root(),
            stage=stage,
            client_job_id=job_id,
            config_path=config_path,
            result_staging=result_staging,
            primary_directory=primary_directory,
            iteration_diagnostics=iteration_diagnostics,
            status_callback=status_update,
            cancel_event=cancel_event,
        )
        if receive_finalize is not None:
            receive_finalize()
        _, files = success_finalize()
        update_job(
            job_id,
            status="done",
            progress=1.0,
            message="Completed",
            files=files,
            remote_job_id=str(remote.get("job_id") or remote_job_id or "") or None,
            elapsed_sec=remote.get("elapsed_sec"),
            finished_at=_utc_now(),
        )
    except RemoteIKError as exc:
        if exc.code == "cancelled":
            update_job(
                job_id,
                status="cancelled",
                message="Cancelled",
                error=None,
                error_code=None,
                remote_job_id=exc.remote_job_id or remote_job_id,
                finished_at=_utc_now(),
            )
            return
        if result_staging.exists() and receive_finalize is not None:
            try:
                receive_finalize()
            except Exception:
                pass
        try:
            _, files = failure_finalize([f"{exc.code}: {exc}"])
        except Exception:
            files = []
        update_job(
            job_id,
            status="failed",
            message="Retarget failed",
            error=f"{exc.code}: {exc}",
            error_code=exc.code,
            remote_job_id=exc.remote_job_id or remote_job_id,
            files=files,
            finished_at=_utc_now(),
        )
    except Exception as exc:
        update_job(
            job_id,
            status="failed",
            message="Retarget failed",
            error=f"{type(exc).__name__}: {exc}",
            error_code="unexpected_exception",
            remote_job_id=remote_job_id,
            finished_at=_utc_now(),
        )
    finally:
        config_path.unlink(missing_ok=True)
        if result_staging.exists():
            shutil.rmtree(result_staging, ignore_errors=True)
        if cleanup is not None:
            try:
                cleanup()
            except Exception:
                pass

@router.post("/run-start")
def run_retarget_start(req: RunRequest):
    job_id = uuid.uuid4().hex
    run_id, rdir, cmd, request_path, overwrite, reservation = _prepare_run(req, job_id)

    backend = configured_backend(req.backend)

    initial_total = selected_frame_count(load_json(request_path))
    _register_job(job_id, {
            "job_id": job_id,
            "run_id": run_id,
            "stage": "primary",
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
            "backend": backend,
            "submitted_at": _utc_now(),
            "started_at": None,
            "finished_at": None,
        })

    def primary_failure_finalize(log_lines: list[str]) -> tuple[Path, list[str]]:
        if overwrite:
            # A failed Retry must leave the last complete published Run intact.
            return rdir / run_id, []
        return _publish_primary_failure_artifacts(
            rdir, run_id, request_path if request_path.exists() else local_request,
            log_lines,
        )

    local_staging: Path | None = None
    local_request = request_path
    if backend == "remote_python":
        remote_staging = rdir / f".{run_id}.{job_id}.remote-result"
        thread = threading.Thread(
            target=_run_remote_job,
            kwargs={
                "job_id": job_id,
                "stage": "primary",
                "config_path": request_path,
                "result_staging": remote_staging,
                "primary_directory": None,
                "iteration_diagnostics": req.iteration_diagnostics,
                "success_finalize": lambda: _existing_primary_result(rdir / run_id),
                "failure_finalize": primary_failure_finalize,
                "receive_finalize": lambda: _receive_remote_primary(
                    remote_staging, rdir / run_id, request_path, overwrite=overwrite,
                ),
                "cleanup": lambda: release_id_reservation(reservation, job_id),
            },
            daemon=True,
        )
    else:
        local_staging = rdir / f".{run_id}.{job_id}.local-staging"
        try:
            local_staging.mkdir(parents=False, exist_ok=False)
            local_request = local_staging / request_path.name
            request_path.replace(local_request)
            try:
                cmd[cmd.index(str(request_path))] = str(local_request)
            except ValueError:
                cmd.append(str(local_request))
        except Exception:
            request_path.unlink(missing_ok=True)
            shutil.rmtree(local_staging, ignore_errors=True)
            release_id_reservation(reservation, job_id)
            with JOBS_LOCK:
                JOBS.pop(job_id, None)
                JOB_CANCEL_EVENTS.pop(job_id, None)
                (CLOUD_JOB_ROOT / f"{job_id}.json").unlink(missing_ok=True)
            raise

        def cleanup_local_primary() -> None:
            shutil.rmtree(local_staging, ignore_errors=True)
            release_id_reservation(reservation, job_id)

        thread = threading.Thread(
            target=_run_job,
            args=(job_id, run_id, rdir, cmd, None, overwrite),
            kwargs={
                "finalize": lambda: _replace_remote_primary_result(
                    local_staging / run_id, rdir / run_id, overwrite=overwrite,
                ),
                "failure_finalize": primary_failure_finalize,
                "cleanup": cleanup_local_primary,
            },
            daemon=True,
        )
    try:
        thread.start()
    except Exception:
        request_path.unlink(missing_ok=True)
        if local_staging is not None:
            shutil.rmtree(local_staging, ignore_errors=True)
        release_id_reservation(reservation, job_id)
        with JOBS_LOCK:
            JOBS.pop(job_id, None)
            JOB_CANCEL_EVENTS.pop(job_id, None)
            (CLOUD_JOB_ROOT / f"{job_id}.json").unlink(missing_ok=True)
        raise

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
    job_id = uuid.uuid4().hex
    reservation: Path | None = None
    if req.main_id == "new":
        main_id, reservation = allocate_main_id(results_dir, req.run_id, job_id)
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
    cfg["artifact_generation_id"] = job_id
    frame_range = cfg.get("frame_range", {})
    frame_stop = frame_range.get("stop")
    cfg["retarget_job"] = {
        "capsule_id": req.capsule_id,
        "start_frame": int(frame_range.get("start", 0)),
        "end_frame": None if frame_stop is None else int(frame_stop) - 1,
        "config_id": cfg.get("config_id"),
        "config_version": cfg.get("version"),
        "target_robot": deepcopy(cfg.get("target_robot") or cfg.get("robot")),
    }
    expected_frames = _main_primary_frame_count(primary_path)
    final_dir = resolve_main_result_dir(
        req.capsule_id, req.robot_variant, req.run_id, main_id, req.user_id,
        must_exist=False,
    )
    staging_dir = run / f".{main_id}.{job_id}.staging"
    try:
        staging_dir.mkdir(parents=False, exist_ok=False)
        cfg_path = staging_dir / f"{main_id}_main_config.json"
        atomic_write_json(cfg_path, cfg)
    except Exception:
        release_id_reservation(reservation, job_id)
        raise

    def cleanup_main_job() -> None:
        _cleanup_main_staging(staging_dir, main_id)
        release_id_reservation(reservation, job_id)

    cmd = [
        sys.executable, "-u", "-m", "server.retarget.main_retarget",
        str(cfg_path),
    ]

    backend = configured_backend(req.backend)
    initial_total = expected_frames
    _register_job(job_id, {
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
            "backend": backend,
            "submitted_at": _utc_now(),
            "started_at": None,
            "finished_at": None,
        })

    if backend == "remote_python":
        remote_staging = staging_dir / ".remote-result"
        thread = threading.Thread(
            target=_run_remote_job,
            kwargs={
                "job_id": job_id,
                "stage": "main",
                "config_path": cfg_path,
                "result_staging": remote_staging,
                "primary_directory": run,
                "iteration_diagnostics": False,
                "receive_finalize": lambda: _merge_remote_main_result(
                    remote_staging, staging_dir, cfg_path, main_id,
                ),
                "success_finalize": lambda: _publish_main_artifact_set(
                    staging_dir, final_dir, main_id,
                    expected_frames=expected_frames, generation_id=job_id,
                ),
                "failure_finalize": lambda log_lines: _publish_main_failure_artifacts(
                    staging_dir, final_dir, main_id, log_lines,
                ),
                "cleanup": cleanup_main_job,
            },
            daemon=True,
        )
    else:
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
                "cleanup": cleanup_main_job,
            },
            daemon=True,
        )
    try:
        thread.start()
    except Exception:
        cleanup_main_job()
        with JOBS_LOCK:
            JOBS.pop(job_id, None)
            JOB_CANCEL_EVENTS.pop(job_id, None)
            (CLOUD_JOB_ROOT / f"{job_id}.json").unlink(missing_ok=True)
        raise
    return JOBS[job_id]

@router.get("/job/{job_id}")
def get_retarget_job(job_id: str):
    with JOBS_LOCK:
        job = JOBS.get(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found")
        return dict(job)


@router.post("/job/{job_id}/cancel")
def cancel_retarget_job(job_id: str):
    if not JOB_ID_RE.fullmatch(job_id):
        raise HTTPException(status_code=404, detail="Job not found")
    with JOBS_LOCK:
        job = JOBS.get(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found")
        if job.get("status") in {"done", "failed", "cancelled"}:
            return dict(job)
        JOB_CANCEL_EVENTS.setdefault(job_id, threading.Event()).set()
        if job.get("status") == "queued":
            job.update({
                "status": "cancelled",
                "message": "Cancelled",
                "error": None,
                "finished_at": _utc_now(),
            })
        else:
            job.update({"status": "cancelling", "message": "Cancelling..."})
        _persist_job_unlocked(job_id)
        return dict(job)

@router.post("/run")
def run_retarget(req: RunRequest):
    # Compatibility endpoint: use the same preparation, backend dispatch,
    # validation, and artifact finalization as the asynchronous UI endpoint.
    submitted = run_retarget_start(req)
    job_id = submitted["job_id"]
    while True:
        with JOBS_LOCK:
            job = dict(JOBS[job_id])
        if job["status"] not in {"queued", "running", "cancelling"}:
            break
        time.sleep(0.1)
    if job["status"] == "failed":
        raise HTTPException(
            status_code=500,
            detail={
                "code": job.get("error_code") or "RETARGET_FAILED",
                "run_id": job["run_id"],
                "message": job.get("error") or "Retarget failed",
            },
        )
    if job["status"] == "cancelled":
        raise HTTPException(
            status_code=409,
            detail={"code": "CANCELLED", "run_id": job["run_id"], "message": "Retarget cancelled"},
        )
    return {
        "ok": True,
        "run_id": job["run_id"],
        "overwritten": job.get("overwritten", False),
        "files": job.get("files", []),
        "stdout": "",
    }
