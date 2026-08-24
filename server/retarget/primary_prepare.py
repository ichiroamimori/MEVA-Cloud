# -*- coding: utf-8 -*-
"""Prepare Primary MEVA targets and Mink tasks for the common IK solver."""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import mujoco
import mink
import numpy as np

from ik_solver import (
    IKFrameSpec,
    PreparedIKFrame,
    SolverSettings,
    build_solver_settings,
    limit_start_ratio,
)
from mapping_tasks import (
    MappingTaskSet,
    RelativeDirectionTask,
    normalize_vec,
    quat_rotate_vec,
    read_meva,
    required_quaternion_columns,
)
from primary_target import load_primary_target


MEVA_HEADER_ROW_1BASED = 8
MEVA_SPATIAL_POSITION_COLUMN_INDICES = {
    "Pelvis": (334, 335, 336),
    "LeftFoot": (55, 56, 57),
    "RightFoot": (372, 373, 374),
}


@dataclass
class PrimaryPreparation:
    model: Any
    initial_configuration: Any
    frame_specs: list[IKFrameSpec]
    solver_settings: SolverSettings
    diagnostic_keys: list[str]
    source_frame_indices: list[int]
    source_frame_float: np.ndarray
    time_s: np.ndarray
    target_fps: float
    primary_target_path: Path
    step: int
    mapping_offsets: dict
    offset_path: Path
    joint_limit_zone_percent: float
    joint_limit_base_cost: float
    joint_limit_max_cost: float


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def resolve_fixed_position_keys(fields):
    max_index = max(
        idx for indices in MEVA_SPATIAL_POSITION_COLUMN_INDICES.values()
        for idx in indices
    )
    if len(fields) <= max_index:
        raise ValueError(
            f"MEVA CSV has only {len(fields)} columns; "
            f"spatial constraints require at least {max_index + 1}."
        )
    return {
        segment: tuple(fields[idx] for idx in indices)
        for segment, indices in MEVA_SPATIAL_POSITION_COLUMN_INDICES.items()
    }


def segpos_fixed(row, fixed_position_keys, segment: str):
    keys = fixed_position_keys[segment]
    pos = np.asarray([float(row[key]) for key in keys], dtype=float)
    if not np.all(np.isfinite(pos)):
        raise ValueError(f"bad fixed position for {segment}: {pos}")
    return pos


def mapped_link_for_source(cfg, source_segment: str) -> str:
    matches = [
        mapping["target_link"] for mapping in cfg.get("mappings", [])
        if mapping.get("source_segment") == source_segment
    ]
    if len(matches) != 1:
        raise ValueError(
            f"Spatial constraint requires exactly one mapping for "
            f"{source_segment!r}; found {matches}"
        )
    return matches[0]


def _solver_settings(model, cfg, output_frame_dt_s, iteration_diagnostics):
    return build_solver_settings(
        model=model,
        cfg=cfg,
        output_frame_dt_s=float(output_frame_dt_s),
        iteration_diagnostics=iteration_diagnostics,
    )


