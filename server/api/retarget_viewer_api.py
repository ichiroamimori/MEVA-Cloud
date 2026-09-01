from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, Response

from server.retarget_config_store import (
    ConfigStoreError,
    load_config as load_shared_config,
    runtime_config as merge_runtime_config,
)
from server.api.retarget_artifact_api import (
    MAIN_ID_RE,
    RUN_RE,
    _main_primary_frame_count,
    _validate_main_artifact_set,
    default_config_path,
    load_json,
    resolve_main_result_dir,
    robot_dir,
    run_config_path,
)
from server.api.retarget_config_api import _capsule_runtime_context, _shared_error
from server.api.retarget_robot_api import (
    _registered_variant,
    _runtime_robot_config,
    repo_root,
)


router = APIRouter()


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

