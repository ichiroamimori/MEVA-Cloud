"""Shared Primary/Main motion diagnostic and Viewer BIN generation."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
from copy import deepcopy

import mujoco
import numpy as np

try:
    from .foot_support import (
        load_foot_support_definition, support_point_metadata,
        support_point_world_positions,
    )
    from .robot_model_info import collision_pair_descriptors, joint_descriptors
    from .validation_data import joint_limit_severity, self_collision_severity
    from .viewer_data import write_viewer_bin
except ImportError:
    from foot_support import (
        load_foot_support_definition, support_point_metadata,
        support_point_world_positions,
    )
    from robot_model_info import collision_pair_descriptors, joint_descriptors
    from validation_data import joint_limit_severity, self_collision_severity
    from viewer_data import write_viewer_bin


SCHEMA_VERSION = "1.0"


@dataclass
class MotionViewerData:
    model: mujoco.MjModel
    link_names: list[str]
    geom_names: list[str]
    joint_names: list[str]
    link_index: dict[str, int]
    geom_index: dict[int, int]
    metadata: dict[str, Any]
    arrays: dict[str, np.ndarray]


def _name(model, obj, index: int, fallback: str) -> str:
    return mujoco.mj_id2name(model, obj, index) or f"{fallback}_{index}"


def _qpos(model, motion: dict[str, Any], frame: int, hinges: list[dict]) -> np.ndarray:
    q = model.qpos0.copy()
    free = next(
        jid for jid in range(model.njnt)
        if model.jnt_type[jid] == mujoco.mjtJoint.mjJNT_FREE
    )
    address = int(model.jnt_qposadr[free])
    q[address:address + 3] = motion["root_pos"][frame]
    rotation = np.asarray(motion["root_rot"][frame], dtype=np.float64)
    order = str(motion["root_rot_order"])
    q[address + 3:address + 7] = rotation[[3, 0, 1, 2]] if order == "xyzw" else rotation
    for index, joint in enumerate(hinges):
        q[int(joint["qpos_address"])] = motion["dof_pos"][frame, index]
    return q


def _limit_values(config: dict, key: str, joint_names: list[str]) -> np.ndarray:
    cfg = dict(config.get(key, {}))
    default_key = "default_rad_s" if "velocity" in key else "default_rad_s2"
    default = float(cfg.get(default_key, 0.0))
    overrides = dict(cfg.get("overrides", {}))
    values = []
    for name in joint_names:
        raw = overrides.get(name, default)
        if isinstance(raw, dict):
            raw = raw.get("max_rad_s" if "velocity" in key else "max_rad_s2", default)
        values.append(float(raw))
    return np.asarray(values, dtype=np.float64)


def _motion_limit_severity(values: np.ndarray, limits: np.ndarray) -> np.ndarray:
    ratio = np.divide(
        np.abs(values), limits[None, :],
        out=np.zeros_like(values, dtype=np.float64),
        where=limits[None, :] > 0.0,
    )
    # Display scale only: zero=blue, configured limit=yellow, 2x limit=red.
    return np.clip(np.rint(ratio * 191.0), 0.0, 255.0).astype(np.uint8)


def build_motion_viewer_data(
    *, repo_root: Path, config: dict[str, Any], motion: dict[str, Any],
    result: Any, stage: str,
) -> MotionViewerData:
    """Compute fields shared by Primary and Main from that stage's final motion."""
    xml_value = Path(str(config["robot"]["mjcf"]))
    xml_path = (repo_root / xml_value).resolve() if not xml_value.is_absolute() else xml_value.resolve()
    model = mujoco.MjModel.from_xml_path(str(xml_path))
    data = mujoco.MjData(model)
    all_joints = joint_descriptors(model)
    hinges = [item for item in all_joints if item["type"] == int(mujoco.mjtJoint.mjJNT_HINGE)]
    joint_names = [str(item["name"]) for item in hinges]
    body_ids = np.arange(1, model.nbody, dtype=np.int32)
    link_names = [_name(model, mujoco.mjtObj.mjOBJ_BODY, int(i), "body") for i in body_ids]
    geom_ids = np.arange(model.ngeom, dtype=np.int32)
    geom_names = [_name(model, mujoco.mjtObj.mjOBJ_GEOM, int(i), "geom") for i in geom_ids]
    pairs = collision_pair_descriptors(model, xml_path)
    support_definition = load_foot_support_definition(
        model, config, required=False
    )
    n = len(motion["frame"])

    link_pos = np.empty((n, len(body_ids), 3), dtype=np.float32)
    link_quat = np.empty((n, len(body_ids), 4), dtype=np.float32)
    geom_pos = np.empty((n, len(geom_ids), 3), dtype=np.float32)
    joint_actual = np.asarray(motion["dof_pos"], dtype=np.float32)
    joint_margin = np.empty_like(joint_actual)
    joint_severity = np.empty_like(joint_actual, dtype=np.uint8)
    collision_distance = np.empty((n, len(pairs)), dtype=np.float32)
    collision_severity = np.empty((n, len(pairs)), dtype=np.uint8)
    foot_support_position = (
        np.empty((n, 8, 3), dtype=np.float32)
        if support_definition is not None else None
    )

    joint_cfg = dict(config.get("joint_limit_avoidance", {}))
    default_zone = float(joint_cfg.get("default", {}).get("limit_zone_percent", 10.0))
    joint_metadata = []
    for joint in hinges:
        override = dict(joint_cfg.get("overrides", {}).get(joint["name"], {}))
        zone_percent = float(override.get("limit_zone_percent", default_zone))
        lo, hi = map(float, joint["range"])
        joint_metadata.append({
            "name": joint["name"], "lower_limit_rad": lo, "upper_limit_rad": hi,
            "limit_zone_percent": zone_percent,
            "limit_zone_rad": max(0.0, (hi - lo) * zone_percent / 100.0),
        })
    collision_zone = float(config.get("self_collision_avoidance", {}).get(
        "damping", {}
    ).get("limit_zone_m", 0.005))

    for frame_index in range(n):
        data.qpos[:] = _qpos(model, motion, frame_index, hinges)
        mujoco.mj_forward(model, data)
        link_pos[frame_index] = data.xpos[body_ids]
        link_quat[frame_index] = data.xquat[body_ids]
        geom_pos[frame_index] = data.geom_xpos[geom_ids]
        if support_definition is not None and foot_support_position is not None:
            foot_support_position[frame_index] = np.concatenate([
                support_point_world_positions(
                    data, support_definition.sides[side]
                )
                for side in ("left", "right")
            ], axis=0)
        for joint_index, info in enumerate(joint_metadata):
            value = float(joint_actual[frame_index, joint_index])
            margin = min(value - info["lower_limit_rad"], info["upper_limit_rad"] - value)
            joint_margin[frame_index, joint_index] = margin
            joint_severity[frame_index, joint_index] = joint_limit_severity(
                margin, info["limit_zone_rad"]
            )
        for pair_index, pair in enumerate(pairs):
            distance = float(mujoco.mj_geomDistance(
                model, data, int(pair["geom_a_id"]), int(pair["geom_b_id"]),
                1e6, np.empty(6, dtype=float),
            ))
            collision_distance[frame_index, pair_index] = distance
            collision_severity[frame_index, pair_index] = self_collision_severity(
                distance, collision_zone
            )

    diagnostics = list(result.diagnostics)
    ik_iterations = np.asarray([row[3] for row in diagnostics], dtype=np.int32)
    ik_converged = np.asarray([row[4] for row in diagnostics], dtype=np.uint8)
    ik_final_delta = np.radians(
        np.asarray([row[5] for row in diagnostics], dtype=np.float64)
    ).astype(np.float32)
    max_iterations = int(config.get("solver", {}).get("max_iterations_per_frame", 20))
    ik_reached_max = ((ik_iterations >= max_iterations) & (ik_converged == 0)).astype(np.uint8)
    velocity_limits = _limit_values(config, "interframe_joint_velocity_limit", joint_names)
    acceleration_limits = _limit_values(config, "interframe_joint_acceleration_limit", joint_names)

    arrays = {
        "frame": motion["frame"], "time_s": motion["time_s"],
        "source_frame_float": motion["source_frame_float"],
        "source_frame_nearest": motion["source_frame_nearest"],
        "root_pos": motion["root_pos"], "root_rot": motion["root_rot"],
        "dof_pos": motion["dof_pos"], "joint_angle_rad": motion["dof_pos"],
        "joint_velocity_rad_s": motion["dof_vel"],
        "joint_acceleration_rad_s2": motion["dof_acc"],
        "joint_velocity_severity": _motion_limit_severity(motion["dof_vel"], velocity_limits),
        "joint_acceleration_severity": _motion_limit_severity(motion["dof_acc"], acceleration_limits),
        "ik_iterations": ik_iterations, "ik_converged": ik_converged,
        "ik_final_joint_delta_rad": ik_final_delta,
        "ik_reached_max_iterations": ik_reached_max,
        "joint_limit_actual_rad": joint_actual,
        "joint_limit_margin_rad": joint_margin,
        "joint_limit_severity": joint_severity,
        "self_collision_signed_distance_m": collision_distance,
        "self_collision_severity": collision_severity,
        "link_pos": link_pos, "link_quat": link_quat, "geom_pos": geom_pos,
        "body_parent_index": np.asarray([
            int(model.body_parentid[int(body_id)] - 1)
            if int(model.body_parentid[int(body_id)]) > 0 else -1
            for body_id in body_ids
        ], dtype=np.int32),
    }
    if foot_support_position is not None:
        arrays["foot_support_point_pos"] = foot_support_position
    metadata = {
        "schema_version": SCHEMA_VERSION,
        "kind": "retarget", "stage": stage, "fps": float(motion["fps"]),
        "frames": n, "frame_count": n, "source_frame_start": 0,
        "source_frame_stop": n, "source_frame_step": 1,
        "quaternion_order": "wxyz", "root_rot_order": str(motion["root_rot_order"]),
        "joint_names": joint_names, "link_names": link_names,
        "geom_names": geom_names,
        "collision_pair_names": [str(item["label"]) for item in pairs],
        "collision_pair_metadata": pairs, "joint_limit_metadata": joint_metadata,
        "joint_velocity_limits_rad_s": velocity_limits.tolist(),
        "joint_acceleration_limits_rad_s2": acceleration_limits.tolist(),
        "severity_lut_anchors": [[0,"blue"],[64,"cyan"],[128,"green"],[191,"yellow"],[223,"orange"],[255,"red"]],
    }
    skeleton = config.get("robot", {}).get("ui", {}).get("skeleton")
    if isinstance(skeleton, dict) and isinstance(skeleton.get("parts"), list):
        skeleton = deepcopy(skeleton)
        terminal_semantics = (
            config.get("robot", {}).get("retargeting", {}).get("terminal_semantics", {})
        )
        for part in skeleton["parts"]:
            if not isinstance(part, dict) or part.get("pattern") != "semantic_axis":
                continue
            semantic = terminal_semantics.get(str(part.get("body") or ""), {})
            primary = semantic.get("primary") if isinstance(semantic, dict) else None
            if not isinstance(primary, list) or len(primary) != 3:
                raise ValueError(
                    "semantic_axis requires terminal_semantics.primary: "
                    f"stage={stage}, body={part.get('body')}, model={xml_path}"
                )
            part["direction_local"] = [float(value) for value in primary]
        referenced_bodies = set(skeleton.get("hide_parent_edges", []))
        for part in skeleton["parts"]:
            if not isinstance(part, dict):
                continue
            if part.get("body"):
                referenced_bodies.add(str(part["body"]))
            for anchor in part.get("anchors", []):
                if isinstance(anchor, dict) and anchor.get("body"):
                    referenced_bodies.add(str(anchor["body"]))
        missing_bodies = sorted(referenced_bodies.difference(link_names))
        if missing_bodies:
            raise ValueError(
                "Robot skeleton definition references bodies missing from the compiled "
                f"model: stage={stage}, bodies={missing_bodies}, model={xml_path}"
            )
        # The manifest is the source of truth; each BIN keeps the exact drawing
        # definition used by this Run so historical artifacts remain reproducible.
        metadata["robot_skeleton"] = skeleton
    if support_definition is not None:
        metadata["foot_support_points"] = support_point_metadata(
            support_definition
        )
        metadata["foot_support_point_names"] = [
            name
            for side in ("left", "right")
            for name in support_definition.sides[side].display_names
        ]
    return MotionViewerData(
        model=model, link_names=link_names, geom_names=geom_names,
        joint_names=joint_names,
        link_index={name: index for index, name in enumerate(link_names)},
        geom_index={int(geom_id): index for index, geom_id in enumerate(geom_ids)},
        metadata=metadata, arrays=arrays,
    )


