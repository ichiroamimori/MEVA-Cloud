"""Main task diagnostics derived from main_target.npz and final main.npz."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

try:
    from .main_calibration import foot_contact_geom_ids
    from .motion_io import quaternion_error_rotvec
    from .motion_viewer import build_motion_viewer_data, write_motion_viewer
except ImportError:
    from main_calibration import foot_contact_geom_ids
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

    foot_geom_ids: list[int] = []
    foot_geom_names: list[str] = []
    for side, source, fallback in (
        ("left", "LeftFoot", "left_ankle_roll_link"),
        ("right", "RightFoot", "right_ankle_roll_link"),
    ):
        ordered = foot_contact_geom_ids(
            data.model, _mapped_link(config, source, fallback)
        )
        ids = list(ordered.values())
        saved_names = [str(value) for value in target[f"{side}_geom_names"]]
        if len(ids) != len(saved_names):
            raise ValueError(f"Main Viewer {side} Foot GEOM count mismatch")
        foot_geom_ids.extend(ids)
        foot_geom_names.extend(saved_names)
    foot_geom_target = np.column_stack((
        np.asarray(target["left_geom_target_z"], dtype=np.float32),
        np.asarray(target["right_geom_target_z"], dtype=np.float32),
    ))
    foot_geom_result = np.column_stack([
        data.arrays["geom_pos"][:, data.geom_index[geom_id], 2]
        for geom_id in foot_geom_ids
    ]).astype(np.float32)
    foot_geom_residual = (foot_geom_target - foot_geom_result).astype(np.float32)

    pelvis_index = data.link_index[pelvis_link]
    direction_target = np.stack((
        target["left_pelvis_to_foot_direction"],
        target["right_pelvis_to_foot_direction"],
    ), axis=1).astype(np.float32)
    direction_result = np.empty_like(direction_target)
    for side_index, (source, fallback) in enumerate((
        ("LeftFoot", "left_ankle_roll_link"),
        ("RightFoot", "right_ankle_roll_link"),
    )):
        foot_index = data.link_index[_mapped_link(config, source, fallback)]
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
        "foot_geom_target_z_m": foot_geom_target,
        "foot_geom_result_z_m": foot_geom_result,
        "foot_geom_residual_z_m": foot_geom_residual,
        "gcp_left_corrected": np.asarray(target["left_gcp_corrected"], dtype=np.float32),
        "gcp_right_corrected": np.asarray(target["right_gcp_corrected"], dtype=np.float32),
        "pelvis_to_foot_target_direction": direction_target,
        "pelvis_to_foot_result_direction": direction_result,
        "pelvis_to_foot_residual_angle_rad": np.arccos(direction_cosine).astype(np.float32),
    }
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
        "foot_geom_task_names": foot_geom_names,
        "foot_geom_task_axes": ["z"] * len(foot_geom_names),
        "gcp_sides": ["left", "right"],
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
