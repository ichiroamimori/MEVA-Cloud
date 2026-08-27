"""Main task diagnostics derived from main_target.npz and final main.npz."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

try:
    from .foot_support import load_foot_support_definition, support_point_metadata
    from .motion_io import quaternion_error_rotvec
    from .motion_viewer import build_motion_viewer_data, write_motion_viewer
except ImportError:
    from foot_support import load_foot_support_definition, support_point_metadata
    from motion_io import quaternion_error_rotvec
    from motion_viewer import build_motion_viewer_data, write_motion_viewer


def _mapped_link(config: dict[str, Any], source: str, fallback: str) -> str:
    for mapping in config.get("mappings", []):
        if str(mapping.get("source_segment")) == source:
            return str(mapping["target_link"])
    return fallback


def write_main_viewer(
    *, path: Path, repo_root: Path, config: dict[str, Any],
    motion: dict[str, Any], target: dict[str, Any], result: Any,
    frame_status: np.ndarray | None = None,
    frame_errors: list[dict[str, Any]] | None = None,
    main_rows: list[dict[str, Any]] | None = None,
) -> Path:
    data = build_motion_viewer_data(
        repo_root=repo_root, config=config, motion=motion, result=result,
        stage="main",
    )
    mappings = list(config.get("mappings", []))
    target_link_names = [str(value) for value in target["link_names"]]
    mapping_link_names = [str(item["target_link"]) for item in mappings]
    if target_link_names != mapping_link_names:
        raise ValueError("Main Viewer target Mapping order does not match Main config")
    link_indices = [data.link_index[name] for name in target_link_names]

    orientation_target = np.asarray(target["link_target_quat"], dtype=np.float32)
    orientation_result = data.arrays["link_quat"][:, link_indices].copy()
    orientation_rotvec = quaternion_error_rotvec(
        orientation_result.astype(np.float64), orientation_target.astype(np.float64)
    ).astype(np.float32)

    pelvis_link = _mapped_link(config, "Pelvis", "pelvis")
    pelvis_result = data.arrays["link_pos"][:, data.link_index[pelvis_link]][:, None, :].copy()
    pelvis_target = np.asarray(target["pelvis_target_xyz"], dtype=np.float32)[:, None, :]
    position_residual = (pelvis_target - pelvis_result).astype(np.float32)

    support_definition = load_foot_support_definition(data.model, config)
    foot_support_names: list[str] = []
    support_positions: list[np.ndarray] = []

    def rotate_wxyz(quaternion: np.ndarray, points: np.ndarray) -> np.ndarray:
        vector = quaternion[:, None, 1:]
        scalar = quaternion[:, None, :1]
        base = np.broadcast_to(points[None, :, :], (len(quaternion), len(points), 3))
        first = np.cross(vector, base)
        return base + 2.0 * (scalar * first + np.cross(vector, first))

    for side in ("left", "right"):
        definition = support_definition.sides[side]
        saved_names = [str(value) for value in target[f"{side}_geom_names"]]
        if definition.display_names != saved_names:
            raise ValueError(f"Main Viewer {side} Foot Support Point order mismatch")
        link_index = data.link_index[definition.body_name]
        support_positions.append(
            data.arrays["link_pos"][:, link_index, None, :]
            + rotate_wxyz(
                data.arrays["link_quat"][:, link_index],
                definition.local_positions,
            )
        )
        foot_support_names.extend(saved_names)
    foot_support_position = np.concatenate(support_positions, axis=1).astype(np.float32)
    foot_support_target = np.column_stack((
        np.asarray(target["left_geom_target_z"], dtype=np.float32),
        np.asarray(target["right_geom_target_z"], dtype=np.float32),
    ))
    foot_support_result = foot_support_position[:, :, 2]
    foot_support_residual = (foot_support_target - foot_support_result).astype(np.float32)

    pelvis_index = data.link_index[pelvis_link]
    direction_target = np.stack((
        target["left_pelvis_to_foot_direction"],
        target["right_pelvis_to_foot_direction"],
    ), axis=1).astype(np.float32)
    direction_result = np.empty_like(direction_target)
    for side_index, side in enumerate(("left", "right")):
        foot_index = data.link_index[support_definition.sides[side].body_name]
        value = data.arrays["link_pos"][:, foot_index] - data.arrays["link_pos"][:, pelvis_index]
        norm = np.linalg.norm(value, axis=1, keepdims=True)
        direction_result[:, side_index] = value / np.maximum(norm, 1e-12)
    direction_cosine = np.clip(
        np.sum(direction_target * direction_result, axis=2), -1.0, 1.0
    )

    arrays = {
        "orientation_target_quat": orientation_target,
        "orientation_result_quat": orientation_result,
        "orientation_residual_rotvec_rad": orientation_rotvec,
        "orientation_residual_angle_rad": np.linalg.norm(
            orientation_rotvec, axis=2
        ).astype(np.float32),
        "position_target_xyz_m": pelvis_target,
        "position_result_xyz_m": pelvis_result,
        "position_residual_xyz_m": position_residual,
        "position_residual_norm_m": np.linalg.norm(
            position_residual, axis=2
        ).astype(np.float32),
        "foot_support_point_pos": foot_support_position,
        "foot_support_target_z_m": foot_support_target,
        "foot_support_result_z_m": foot_support_result,
        "foot_support_residual_z_m": foot_support_residual,
        # Legacy aliases keep existing Viewer clients able to read new BINs.
        "foot_geom_target_z_m": foot_support_target,
        "foot_geom_result_z_m": foot_support_result,
        "foot_geom_residual_z_m": foot_support_residual,
        "gcp_left_raw": np.asarray(
            target.get("left_gcp_raw", target["left_gcp_corrected"]), dtype=np.float32
        ),
        "gcp_right_raw": np.asarray(
            target.get("right_gcp_raw", target["right_gcp_corrected"]), dtype=np.float32
        ),
        "gcp_left_smoothed": np.asarray(
            target.get("left_gcp_smoothed", target["left_gcp_corrected"]), dtype=np.float32
        ),
        "gcp_right_smoothed": np.asarray(
            target.get("right_gcp_smoothed", target["right_gcp_corrected"]), dtype=np.float32
        ),
        "gcp_left_corrected": np.asarray(target["left_gcp_corrected"], dtype=np.float32),
        "gcp_right_corrected": np.asarray(target["right_gcp_corrected"], dtype=np.float32),
        "foot_support_min_point_index": np.column_stack((
            np.asarray(target["left_min_geom_index"], dtype=np.int32),
            np.asarray(target["right_min_geom_index"], dtype=np.int32),
        )),
        "pelvis_to_foot_target_direction": direction_target,
        "pelvis_to_foot_result_direction": direction_result,
        "pelvis_to_foot_residual_angle_rad": np.arccos(direction_cosine).astype(np.float32),
    }
    rows = list(main_rows or [])
    if len(rows) == len(motion["frame"]):
        arrays.update({
            "gcp_left_used": np.asarray(
                [row.get("Left_used_GCP", row.get("Left_corrected_GCP", 0.0)) for row in rows],
                dtype=np.float32,
            ),
            "gcp_right_used": np.asarray(
                [row.get("Right_used_GCP", row.get("Right_corrected_GCP", 0.0)) for row in rows],
                dtype=np.float32,
            ),
            "support_state": np.asarray(
                [row.get("Support_State", 0) for row in rows], dtype=np.uint8
            ),
            "foot_contact_correction_strength": np.column_stack((
                np.asarray([row.get("Left_ground_contact_correction_strength_a", 0.0) for row in rows]),
                np.asarray([row.get("Right_ground_contact_correction_strength_a", 0.0) for row in rows]),
            )).astype(np.float32),
            "foot_contact_delta_z_m": np.column_stack((
                np.asarray([row.get("Left_ground_contact_delta_z", 0.0) for row in rows]),
                np.asarray([row.get("Right_ground_contact_delta_z", 0.0) for row in rows]),
            )).astype(np.float32),
        })
    if frame_status is None:
        frame_status = np.zeros(len(motion["frame"]), dtype=np.uint8)
    frame_status = np.asarray(frame_status, dtype=np.uint8)
    if frame_status.shape != (len(motion["frame"]),):
        raise ValueError("Main Viewer frame_status length mismatch")
    arrays["frame_status"] = frame_status
    arrays["frame_valid"] = (frame_status < 2).astype(np.uint8)
    errors = list(frame_errors or [])
    metadata = {
        "main_id": str(config.get("main_id", "")),
        "artifact_generation_id": str(config.get("artifact_generation_id", "")),
        "mappings": mappings,
        "orientation_mappings": [{
            "source_segment": item["source_segment"],
            "target_link": item["target_link"],
            "orientation_mode": item.get("orientation_mode", "full"),
        } for item in mappings],
        "position_mappings": [{
            "source_segment": "Pelvis", "target_link": pelvis_link,
            "position_axes": ["x", "y", "z"],
        }],
        "foot_support_points": support_point_metadata(support_definition),
        "foot_support_point_names": foot_support_names,
        "foot_support_task_axes": ["z"] * len(foot_support_names),
        "foot_geom_task_names": foot_support_names,
        "foot_geom_task_axes": ["z"] * len(foot_support_names),
        "gcp_sides": ["left", "right"],
        "support_state_codes": {
            "0": "FLYING", "1": "SINGLE_LEFT", "2": "SINGLE_RIGHT",
            "3": "DOUBLE_LEFT_MAIN", "4": "DOUBLE_RIGHT_MAIN",
        },
        "pelvis_to_foot_sides": ["left", "right"],
        "main_target_schema_version": str(np.asarray(target["schema_version"]).item()),
        "run_status": "partial" if errors else "complete",
        "failed_frame_count": int(np.count_nonzero(frame_status >= 2)),
        "frame_status_codes": {
            "0": "valid", "1": "not converged",
            "2": "solver error", "3": "not computed",
        },
        "frame_errors": errors,
    }
    return write_motion_viewer(path=path, data=data, arrays=arrays, metadata=metadata)
