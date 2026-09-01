# -*- coding: utf-8 -*-
"""Build and validate the compact, solver-facing Main target artifact."""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

import mujoco
import numpy as np

from main_calibration import (
    _free_joint_qpos_addr,
    _hinge_joints,
    _qpos_from_primary_frame,
    preprocess_gcp,
)
from primary_target import load_primary_target
try:
    from server.retarget.robot_runtime_definition import BodyPointDefinition
except ModuleNotFoundError:  # Direct execution from server/retarget.
    from robot_runtime_definition import BodyPointDefinition
from mapping_tasks import quat_rotate_vec


SCHEMA_VERSION = "1.2"


@dataclass(frozen=True)
class MainTargetBuildResult:
    path: Path
    base_z: dict[str, np.ndarray]
    selected_raw_gcp: dict[str, np.ndarray]
    smoothed_gcp: dict[str, np.ndarray]


def _saved_common_scale(primary: dict, fallback: float) -> float:
    metadata = dict(primary.get("metadata", {}))
    diagnostics = dict(metadata.get(
        "primary_post_diagnostics", metadata.get("main_input_diagnostics", {})
    ))
    value = dict(diagnostics.get("pelvis_foot_scale_g", {})).get("common", fallback)
    value = float(value)
    if not np.isfinite(value) or value <= 0.0:
        raise ValueError("Primary Pelvis-Foot common scale is unavailable")
    return value


def _target_z(base_z: np.ndarray, corrected_gcp: np.ndarray) -> np.ndarray:
    """Apply one common Z translation per foot, preserving its four-point shape."""
    base_z = np.asarray(base_z, dtype=np.float64)
    corrected_gcp = np.asarray(corrected_gcp, dtype=np.float64)
    minimum = np.min(base_z, axis=1)
    target_minimum = (1.0 - corrected_gcp) * np.maximum(minimum, 0.0)
    return base_z + (target_minimum - minimum)[:, None]


