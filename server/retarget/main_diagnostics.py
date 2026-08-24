"""Post-solve Main diagnostics; intentionally independent from the IK solver."""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np


FIELDS = [
    "frame", "source_frame", "time_s", "iterations_used", "converged",
    "final_max_joint_delta_deg", "max_acceleration_ratio",
    "max_acceleration_joint", "max_abs_acceleration_rad_s2",
    "acceleration_limit_rad_s2", "acceleration_soft_weight",
    "max_joint_limit_cost", "max_orientation_error_deg",
]


def write_main_diagnostics_csv(
    path: Path,
    *,
    diagnostics: list[tuple],
    dof_pos: np.ndarray,
    source_frame_indices: np.ndarray,
    fps: float,
    joint_names: list[str],
    acceleration_limits: dict[str, float],
    weight_at_2x_limit: float,
) -> None:
    """Persist frame diagnostics without changing the IK solve."""
    frame_count = len(diagnostics)
    if len(dof_pos) != frame_count or len(source_frame_indices) != frame_count:
        raise ValueError("Main diagnostic arrays must have one row per trajectory frame")
    dt = 1.0 / float(fps)
    rows: list[dict] = []
    for frame_index, diag in enumerate(diagnostics):
        row = {
            "frame": frame_index,
            "source_frame": int(source_frame_indices[frame_index]),
            "time_s": frame_index / float(fps),
            "iterations_used": int(diag[3]),
            "converged": bool(diag[4]),
            "final_max_joint_delta_deg": float(diag[5]),
            "max_acceleration_ratio": "",
            "max_acceleration_joint": "",
            "max_abs_acceleration_rad_s2": "",
            "acceleration_limit_rad_s2": "",
            "acceleration_soft_weight": "",
            "max_joint_limit_cost": float(diag[1]),
            "max_orientation_error_deg": float(diag[2]),
        }
        if 0 < frame_index < frame_count - 1:
            acceleration = (
                dof_pos[frame_index + 1]
                - 2.0 * dof_pos[frame_index]
                + dof_pos[frame_index - 1]
            ) / (dt * dt)
            candidates = []
            for joint_index, joint_name in enumerate(joint_names):
                limit = float(acceleration_limits.get(joint_name, 0.0))
                if joint_index >= len(acceleration) or not np.isfinite(limit) or limit <= 0.0:
                    continue
                abs_acceleration = abs(float(acceleration[joint_index]))
                candidates.append((abs_acceleration / limit, joint_name, abs_acceleration, limit))
            if candidates:
                ratio, joint_name, abs_acceleration, limit = max(candidates, key=lambda item: item[0])
                row.update({
                    "max_acceleration_ratio": ratio,
                    "max_acceleration_joint": joint_name,
                    "max_abs_acceleration_rad_s2": abs_acceleration,
                    "acceleration_limit_rad_s2": limit,
                    "acceleration_soft_weight": (
                        0.0 if ratio <= 1.0 else weight_at_2x_limit * (ratio - 1.0)
                    ),
                })
        rows.append(row)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