def prepare_primary(
    *, config_path: Path, cfg: dict, repo_root: Path,
    primary_target_path: Path,
    iteration_diagnostics: bool = False,
) -> PrimaryPreparation:
    csv_path = (repo_root / cfg["source"]["file"]).resolve()
    xml_path = (repo_root / cfg["robot"]["mjcf"]).resolve()
    bvh_path = (
        (repo_root / cfg["source"]["bvh"]).resolve()
        if cfg["source"].get("bvh") else csv_path.with_suffix(".bvh")
    )
    print("CSV    :", csv_path)
    print("BVH    :", bvh_path)
    print("MJCF   :", xml_path)

    tools_dir = Path(__file__).resolve().parent
    if str(tools_dir) not in sys.path:
        sys.path.insert(0, str(tools_dir))
    from check_offsets import compute_offsets
    mapping_offsets, offset_path, offsets_generated = compute_offsets(
        config_path,
        force=bool(cfg.get("offsets", {}).get("force_recompute", False)),
    )
    print("OFFSET :", offset_path, "(generated)" if offsets_generated else "(reused)")
    offset_asset = load_json(offset_path)
    offset_details = offset_asset.get("details", {})

    model = mujoco.MjModel.from_xml_path(str(xml_path))
    conf = mink.Configuration(model)
    key = cfg["robot"].get("initial_keyframe")
    try:
        conf.update_from_keyframe(key) if key else conf.update()
    except Exception:
        print("WARNING: keyframe not found; model default used")
        conf.update()

    target = load_primary_target(primary_target_path)
    target_fps = float(target["target_fps"])
    segment_names = [str(value) for value in target["segment_names"].tolist()]
    segment_quat = np.asarray(target["segment_quat"], dtype=np.float64)
    quaternion_order = str(target["quaternion_order"])
    if quaternion_order != "wxyz":
        raise ValueError("Primary Mapping currently requires wxyz target quaternions")
    pattern = cfg["source"]["quaternion_columns"]
    fields = [
        pattern.format(segment=segment, component=component)
        for segment in segment_names for component in "wxyz"
    ]
    rows = []
    for frame_index in range(len(target["frame"])):
        row = {}
        for segment_index, segment in enumerate(segment_names):
            for component_index, component in enumerate("wxyz"):
                row[pattern.format(segment=segment, component=component)] = float(
                    segment_quat[frame_index, segment_index, component_index]
                )
        rows.append(row)
    spatial_cfg = dict(cfg.get("spatial_constraints", {}))
    pelvis_foot_cfg = dict(spatial_cfg.get("pelvis_foot_direction", {}))
    pelvis_foot_enabled = bool(pelvis_foot_cfg.get("enabled", False))
    left_direction_cost = float(pelvis_foot_cfg.get("left_cost", 0.1))
    right_direction_cost = float(pelvis_foot_cfg.get("right_cost", 0.1))
    for side, value in (("left", left_direction_cost), ("right", right_direction_cost)):
        if not np.isfinite(value) or value < 0.0:
            raise ValueError(
                f"spatial_constraints.pelvis_foot_direction.{side}_cost "
                "must be a finite non-negative number"
            )
    target_positions = {
        "Pelvis": np.asarray(target["pelvis_xyz_m"], dtype=np.float64),
        "LeftFoot": np.asarray(target["left_foot_xyz_m"], dtype=np.float64),
        "RightFoot": np.asarray(target["right_foot_xyz_m"], dtype=np.float64),
    }
    required = required_quaternion_columns(cfg)
    missing = sorted(required - set(fields))
    if missing:
        raise KeyError("Missing MEVA columns:\n  " + "\n  ".join(missing))

    pelvis0 = conf.get_transform_frame_to_world("pelvis", "body").translation().copy()
    position_cost_by_link = {}
    for mapping in cfg["mappings"]:
        link = mapping["target_link"]
        position_cost = float(mapping["position_weight"])
        if link == "pelvis":
            position_cost = float(cfg["root"]["position_cost"])
        position_cost_by_link[link] = position_cost
    mapping_tasks = MappingTaskSet(
        model=model,
        cfg=cfg,
        mapping_offsets=mapping_offsets,
        offset_details=offset_details,
        position_cost_by_link=position_cost_by_link,
    )

    spatial_direction_tasks = {}
    if pelvis_foot_enabled:
        pelvis_link = mapped_link_for_source(cfg, "Pelvis")
        left_foot_link = mapped_link_for_source(cfg, "LeftFoot")
        right_foot_link = mapped_link_for_source(cfg, "RightFoot")
        if left_direction_cost > 0.0:
            spatial_direction_tasks["left"] = RelativeDirectionTask(
                pelvis_link, left_foot_link, cost=left_direction_cost,
                gain=1.0, lm_damping=float(cfg["solver"]["task_lm_damping"]),
            )
        if right_direction_cost > 0.0:
            spatial_direction_tasks["right"] = RelativeDirectionTask(
                pelvis_link, right_foot_link, cost=right_direction_cost,
                gain=1.0, lm_damping=float(cfg["solver"]["task_lm_damping"]),
            )

    world_alignment = mapping_tasks.world_alignment
    idxs = [int(value) for value in target["source_frame_nearest"].tolist()]
    source_float = np.asarray(target["source_frame_float"], dtype=np.float64)
    time_s = np.asarray(target["time_s"], dtype=np.float64)
    step = 1

    frame_specs = []
    for frame_index, source_frame in enumerate(idxs):
        def prepare_frame(configuration, frame_index=frame_index, source_frame=source_frame):
            row = rows[frame_index]
            prepared_mapping = mapping_tasks.prepare(
                row=row,
                configuration=configuration,
                source_frame=source_frame,
                position_targets_by_link={"pelvis": pelvis0},
            )
            active = list(prepared_mapping.tasks)

            if spatial_direction_tasks:
                pelvis_source_pos = target_positions["Pelvis"][frame_index]
                if "left" in spatial_direction_tasks:
                    direction = normalize_vec(
                        target_positions["LeftFoot"][frame_index]
                        - pelvis_source_pos
                    )
                    spatial_direction_tasks["left"].set_target(
                        quat_rotate_vec(world_alignment, direction)
                    )
                    active.append(spatial_direction_tasks["left"])
                if "right" in spatial_direction_tasks:
                    direction = normalize_vec(
                        target_positions["RightFoot"][frame_index]
                        - pelvis_source_pos
                    )
                    spatial_direction_tasks["right"].set_target(
                        quat_rotate_vec(world_alignment, direction)
                    )
                    active.append(spatial_direction_tasks["right"])

            return PreparedIKFrame(
                tasks=active,
                diagnostics=prepared_mapping.diagnostics,
            )

        frame_specs.append(IKFrameSpec(source_frame=source_frame, prepare=prepare_frame))

    settings = _solver_settings(model, cfg, 1.0 / target_fps, iteration_diagnostics)
    joint_default = dict(settings.joint_limit_avoidance.get("default", {}))
    joint_start = limit_start_ratio(joint_default)
    zone_percent = (1.0 - joint_start) * 50.0
    base_cost = float(joint_default.get("base_cost", 0.01))
    max_cost = float(joint_default.get("max_cost", 0.2))
    print(
        "TEMPORAL:",
        f"enabled, cost={settings.temporal_regularization_cost:g}"
        if settings.temporal_regularization_enabled and settings.temporal_regularization_cost > 0
        else "disabled",
    )
    print(
        "SPATIAL Pelvis->Foot direction:",
        f"enabled, left_cost={left_direction_cost:g}, right_cost={right_direction_cost:g}"
        if pelvis_foot_enabled else "disabled",
    )
    print(
        "JOINT LIMIT WEIGHT:",
        (
            f"enabled, zone={zone_percent:g}% each side, base_cost={base_cost:g}, "
            f"max_cost={max_cost:g}, per-iteration"
            if settings.joint_limit_avoidance.get("enabled", False) else "disabled"
        ),
    )
    print(
        "JOINT VELOCITY:",
        (
            f"enabled, default={settings.velocity_limit_default_rad_s / np.pi:g}*pi "
            f"rad/s ({settings.velocity_limit_default_rad_s:g} rad/s), "
            "output-frame hard limit"
            if settings.velocity_limit_enabled else "disabled"
        ),
    )
    return PrimaryPreparation(
        model=model,
        initial_configuration=conf,
        frame_specs=frame_specs,
        solver_settings=settings,
        diagnostic_keys=[m["target_link"] for m in cfg["mappings"]],
        source_frame_indices=idxs,
        source_frame_float=source_float,
        time_s=time_s,
        target_fps=target_fps,
        primary_target_path=primary_target_path,
        step=step,
        mapping_offsets=mapping_offsets,
        offset_path=offset_path,
        joint_limit_zone_percent=zone_percent,
        joint_limit_base_cost=base_cost,
        joint_limit_max_cost=max_cost,
    )