def build_main_target(
    *,
    output_path: Path,
    primary: dict,
    primary_target_path: Path,
    model: mujoco.MjModel,
    cfg: dict,
    pelvis_reference: BodyPointDefinition,
    contact_geometry: dict,
    mapping_offset_path: Path,
    fallback_common_scale: float,
    meva_foot_to_ground_offset_m: float,
    robot_foot_to_ground_offset_m: float,
    gcp_smoothing_ms: float,
    gcp_min_offset: float,
    gcp_max_offset: float,
    gcp_power_number: float,
) -> MainTargetBuildResult:
    """Generate only the final values consumed as Main IK targets."""
    source = load_primary_target(primary_target_path)
    n = len(np.asarray(primary["root_pos"]))
    target_fps = float(np.asarray(source["target_fps"]).item())
    if len(source["frame"]) != n:
        raise ValueError("Primary motion and primary_target.npz frame counts differ")
    primary_fps = float(primary.get("fps", target_fps))
    if not np.isclose(primary_fps, target_fps):
        raise ValueError("Primary motion and primary_target.npz sampling rates differ")

    scale = _saved_common_scale(primary, fallback_common_scale)
    free_qadr = _free_joint_qpos_addr(model)
    hinges = _hinge_joints(model)
    pelvis_link = pelvis_reference.body_name
    pelvis_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, pelvis_link)
    if pelvis_id < 0:
        raise KeyError(f"Pelvis body not found: {pelvis_link}")

    link_names = [str(mapping["target_link"]) for mapping in cfg.get("mappings", [])]
    if len(link_names) != len(set(link_names)) or not link_names:
        raise ValueError("Main Mapping target links must be non-empty and unique")
    link_ids = [
        mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, name)
        for name in link_names
    ]
    if any(body_id < 0 for body_id in link_ids):
        raise KeyError("A configured Main Mapping body is missing from the Robot model")
    offset_asset = json.loads(mapping_offset_path.read_text(encoding="utf-8"))
    offset_details = dict(offset_asset.get("details", {}))
    link_orientation_mode = np.asarray([
        str(mapping.get("orientation_mode", "full"))
        for mapping in cfg.get("mappings", [])
    ])
    link_axis_local = np.zeros((len(link_names), 3), dtype=np.float64)
    for index, (name, mode) in enumerate(zip(link_names, link_orientation_mode)):
        if mode == "axis":
            axis = np.asarray(
                offset_details.get(name, {}).get("robot_long_axis_link_local"),
                dtype=np.float64,
            )
            if axis.shape != (3,) or not np.all(np.isfinite(axis)):
                raise ValueError(f"Axis Mapping metadata is missing for {name}")
            norm = float(np.linalg.norm(axis))
            if norm <= 1e-12:
                raise ValueError(f"Axis Mapping metadata is degenerate for {name}")
            link_axis_local[index] = axis / norm
        elif mode != "full":
            raise ValueError(f"Unsupported Main orientation mode: {mode}")
    link_target_quat = np.empty((n, len(link_names), 4), dtype=np.float64)
    pelvis_quat = np.empty((n, 4), dtype=np.float64)
    pelvis_to_foot_direction = {
        side: np.empty((n, 3), dtype=np.float64) for side in ("left", "right")
    }
    meva_pelvis = np.asarray(source["pelvis_xyz_m"], dtype=np.float64)
    meva_pelvis_to_foot_direction: dict[str, np.ndarray] = {}
    for side in ("left", "right"):
        meva_foot = np.asarray(source[f"{side}_foot_xyz_m"], dtype=np.float64)
        direction = meva_foot - meva_pelvis
        norm = np.linalg.norm(direction, axis=1, keepdims=True)
        if np.any(~np.isfinite(norm)) or np.any(norm <= 1e-12):
            raise ValueError(f"MEVA {side} Pelvis-to-Foot direction is degenerate")
        meva_pelvis_to_foot_direction[side] = direction / norm
    relative_z = {
        side: np.empty((n, 4), dtype=np.float64) for side in ("left", "right")
    }
    data = mujoco.MjData(model)
    foot_links = {
        side: str(contact_geometry[side]["body_name"])
        for side in ("left", "right")
    }
    foot_ids = {
        side: mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, name)
        for side, name in foot_links.items()
    }
    if any(body_id < 0 for body_id in foot_ids.values()):
        raise KeyError("Mapped Foot body is missing from the Robot model")
    for i in range(n):
        data.qpos[:] = _qpos_from_primary_frame(model, primary, i, free_qadr, hinges)
        mujoco.mj_forward(model, data)
        pelvis_quat[i] = data.xquat[pelvis_id]
        link_target_quat[i] = data.xquat[link_ids]
        pelvis_position = pelvis_reference.world_position(model, data)
        for side in ("left", "right"):
            foot_z = float(data.xpos[foot_ids[side], 2])
            direction = data.xpos[foot_ids[side]] - pelvis_position
            direction_norm = float(np.linalg.norm(direction))
            if not np.isfinite(direction_norm) or direction_norm <= 1e-12:
                raise ValueError(f"Primary {side} Pelvis-to-Foot direction is degenerate")
            pelvis_to_foot_direction[side][i] = direction / direction_norm
            relative_z[side][i] = (
                np.asarray(contact_geometry[side]["xyz"][i], dtype=np.float64)[:, 2]
                - foot_z
            )

    pelvis_norm = np.linalg.norm(pelvis_quat, axis=1, keepdims=True)
    if np.any(pelvis_norm <= 1e-12):
        raise ValueError("Primary Pelvis orientation contains a zero quaternion")
    pelvis_quat /= pelvis_norm
    link_norm = np.linalg.norm(link_target_quat, axis=2, keepdims=True)
    if np.any(link_norm <= 1e-12):
        raise ValueError("Primary Mapping target contains a zero quaternion")
    link_target_quat /= link_norm

    pelvis_reference_xyz = np.zeros((n, 3), dtype=np.float64)
    pelvis_reference_xyz[:, 2] = (
        robot_foot_to_ground_offset_m
        + scale * (
            np.asarray(source["pelvis_z_m"], dtype=np.float64)
            - meva_foot_to_ground_offset_m
        )
    )
    pelvis_xyz = np.asarray([
        pelvis_reference_xyz[index]
        - quat_rotate_vec(pelvis_quat[index], pelvis_reference.local_position)
        for index in range(n)
    ], dtype=np.float64)
    base_z: dict[str, np.ndarray] = {}
    min_index: dict[str, np.ndarray] = {}
    selected_raw: dict[str, np.ndarray] = {}
    smoothed: dict[str, np.ndarray] = {}
    corrected: dict[str, np.ndarray] = {}
    geom_target_z: dict[str, np.ndarray] = {}
    for side in ("left", "right"):
        meva_foot_z = np.asarray(source[f"{side}_foot_z_m"], dtype=np.float64)
        robot_foot_base_z = (
            robot_foot_to_ground_offset_m
            + scale * (meva_foot_z - meva_foot_to_ground_offset_m)
        )
        base_z[side] = robot_foot_base_z[:, None] + relative_z[side]
        min_index[side] = np.argmin(base_z[side], axis=1).astype(np.int64)
        labels = list(contact_geometry[side]["labels"])
        ca = np.asarray(source[f"gcp_{side}_ca"], dtype=np.float64)
        ff = np.asarray(source[f"gcp_{side}_ff"], dtype=np.float64)
        is_ca = np.asarray([labels[index].startswith("CA") for index in min_index[side]])
        selected_raw[side] = np.where(is_ca, ca, ff)
        smoothed[side], corrected[side], _ = preprocess_gcp(
            selected_raw[side],
            sampling_rate_hz=target_fps,
            smoothing_ms=gcp_smoothing_ms,
            min_offset=gcp_min_offset,
            max_offset=gcp_max_offset,
            power_number=gcp_power_number,
        )
        corrected[side] = np.clip(corrected[side], 0.0, 1.0)
        geom_target_z[side] = _target_z(base_z[side], corrected[side])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        output_path,
        schema_version=np.asarray(SCHEMA_VERSION),
        target_fps=np.asarray(target_fps, dtype=np.float64),
        frame=np.arange(n, dtype=np.int64),
        time_s=np.arange(n, dtype=np.float64) / target_fps,
        source_frame_float=np.asarray(
            primary.get("source_frame_float", np.arange(n)), dtype=np.float64
        ),
        source_frame_nearest=np.asarray(
            primary.get("source_frame_indices", np.arange(n)), dtype=np.int64
        ),
        pelvis_target_xyz=pelvis_xyz,
        pelvis_reference_target_xyz=pelvis_reference_xyz,
        pelvis_reference_body=np.asarray(pelvis_reference.body_name),
        pelvis_reference_local_position=np.asarray(
            pelvis_reference.local_position, dtype=np.float64
        ),
        pelvis_target_quat=pelvis_quat,
        quaternion_order=np.asarray("wxyz"),
        link_names=np.asarray(link_names),
        link_orientation_mode=link_orientation_mode,
        link_axis_local=link_axis_local,
        link_target_quat=link_target_quat,
        left_pelvis_to_foot_direction=pelvis_to_foot_direction["left"],
        right_pelvis_to_foot_direction=pelvis_to_foot_direction["right"],
        left_meva_pelvis_to_foot_direction=(
            meva_pelvis_to_foot_direction["left"]
        ),
        right_meva_pelvis_to_foot_direction=(
            meva_pelvis_to_foot_direction["right"]
        ),
        left_gcp_corrected=corrected["left"],
        right_gcp_corrected=corrected["right"],
        left_gcp_raw=selected_raw["left"],
        right_gcp_raw=selected_raw["right"],
        left_gcp_smoothed=smoothed["left"],
        right_gcp_smoothed=smoothed["right"],
        left_min_geom_index=min_index["left"],
        right_min_geom_index=min_index["right"],
        left_geom_target_z=geom_target_z["left"],
        right_geom_target_z=geom_target_z["right"],
        left_geom_names=np.asarray(contact_geometry["left"]["display_names"]),
        right_geom_names=np.asarray(contact_geometry["right"]["display_names"]),
        left_support_local_position=np.asarray(
            contact_geometry["left"]["local_positions"], dtype=np.float64
        ),
        right_support_local_position=np.asarray(
            contact_geometry["right"]["local_positions"], dtype=np.float64
        ),
        left_support_body=np.asarray(contact_geometry["left"]["body_name"]),
        right_support_body=np.asarray(contact_geometry["right"]["body_name"]),
    )
    load_main_target(output_path, expected_frames=n, expected_fps=primary_fps)
    return MainTargetBuildResult(output_path, base_z, selected_raw, smoothed)


