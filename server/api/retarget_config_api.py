from __future__ import annotations

import json
import math
from copy import deepcopy
from pathlib import Path
from typing import Any, Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from server.capsule_identity import CAPSULE_ID_RE

from server.retarget_config_store import (
    archive_config,
    ConfigNameCollision,
    ConfigStoreError,
    list_configs as list_shared_configs,
    load_config as load_shared_config,
    overlay_main_mapping_parameters,
    publish_to_workspace,
    replace_xenoma_standard,
    runtime_config as merge_runtime_config,
    save_user_config,
    workspace_root,
)
from server.service_context import DEVELOPMENT_USER, can_replace_standard
from server.api.retarget_artifact_api import (
    MAIN_ID_RE,
    RUN_RE,
    _main_primary_frame_count,
    _validate_main_artifact_set,
    atomic_write_json,
    capsule_metadata,
    count_source_frames,
    default_config_path,
    list_main_result_ids,
    list_primary_run_ids,
    list_run_ids,
    load_json,
    main_default_config_path,
    main_result_json_path,
    main_results_dir,
    main_run_config_path,
    metadata_frame_count,
    resolve_main_result_dir,
    robot_dir,
    run_config_path,
)
from server.api.retarget_robot_api import (
    _assert_config_robot,
    _manifest_robot_foot_to_ground_offset,
    _registered_variant,
    _runtime_robot_config,
    _sole_geom_descriptors,
    _validate_retarget_config_or_http,
    repo_root,
)


router = APIRouter()


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
    selected_scope: Literal[
        "xenoma_standard", "personal", "workspace", "xenoma", "user"
    ] | None = None
    selected_filename: str | None = None
    overwrite: bool = False
    config: dict[str, Any]


class ConfigArchiveRequest(BaseModel):
    scope: Literal["personal", "workspace"]
    filename: str
    source_type: str = "meva"
    manufacturer: str = "unitree"
    robot_variant: str = "g1_29dof"
    user_id: str = "local_user"
    stage: Literal["primary", "main"] = "primary"


class AnalyticJointDetectionRequest(BaseModel):
    manufacturer: str = "unitree"
    robot_variant: str = "g1_29dof"
    config: dict[str, Any]


@router.post("/analytic-joint-target/detect")
def detect_analytic_joint_target(req: AnalyticJointDetectionRequest):
    variant = _registered_variant(req.robot_variant, manufacturer=req.manufacturer)
    _assert_config_robot(req.config, variant)
    runtime_config = _runtime_robot_config(req.config, variant)
    try:
        from server.retarget.analytic_joint_target import (
            detect_analytic_joint_clusters,
        )
        from server.retarget.robot_runtime_definition import (
            load_robot_runtime_definition_for_config,
        )
        runtime = load_robot_runtime_definition_for_config(
            repo_root(), runtime_config, validate_config=False
        )
        clusters = detect_analytic_joint_clusters(runtime, runtime_config)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Analytic Joint Target detection failed: {type(exc).__name__}: {exc}",
        ) from exc
    target_joints: list[str] = []
    axial_joints: list[str] = []
    for cluster in clusters:
        if not cluster.supported:
            continue
        target_joints.extend(
            cluster.joint_names if cluster.mapping_mode == "full"
            else cluster.joint_names[:2]
        )
        if cluster.mapping_mode == "axis" and cluster.axial_joint_index is not None:
            axial_joints.append(cluster.joint_names[cluster.axial_joint_index])
    return {
        "clusters": [cluster.metadata() for cluster in clusters],
        "target_joints": sorted(set(target_joints)),
        "axial_joints": sorted(set(axial_joints)),
    }

def _capsule_runtime_context(
    capsule_id: str,
    robot_variant: str,
    user_id: str = "local_user",
) -> dict[str, Any]:
    """Build only the Capsule-specific fields merged into a Shared Config."""
    if not CAPSULE_ID_RE.fullmatch(capsule_id) or user_id != "local_user":
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
    source_file = (capsule / relative_path).resolve()
    try:
        source_file.relative_to(capsule)
    except ValueError as exc:
        raise HTTPException(
            status_code=409, detail="Capsule MEVA source is unavailable"
        ) from exc
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


