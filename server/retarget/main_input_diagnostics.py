# -*- coding: utf-8 -*-
"""Build and persist Primary postprocessing data from a Primary IK result.

The builder is deliberately independent from Main IK.  It returns an in-memory
dataset first and delegates persistence to a format writer so CSV can later be
replaced by a binary or pickle writer without changing the calculation path.
"""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import numpy as np

from main_calibration import CalibrationSettings, analyze_main_calibration


PRIMARY_POST_FIELDS = [
    "frame",
    "source_frame",
    "time_s",
    "MEVA_Pelvis_x",
    "MEVA_Pelvis_y",
    "MEVA_Pelvis_z",
    "MEVA_LeftFoot_x",
    "MEVA_LeftFoot_y",
    "MEVA_LeftFoot_z",
    "MEVA_RightFoot_x",
    "MEVA_RightFoot_y",
    "MEVA_RightFoot_z",
    "Robot_Primary_Pelvis_x",
    "Robot_Primary_Pelvis_y",
    "Robot_Primary_Pelvis_z",
    "Robot_Primary_LeftFoot_x",
    "Robot_Primary_LeftFoot_y",
    "Robot_Primary_LeftFoot_z",
    "Robot_Primary_RightFoot_x",
    "Robot_Primary_RightFoot_y",
    "Robot_Primary_RightFoot_z",
    "MEVA_LeftFoot_GCP_FF_raw",
    "MEVA_LeftFoot_GCP_CA_raw",
    "MEVA_RightFoot_GCP_FF_raw",
    "MEVA_RightFoot_GCP_CA_raw",
    "MEVA_LeftFoot_GCP_selected_raw",
    "MEVA_RightFoot_GCP_selected_raw",
    "MEVA_Pelvis_z_minus_LeftFoot_z",
    "MEVA_Pelvis_z_minus_RightFoot_z",
    "Robot_Primary_Pelvis_z_minus_LeftFoot_z",
    "Robot_Primary_Pelvis_z_minus_RightFoot_z",
    "MEVA_Left_Pelvis_to_Foot_vertical_angle_deg",
    "MEVA_Right_Pelvis_to_Foot_vertical_angle_deg",
    "Robot_Left_minimum_GEOM_z_Main_base",
    "Robot_Right_minimum_GEOM_z_Main_base",
    "Robot_Pelvis_z_target_Main_input",
    "Robot_global_z_shift_to_Main_input",
]


@dataclass(frozen=True)
class PrimaryPostDiagnostics:
    rows: list[dict[str, Any]]
    metadata: dict[str, Any]
    postprocessed_root_pos: np.ndarray
    pelvis_targets_z: np.ndarray
    pelvis_shifts_z: np.ndarray


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, np.generic):
        value = value.item()
    if isinstance(value, float) and not np.isfinite(value):
        return None
    return value