def load_main_target(
    path: Path, *, expected_frames: int | None = None, expected_fps: float | None = None
) -> dict[str, Any]:
    with np.load(path, allow_pickle=False) as archive:
        target = {key: archive[key].copy() for key in archive.files}
    n = len(target["frame"])
    expected_shapes = {
        "time_s": (n,), "source_frame_float": (n,),
        "source_frame_nearest": (n,), "pelvis_target_xyz": (n, 3),
        "pelvis_target_quat": (n, 4), "left_gcp_corrected": (n,),
        "right_gcp_corrected": (n,), "left_min_geom_index": (n,),
        "right_min_geom_index": (n,), "left_geom_target_z": (n, 4),
        "right_geom_target_z": (n, 4), "left_geom_names": (4,),
        "right_geom_names": (4,),
    }
    optional_shapes = {
        "left_gcp_raw": (n,), "right_gcp_raw": (n,),
        "left_gcp_smoothed": (n,), "right_gcp_smoothed": (n,),
        "left_support_local_position": (4, 3),
        "right_support_local_position": (4, 3),
        "left_support_body": (), "right_support_body": (),
        "pelvis_reference_target_xyz": (n, 3),
        "pelvis_reference_body": (),
        "pelvis_reference_local_position": (3,),
        "left_meva_pelvis_to_foot_direction": (n, 3),
        "right_meva_pelvis_to_foot_direction": (n, 3),
    }
    if "link_names" not in target or target["link_names"].ndim != 1:
        raise ValueError("Invalid main target field link_names")
    link_count = len(target["link_names"])
    expected_shapes.update({
        "link_orientation_mode": (link_count,),
        "link_axis_local": (link_count, 3),
        "link_target_quat": (n, link_count, 4),
        "left_pelvis_to_foot_direction": (n, 3),
        "right_pelvis_to_foot_direction": (n, 3),
    })
    for key, shape in expected_shapes.items():
        if key not in target or target[key].shape != shape:
            raise ValueError(f"Invalid main target field {key}: expected {shape}")
    for key, shape in optional_shapes.items():
        if key in target and target[key].shape != shape:
            raise ValueError(f"Invalid main target field {key}: expected {shape}")
    reference_keys = {
        "pelvis_reference_target_xyz",
        "pelvis_reference_body",
        "pelvis_reference_local_position",
    }
    present_reference_keys = reference_keys.intersection(target)
    if present_reference_keys and present_reference_keys != reference_keys:
        raise ValueError("Main target Pelvis Reference fields are incomplete")
    if expected_frames is not None and n != expected_frames:
        raise ValueError("Main target frame count does not match Primary")
    fps = float(np.asarray(target["target_fps"]).item())
    if expected_fps is not None and not np.isclose(fps, expected_fps):
        raise ValueError("Main target sampling rate does not match Primary")
    if str(np.asarray(target["quaternion_order"]).item()) != "wxyz":
        raise ValueError("Main target quaternion order must be wxyz")
    if not np.all(np.isfinite(target["pelvis_target_xyz"])):
        raise ValueError("Main Pelvis target contains NaN/Inf")
    if "pelvis_reference_target_xyz" in target and not np.all(np.isfinite(
        target["pelvis_reference_target_xyz"]
    )):
        raise ValueError("Main Pelvis Reference target contains NaN/Inf")
    if not np.allclose(np.linalg.norm(target["pelvis_target_quat"], axis=1), 1.0, atol=1e-7):
        raise ValueError("Main Pelvis target quaternion is not normalized")
    if not np.allclose(
        np.linalg.norm(target["link_target_quat"], axis=2), 1.0, atol=1e-7
    ):
        raise ValueError("Main Link target quaternion is not normalized")
    for side in ("left", "right"):
        if not np.allclose(
            np.linalg.norm(target[f"{side}_pelvis_to_foot_direction"], axis=1),
            1.0,
            atol=1e-7,
        ):
            raise ValueError(f"Main {side} Pelvis-to-Foot direction is not normalized")
        meva_key = f"{side}_meva_pelvis_to_foot_direction"
        if meva_key in target and not np.allclose(
            np.linalg.norm(target[meva_key], axis=1), 1.0, atol=1e-7
        ):
            raise ValueError(
                f"MEVA {side} Pelvis-to-Foot direction is not normalized"
            )
    for side in ("left", "right"):
        gcp = target[f"{side}_gcp_corrected"]
        indices = target[f"{side}_min_geom_index"]
        geom_z = target[f"{side}_geom_target_z"]
        if np.any((gcp < 0.0) | (gcp > 1.0)):
            raise ValueError(f"{side} corrected GCP is outside [0, 1]")
        if np.any((indices < 0) | (indices > 3)):
            raise ValueError(f"{side} minimum GEOM index is outside [0, 3]")
        if not np.all(np.isfinite(geom_z)):
            raise ValueError(f"{side} GEOM target Z contains NaN/Inf")
    return target