def _blank_primary_config(variant: Any) -> dict[str, Any]:
    """Robot-neutral editable Config used before a standard Config is installed."""
    retargeting = variant.variant.get("retargeting") or {}
    has_feet = isinstance(retargeting.get("foot_contacts"), dict)
    robot_ground_height = (
        _manifest_robot_foot_to_ground_offset({
            "robot": {
                "manufacturer": variant.manufacturer_id,
                "model": variant.robot_id,
                "variant": variant.variant_id,
            }
        }) if has_feet else 0.0
    )
    return {
        "schema_version": "1.0",
        "name": "New",
        "config_name": "New",
        "retarget_stage": "primary",
        "robot": {
            "manufacturer": variant.manufacturer_id,
            "model": variant.robot_id,
            "variant": variant.variant_id,
        },
        "root": {"position_mode": "keep_robot_initial", "position_cost": 100.0},
        "world_alignment": {"offset_quaternion_wxyz": [1.0, 0.0, 0.0, 0.0]},
        "mappings": [],
        "analytic_joint_target": {"joint_weights": {}},
        "joint_limit_avoidance": {
            "enabled": True, "enforce_hard_xml_limits": True,
            "default": {"limit_zone_percent": 5.0, "base_cost": 0.01,
                        "max_cost": 0.2, "exponent": 2},
            "overrides": {},
        },
        "solver": {
            "name": "daqp", "dt_s": 0.02, "global_damping": 1e-8,
            "task_lm_damping": 1e-6, "max_iterations_per_frame": 100,
            "convergence_joint_delta_deg": 0.01,
            "convergence_consecutive_iterations": 2,
        },
        "output": {"root_rot_order": "xyzw", "save_diagnostics_csv": False},
        "temporal_regularization": {"enabled": True, "cost": 0.1},
        "interframe_joint_velocity_limit": {
            "enabled": True, "default_rad_s": 3.0 * math.pi, "overrides": {},
        },
        "interframe_joint_acceleration_limit": {
            "enabled": False, "default_rad_s2": 220.0,
            "weight_at_2x_limit": 0.1, "overrides": {},
        },
        "spatial_constraints": {
            "pelvis_foot_direction": {
                "enabled": False, "left_cost": 0.3, "right_cost": 0.3,
            }
        },
        "ground_contact_estimation": {
            "geom_flatness_threshold_m": 0.005,
            "gcp_contact_threshold": 0.99,
            "robot_foot_ground_height_m": float(robot_ground_height or 0.0),
        },
        "self_collision_avoidance": {
            "enabled": False, "mode": "manual", "selected_pairs": [],
            "damping": {
                "limit_zone_m": 0.005,
                "penetration_scale_m": 0.005,
                "penetration_gain": 4.0,
                "base_cost": 0.01,
                "max_cost": 0.2,
                "gain": 0.2,
            },
        },
    }

@router.get("/configs")
def get_shared_configs(
    source_type: str = "meva",
    manufacturer: str = "unitree",
    robot_variant: str = "g1_29dof",
    user_id: str = "local_user",
    stage: Literal["primary", "main"] = "primary",
    include_archived: bool = False,
):
    _registered_variant(robot_variant, manufacturer=manufacturer)
    try:
        configs = list_shared_configs(
            source_type=source_type,
            manufacturer=manufacturer,
            robot_variant=robot_variant,
            user_id=user_id,
            stage=stage,
            include_archived=include_archived,
        )
    except ConfigStoreError as exc:
        raise _shared_error(exc) from exc
    return {"configs": [record.as_dict() for record in configs]}

