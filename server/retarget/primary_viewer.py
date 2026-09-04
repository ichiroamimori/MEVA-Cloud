"""Primary task-specific fields layered onto the shared motion Viewer BIN."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import mujoco
import numpy as np

try:
    from .mapping_tasks import (
        VIRTUAL_SOURCE_SEGMENTS, axis_angle_rad, normq, normalize_vec, qmul,
        quat_rotate_vec, quat_slerp,
    )
    from .motion_io import quaternion_error_rotvec
    from .motion_viewer import build_motion_viewer_data, write_motion_viewer
except ImportError:
    from mapping_tasks import (
        VIRTUAL_SOURCE_SEGMENTS, axis_angle_rad, normq, normalize_vec, qmul,
        quat_rotate_vec, quat_slerp,
    )
    from motion_io import quaternion_error_rotvec
    from motion_viewer import build_motion_viewer_data, write_motion_viewer


def _source_quaternion(target: dict[str, Any], frame: int, segment: str) -> np.ndarray:
    names = [str(value) for value in target["segment_names"]]
    index = {name: i for i, name in enumerate(names)}
    virtual = VIRTUAL_SOURCE_SEGMENTS.get(segment)
    if virtual is None:
        return normq(target["segment_quat"][frame, index[segment]])
    first, second, weight = virtual
    return quat_slerp(
        target["segment_quat"][frame, index[first]],
        target["segment_quat"][frame, index[second]],
        float(weight),
    )


def write_primary_viewer(
    *, path: Path, repo_root: Path, config: dict[str, Any],
    motion: dict[str, Any], target: dict[str, Any], result: Any,
    mapping_offsets: dict[str, Any], offset_details: dict[str, Any],
    post_diagnostics: Any | None,
    frame_status: np.ndarray | None = None,
    frame_errors: list[dict[str, Any]] | None = None,
) -> Path:
    data = build_motion_viewer_data(
        repo_root=repo_root, config=config, motion=motion, result=result,
        stage="primary",
    )
    mappings = list(config.get("mappings", []))
    mapping_link_indices = [data.link_index[str(item["target_link"])] for item in mappings]
    n = len(motion["frame"])
    orientation_target = np.empty((n, len(mappings), 4), dtype=np.float32)
    orientation_result = data.arrays["link_quat"][:, mapping_link_indices].copy()
    world = normq(config.get("world_alignment", {}).get(
        "offset_quaternion_wxyz", [1.0, 0.0, 0.0, 0.0]
    ))
    for frame_index in range(n):
        for mapping_index, mapping in enumerate(mappings):
            q_source = _source_quaternion(
                target, frame_index, str(mapping["source_segment"])
            )
            orientation_target[frame_index, mapping_index] = qmul(
                world, qmul(q_source, mapping_offsets[str(mapping["target_link"])])
            )
    orientation_rotvec = quaternion_error_rotvec(
        orientation_result.astype(np.float64), orientation_target.astype(np.float64)
    ).astype(np.float32)
    orientation_target_direction = np.full(
        (n, len(mappings), 3), np.nan, dtype=np.float32
    )
    orientation_result_direction = np.full_like(
        orientation_target_direction, np.nan
    )
    orientation_axis_error = np.full(
        (n, len(mappings)), np.nan, dtype=np.float32
    )
    for mapping_index, mapping in enumerate(mappings):
        if str(mapping.get("orientation_mode", "full")) != "axis":
            continue
        link = str(mapping["target_link"])
        axis = offset_details.get(link, {}).get("robot_long_axis_link_local")
        if axis is None:
            raise KeyError(
                "Axis mode requires robot_long_axis_link_local in the mapping "
                f"offset asset for Primary Viewer diagnostics: {link}"
            )
        axis = normalize_vec(axis)
        for frame_index in range(n):
            target_direction = normalize_vec(quat_rotate_vec(
                orientation_target[frame_index, mapping_index], axis
            ))
            result_direction = normalize_vec(quat_rotate_vec(
                orientation_result[frame_index, mapping_index], axis
            ))
            orientation_target_direction[frame_index, mapping_index] = target_direction
            orientation_result_direction[frame_index, mapping_index] = result_direction
            orientation_axis_error[frame_index, mapping_index] = axis_angle_rad(
                target_direction, result_direction
            )

    position_indices = [
        index for index, item in enumerate(mappings)
        if float(item.get("position_weight", 0.0)) > 0.0
        or str(item.get("source_segment")) == "Pelvis"
    ]
    position_result = data.arrays["link_pos"][
        :, [mapping_link_indices[i] for i in position_indices]
    ].copy()
    position_target = position_result.copy()
    initial_data = mujoco.MjData(data.model)
    keyframe_name = config.get("robot", {}).get("initial_keyframe")
    if keyframe_name:
        keyframe_id = mujoco.mj_name2id(
            data.model, mujoco.mjtObj.mjOBJ_KEY, str(keyframe_name)
        )
        if keyframe_id >= 0:
            mujoco.mj_resetDataKeyframe(data.model, initial_data, keyframe_id)
    mujoco.mj_forward(data.model, initial_data)
    for output_index, mapping_index in enumerate(position_indices):
        if str(mappings[mapping_index]["source_segment"]) == "Pelvis":
            body_id = mujoco.mj_name2id(
                data.model, mujoco.mjtObj.mjOBJ_BODY,
                str(mappings[mapping_index]["target_link"]),
            )
            position_target[:, output_index] = initial_data.xpos[body_id]
    position_residual = (position_target - position_result).astype(np.float32)

    arrays = {
        "orientation_target_quat": orientation_target,
        "orientation_result_quat": orientation_result,
        "orientation_residual_rotvec_rad": orientation_rotvec,
        "orientation_residual_angle_rad": np.linalg.norm(
            orientation_rotvec, axis=2
        ).astype(np.float32),
        "orientation_target_direction": orientation_target_direction,
        "orientation_result_direction": orientation_result_direction,
        "orientation_axis_error_rad": orientation_axis_error,
        "position_target_xyz_m": position_target,
        "position_result_xyz_m": position_result,
        "position_residual_xyz_m": position_residual,
        "position_residual_norm_m": np.linalg.norm(
            position_residual, axis=2
        ).astype(np.float32),
        "gcp_left_ff_raw": target["gcp_left_ff"],
        "gcp_left_ca_raw": target["gcp_left_ca"],
        "gcp_right_ff_raw": target["gcp_right_ff"],
        "gcp_right_ca_raw": target["gcp_right_ca"],
        "meva_pelvis_z_m": target["pelvis_z_m"],
        "meva_left_foot_z_m": target["left_foot_z_m"],
        "meva_right_foot_z_m": target["right_foot_z_m"],
    }
    if post_diagnostics is not None:
        arrays["primary_pelvis_target_z_m"] = post_diagnostics.pelvis_targets_z
        arrays["primary_pelvis_shift_z_m"] = post_diagnostics.pelvis_shifts_z
    if frame_status is None:
        frame_status = np.zeros(n, dtype=np.uint8)
        blocked = data.arrays.get("collision_backtracking_blocked")
        if blocked is not None:
            frame_status[np.asarray(blocked, dtype=bool)] = 4
    frame_status = np.asarray(frame_status, dtype=np.uint8)
    if frame_status.shape != (n,):
        raise ValueError("Primary Viewer frame_status length mismatch")
    arrays["frame_status"] = frame_status
    arrays["frame_valid"] = np.isin(frame_status, (0, 1)).astype(np.uint8)
    errors = list(frame_errors or [])
    metadata = {
        "mappings": mappings,
        "orientation_mappings": [{
            "source_segment": item["source_segment"],
            "target_link": item["target_link"],
            "orientation_mode": item.get("orientation_mode", "full"),
        } for item in mappings],
        "position_mappings": [{
            "source_segment": mappings[index]["source_segment"],
            "target_link": mappings[index]["target_link"],
        } for index in position_indices],
        "mapping_offsets_wxyz_by_link": {
            key: [float(x) for x in value] for key, value in mapping_offsets.items()
        },
        "world_alignment_wxyz": [float(x) for x in world],
        "orientation_axis_definition": "robot_long_axis_link_local",
        "run_status": "partial" if errors else "complete",
        "failed_frame_count": int(np.count_nonzero(frame_status >= 2)),
        "frame_status_codes": {
            "0": "valid", "1": "not converged",
            "2": "solver error", "3": "not computed",
            "4": "collision blocked",
        },
        "frame_errors": errors,
    }
    return write_motion_viewer(path=path, data=data, arrays=arrays, metadata=metadata)