def write_motion_viewer(
    *, path: Path, data: MotionViewerData,
    arrays: dict[str, np.ndarray] | None = None,
    metadata: dict[str, Any] | None = None,
) -> Path:
    """Write the common self-contained container with optional task fields."""
    combined_arrays = {**data.arrays, **(arrays or {})}
    combined_metadata = {**data.metadata, **(metadata or {})}
    units = {
        "time_s": "s", "root_pos": "m", "joint_angle_rad": "rad",
        "joint_velocity_rad_s": "rad/s", "joint_acceleration_rad_s2": "rad/s^2",
        "ik_final_joint_delta_rad": "rad", "orientation_residual_rotvec_rad": "rad",
        "orientation_residual_angle_rad": "rad", "orientation_axis_error_rad": "rad",
        "position_target_xyz_m": "m",
        "position_result_xyz_m": "m", "position_residual_xyz_m": "m",
        "position_residual_norm_m": "m", "joint_limit_actual_rad": "rad",
        "joint_limit_margin_rad": "rad", "self_collision_signed_distance_m": "m",
        "link_pos": "m", "geom_pos": "m", "foot_geom_target_z_m": "m",
        "foot_geom_result_z_m": "m", "foot_geom_residual_z_m": "m",
        "foot_support_point_pos": "m", "foot_support_target_z_m": "m",
        "foot_support_result_z_m": "m", "foot_support_residual_z_m": "m",
        "foot_contact_delta_z_m": "m",
        "pelvis_to_foot_residual_angle_rad": "rad",
        "pelvis_to_foot_meva_direction": "1",
    }
    combined_metadata["array_metadata"] = {
        name: {
            "unit": units.get(name, "1"),
            "semantic_description": name.replace("_", " "),
        }
        for name in combined_arrays
    }
    return write_viewer_bin(path, combined_metadata, combined_arrays)