@router.get("/configs/load")
def get_shared_config(
    capsule_id: str,
    scope: Literal[
        "xenoma_standard", "personal", "workspace", "xenoma", "user"
    ],
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
        if not CAPSULE_ID_RE.fullmatch(capsule_id) or user_id != "local_user":
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
            if not CAPSULE_ID_RE.fullmatch(req.capsule_id) or req.user_id != "local_user":
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


@router.post("/configs/publish-workspace")
def publish_shared_config_to_workspace(req: SharedConfigSaveRequest):
    variant = _registered_variant(req.robot_variant, manufacturer=req.manufacturer)
    _assert_config_robot(req.config, variant)
    _validate_retarget_config_or_http(variant, req.config)
    try:
        record, shared = publish_to_workspace(
            req.config,
            name=req.name,
            source_type=req.source_type,
            manufacturer=req.manufacturer,
            robot_variant=req.robot_variant,
            user_id=req.user_id,
            stage=req.stage,
        )
    except ConfigStoreError as exc:
        raise _shared_error(exc) from exc
    return {
        "ok": True,
        "shared_config": shared,
        "selection": record.as_dict(),
    }


@router.post("/configs/archive")
def archive_shared_config(req: ConfigArchiveRequest):
    _registered_variant(req.robot_variant, manufacturer=req.manufacturer)
    try:
        record = archive_config(
            scope=req.scope,
            filename=req.filename,
            source_type=req.source_type,
            manufacturer=req.manufacturer,
            robot_variant=req.robot_variant,
            user_id=req.user_id,
            stage=req.stage,
        )
    except ConfigStoreError as exc:
        raise _shared_error(exc) from exc
    return {"ok": True, "selection": record.as_dict()}


@router.post("/configs/replace-standard")
def replace_standard_config(req: SharedConfigSaveRequest):
    if not can_replace_standard(DEVELOPMENT_USER.role):
        raise HTTPException(status_code=403, detail="Replacing Xenoma Standard is not allowed")
    if req.selected_scope not in {"xenoma_standard", "xenoma"} or not req.selected_filename:
        raise HTTPException(status_code=400, detail="An active Xenoma Standard must be selected")
    variant = _registered_variant(req.robot_variant, manufacturer=req.manufacturer)
    _assert_config_robot(req.config, variant)
    _validate_retarget_config_or_http(variant, req.config)
    try:
        record, shared, archived_record = replace_xenoma_standard(
            req.config,
            name=req.name,
            filename=req.selected_filename,
            source_type=req.source_type,
            manufacturer=req.manufacturer,
            robot_variant=req.robot_variant,
            user_id=req.user_id,
            stage=req.stage,
        )
    except ConfigStoreError as exc:
        raise _shared_error(exc) from exc
    return {
        "ok": True,
        "shared_config": shared,
        "selection": record.as_dict(),
        "archived_selection": archived_record.as_dict(),
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
            # Do not leave the previous Robot's Config in the browser when a
            # newly registered Variant has no standard Config yet.
            default_config = merge_runtime_config(
                _blank_primary_config(variant),
                _capsule_runtime_context(capsule_id, robot_variant, user_id),
            )
            default_config = _runtime_robot_config(default_config, variant)
            _normalize_ground_contact_estimation(default_config)

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
        model_config = default_config or {
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

def _overlay_main_defaults(primary_cfg: dict[str, Any], overlay: dict[str, Any] | None) -> dict[str, Any]:
    cfg = deepcopy(primary_cfg)
    # Analytic Joint Targets belong exclusively to Primary.
    cfg.pop("analytic_joint_target", None)
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
        cfg["mappings"] = overlay_main_mapping_parameters(
            primary_cfg.get("mappings"), overlay.get("mappings")
        )
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

    variant = _registered_variant(robot_variant)
    primary_cfg = _runtime_robot_config(
        load_json(run_config_path(capsule_id, robot_variant, run_id, user_id)),
        variant,
    )
    legacy_cfg_path = main_run_config_path(capsule_id, robot_variant, run_id, user_id)
    default_main_cfg_path = main_default_config_path(capsule_id, robot_variant, user_id)
    results_dir = main_results_dir(capsule_id, robot_variant, run_id, user_id)
    main_ids = list_main_result_ids(results_dir, run_id)

    if main_id == "legacy":
        if not legacy_cfg_path.exists():
            raise HTTPException(status_code=404, detail="Legacy Main config not found")
        cfg = _runtime_robot_config(load_json(legacy_cfg_path), variant)
        main_path = run / f"{run_id}_main.pkl"
        main_csv_path = run / f"{run_id}_main_targets.csv"
    elif main_id == "new":
        overlay = load_json(default_main_cfg_path) if default_main_cfg_path.exists() else None
        cfg = _overlay_main_defaults(primary_cfg, overlay)
        # A Main note belongs to a concrete Main result, not its parent Primary.
        cfg["note"] = ""
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
        cfg = _runtime_robot_config(load_json(cfg_path), variant)
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
        # Foot support points are Robot Definition data.  Always resolve them
        # from the requested registered Variant, including when an old Main
        # snapshot predates embedded robot metadata.
        "sole_geoms": _sole_geom_descriptors(_runtime_robot_config(cfg, variant)),
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
    cfg.pop("note", None)
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
    cfg.pop("note", None)
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