def build_primary_post_diagnostics(
    *,
    primary_motion: dict,
    meva_csv: Path,
    robot_xml: Path,
    config: dict,
    primary_target_npz: Path | None = None,
    calibration_settings: CalibrationSettings,
    robot_foot_ground_height_m: float,
) -> PrimaryPostDiagnostics:
    """Derive Primary-post data without running Primary or Main IK."""
    rows, summary, contact_geometry = analyze_main_calibration(
        primary_motion=primary_motion,
        meva_csv=meva_csv,
        primary_target_npz=primary_target_npz,
        robot_xml=robot_xml,
        settings=calibration_settings,
        config=config,
    )
    scale_common = float(summary["scale_common"]["scale"])
    meva_ground = float(summary["meva_foot_z_at_ground_m"])
    if not np.isfinite(meva_ground):
        # Main itself cannot proceed without this value.  Keep Primary output
        # usable and make the unavailable Main-base diagnostic explicit.
        main_base_available = False
    else:
        main_base_available = True

    primary_root_pos = np.asarray(primary_motion["root_pos"], dtype=np.float64)
    postprocessed_root_pos = primary_root_pos.copy()
    pelvis_targets_z = np.full(len(rows), np.nan, dtype=np.float64)
    pelvis_shifts_z = np.full(len(rows), np.nan, dtype=np.float64)
    output_rows: list[dict[str, Any]] = []
    for frame_index, row in enumerate(rows):
        item = {
            "frame": row["frame"],
            "source_frame": row["source_frame"],
            "time_s": row["time_s"],
            "MEVA_Pelvis_x": row["MEVA_Pelvis_x"],
            "MEVA_Pelvis_y": row["MEVA_Pelvis_y"],
            "MEVA_Pelvis_z": row["MEVA_Pelvis_z"],
            "MEVA_LeftFoot_x": row["MEVA_LeftFoot_x"],
            "MEVA_LeftFoot_y": row["MEVA_LeftFoot_y"],
            "MEVA_LeftFoot_z": row["MEVA_LeftFoot_z"],
            "MEVA_RightFoot_x": row["MEVA_RightFoot_x"],
            "MEVA_RightFoot_y": row["MEVA_RightFoot_y"],
            "MEVA_RightFoot_z": row["MEVA_RightFoot_z"],
            "Robot_Primary_Pelvis_x": row["Primary_Pelvis_x"],
            "Robot_Primary_Pelvis_y": row["Primary_Pelvis_y"],
            "Robot_Primary_Pelvis_z": row["Primary_Pelvis_z"],
            "Robot_Primary_LeftFoot_x": row["Primary_LeftFoot_x"],
            "Robot_Primary_LeftFoot_y": row["Primary_LeftFoot_y"],
            "Robot_Primary_LeftFoot_z": row["Primary_LeftFoot_z"],
            "Robot_Primary_RightFoot_x": row["Primary_RightFoot_x"],
            "Robot_Primary_RightFoot_y": row["Primary_RightFoot_y"],
            "Robot_Primary_RightFoot_z": row["Primary_RightFoot_z"],
            "MEVA_LeftFoot_GCP_FF_raw": row["MEVA_LeftFoot_GCP_FF"],
            "MEVA_LeftFoot_GCP_CA_raw": row["MEVA_LeftFoot_GCP_CA"],
            "MEVA_RightFoot_GCP_FF_raw": row["MEVA_RightFoot_GCP_FF"],
            "MEVA_RightFoot_GCP_CA_raw": row["MEVA_RightFoot_GCP_CA"],
            "MEVA_LeftFoot_GCP_selected_raw": row["Left_selected_GCP_raw"],
            "MEVA_RightFoot_GCP_selected_raw": row["Right_selected_GCP_raw"],
            "MEVA_Pelvis_z_minus_LeftFoot_z": row["MEVA_Pelvis_z-LeftFoot_z"],
            "MEVA_Pelvis_z_minus_RightFoot_z": row["MEVA_Pelvis_z-RightFoot_z"],
            "Robot_Primary_Pelvis_z_minus_LeftFoot_z": row["Primary_Pelvis_z-LeftFoot_z"],
            "Robot_Primary_Pelvis_z_minus_RightFoot_z": row["Primary_Pelvis_z-RightFoot_z"],
            "MEVA_Left_Pelvis_to_Foot_vertical_angle_deg": row[
                "MEVA_Left_Pelvis_to_Foot_vertical_angle_deg"
            ],
            "MEVA_Right_Pelvis_to_Foot_vertical_angle_deg": row[
                "MEVA_Right_Pelvis_to_Foot_vertical_angle_deg"
            ],
        }
        if main_base_available:
            pelvis_target = (
                float(robot_foot_ground_height_m)
                + scale_common * (float(row["MEVA_Pelvis_z"]) - meva_ground)
            )
            pelvis_shift = pelvis_target - float(row["Primary_Pelvis_z"])
            pelvis_targets_z[frame_index] = pelvis_target
            pelvis_shifts_z[frame_index] = pelvis_shift
            postprocessed_root_pos[frame_index, 2] += pelvis_shift
            # Primary completes with the root translation applied.  A root Z
            # translation moves every FK-derived Robot point equally, so keep
            # the diagnostic Robot Primary coordinates aligned with the final
            # Primary PKL rather than the pre-shift IK snapshot.
            item["Robot_Primary_Pelvis_z"] += pelvis_shift
            item["Robot_Primary_LeftFoot_z"] += pelvis_shift
            item["Robot_Primary_RightFoot_z"] += pelvis_shift
        else:
            pelvis_target = pelvis_shift = float("nan")
        for side, title in (("left", "Left"), ("right", "Right")):
            if main_base_available:
                primary_geom = np.asarray(
                    contact_geometry[side]["xyz"][frame_index], dtype=np.float64
                )
                # Primary's root Z shift is a rigid translation.  Main base is
                # therefore the actual final-Primary GEOM Z, not a separately
                # reconstructed MEVA-derived Foot height.
                minimum_z = float(np.min(primary_geom[:, 2] + pelvis_shift))
            else:
                minimum_z = float("nan")
            item[f"Robot_{title}_minimum_GEOM_z_Main_base"] = minimum_z
        item["Robot_Pelvis_z_target_Main_input"] = pelvis_target
        item["Robot_global_z_shift_to_Main_input"] = pelvis_shift
        output_rows.append(item)

    metadata = {
        "schema": "meva-primary-post",
        "schema_version": 3,
        "storage_format": "csv",
        "frame_count": len(output_rows),
        "fps": float(primary_motion.get("fps", 100.0)),
        "primary_result_reused": True,
        "main_ik_executed": False,
        "gcp_values_in_csv": "raw; corrected GCP is calculated by the viewer",
        "pelvis_foot_scale_g": {
            "common": scale_common,
            "left": float(summary["scale_left"]["scale"]),
            "right": float(summary["scale_right"]["scale"]),
            "fit": "least_squares_through_origin",
        },
        "main_base": {
            "available": main_base_available,
            "robot_foot_ground_height_m": float(robot_foot_ground_height_m),
            "meva_foot_z_at_ground_m": meva_ground,
            "geom_definition": (
                "minimum of four contact GEOM center Z values in the final "
                "postprocessed Primary pose; before Main Ground correction"
            ),
        },
        "primary_postprocess": {
            "completed": main_base_available,
            "root_pos_shift_applied": main_base_available,
            "sequence": [
                "fixed_foot_to_ground_offset",
                "pelvis_foot_scale_g",
                "meva_ground_reference_hM",
                "robot_ground_reference_hG",
                "primary_root_z_shift",
            ],
            "meva_ground_reference_hM_m": meva_ground,
            "meva_foot_to_ground_offset_m": meva_ground,
            "robot_ground_reference_hG_m": float(robot_foot_ground_height_m),
            "robot_foot_to_ground_offset_m": float(robot_foot_ground_height_m),
            "pelvis_target_formula": "hG + g * (MEVA_Pelvis_z - hM)",
        },
        "calibration_settings": {
            "geom_flatness_threshold_m": float(
                calibration_settings.geom_flatness_threshold_m
            ),
            "gcp_contact_threshold": float(
                calibration_settings.gcp_contact_threshold
            ),
        },
        "vertical_angle": {
            "coordinate_source": "MEVA",
            "unit": "degree",
            "formula": "acos((-v_z) / norm(Foot - Pelvis))",
        },
    }
    return PrimaryPostDiagnostics(
        rows=output_rows,
        metadata=metadata,
        postprocessed_root_pos=postprocessed_root_pos,
        pelvis_targets_z=pelvis_targets_z,
        pelvis_shifts_z=pelvis_shifts_z,
    )


def _write_csv(path: Path, dataset: PrimaryPostDiagnostics) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=PRIMARY_POST_FIELDS)
        writer.writeheader()
        writer.writerows(dataset.rows)


FORMAT_WRITERS: dict[str, Callable[[Path, PrimaryPostDiagnostics], None]] = {
    "csv": _write_csv,
}


def write_primary_post_diagnostics(
    path: Path,
    dataset: PrimaryPostDiagnostics,
    *,
    storage_format: str = "csv",
) -> tuple[Path, Path]:
    """Write diagnostics through a replaceable persistence adapter."""
    try:
        writer = FORMAT_WRITERS[storage_format]
    except KeyError as exc:
        raise ValueError(f"Unsupported Primary-post format: {storage_format}") from exc
    writer(path, dataset)
    metadata_path = path.with_suffix(".json")
    metadata = dict(dataset.metadata)
    metadata["data_file"] = path.name
    metadata_path.write_text(
        json.dumps(_json_safe(metadata), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path, metadata_path
