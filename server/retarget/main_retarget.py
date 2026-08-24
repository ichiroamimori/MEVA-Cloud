# -*- coding: utf-8 -*-
"""Main-stage target generation and common-Mink IK execution."""
from __future__ import annotations

import argparse
import csv
import json
import pickle
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

import numpy as np

from main_calibration import CalibrationSettings
from main_diagnostics import write_main_diagnostics_csv
from ik_solver import hinge_info, solve_ik_sequence
from main_prepare import (
    _support_state_and_used_gcp,
    apply_main_ik_result,
    prepare_main,
    prepare_main_ik_from_target,
)
from main_target import build_main_target, load_main_target
from main_postprocess import (
    GlobalContactAnchoringSettings,
    apply_global_contact_anchoring,
)
from validation_data import write_stage_validation_artifacts


CSV_FIELDS = [
    "frame",
    "source_frame",
    "source_frame_float",
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
    "MEVA_LeftFoot_GCP_FF",
    "MEVA_LeftFoot_GCP_CA",
    "MEVA_RightFoot_GCP_FF",
    "MEVA_RightFoot_GCP_CA",
    "Primary_Pelvis_x",
    "Primary_Pelvis_y",
    "Primary_Pelvis_z",
    "Primary_LeftFoot_x",
    "Primary_LeftFoot_y",
    "Primary_LeftFoot_z",
    "Primary_RightFoot_x",
    "Primary_RightFoot_y",
    "Primary_RightFoot_z",
    "MEVA_Pelvis_z-LeftFoot_z",
    "MEVA_Pelvis_z-RightFoot_z",
    "Primary_Pelvis_z-LeftFoot_z",
    "Primary_Pelvis_z-RightFoot_z",
    "MEVA_Left_Pelvis_to_Foot_vertical_angle_deg",
    "MEVA_Right_Pelvis_to_Foot_vertical_angle_deg",
    "Left_CA_ypos_z_at_MEVA_Foot_z",
    "Left_CA_yneg_z_at_MEVA_Foot_z",
    "Left_FF_ypos_z_at_MEVA_Foot_z",
    "Left_FF_yneg_z_at_MEVA_Foot_z",
    "Left_min_GEOM_contact",
    "Left_selected_GCP_raw",
    "Left_selected_GCP_smoothed",
    "Left_selected_GCP_corrected",
    "Right_CA_ypos_z_at_MEVA_Foot_z",
    "Right_CA_yneg_z_at_MEVA_Foot_z",
    "Right_FF_ypos_z_at_MEVA_Foot_z",
    "Right_FF_yneg_z_at_MEVA_Foot_z",
    "Right_min_GEOM_contact",
    "Right_selected_GCP_raw",
    "Right_selected_GCP_smoothed",
    "Right_selected_GCP_corrected",
    "Left_used_GCP",
    "Right_used_GCP",
    "Support_State",
    "G1_Pelvis_z_target_ground_corrected",
    "G1_global_z_shift_to_Pelvis_target",
    "G1_Pelvis_z_initial_after_shift",
    "G1_LeftFoot_z_base",
    "G1_RightFoot_z_base",
    "Left_contact_GEOM_1_base_z",
    "Left_contact_GEOM_2_base_z",
    "Left_contact_GEOM_3_base_z",
    "Left_contact_GEOM_4_base_z",
    "Left_contact_GEOM_1_current_z",
    "Left_contact_GEOM_2_current_z",
    "Left_contact_GEOM_3_current_z",
    "Left_contact_GEOM_4_current_z",
    "Left_minimum_GEOM_z_base",
    "Left_selected_GEOM_name",
    "Left_ground_contact_height_weight_H",
    "Left_ground_contact_correction_strength_a",
    "Left_ground_contact_delta_z",
    "Left_minimum_GEOM_z_target",
    "Left_contact_GEOM_1_target_z",
    "Left_contact_GEOM_2_target_z",
    "Left_contact_GEOM_3_target_z",
    "Left_contact_GEOM_4_target_z",
    "Right_contact_GEOM_1_base_z",
    "Right_contact_GEOM_2_base_z",
    "Right_contact_GEOM_3_base_z",
    "Right_contact_GEOM_4_base_z",
    "Right_contact_GEOM_1_current_z",
    "Right_contact_GEOM_2_current_z",
    "Right_contact_GEOM_3_current_z",
    "Right_contact_GEOM_4_current_z",
    "Right_minimum_GEOM_z_base",
    "Right_selected_GEOM_name",
    "Right_ground_contact_height_weight_H",
    "Right_ground_contact_correction_strength_a",
    "Right_ground_contact_delta_z",
    "Right_minimum_GEOM_z_target",
    "Right_contact_GEOM_1_target_z",
    "Right_contact_GEOM_2_target_z",
    "Right_contact_GEOM_3_target_z",
    "Right_contact_GEOM_4_target_z",
    "G1_Pelvis_z_after_IK",
    "Pelvis_z_target_error_after_IK",
    "Left_contact_GEOM_1_z_after_IK",
    "Left_contact_GEOM_2_z_after_IK",
    "Left_contact_GEOM_3_z_after_IK",
    "Left_contact_GEOM_4_z_after_IK",
    "Left_contact_GEOM_1_z_error_after_IK",
    "Left_contact_GEOM_2_z_error_after_IK",
    "Left_contact_GEOM_3_z_error_after_IK",
    "Left_contact_GEOM_4_z_error_after_IK",
    "Left_minimum_GEOM_z_after_IK",
    "Right_contact_GEOM_1_z_after_IK",
    "Right_contact_GEOM_2_z_after_IK",
    "Right_contact_GEOM_3_z_after_IK",
    "Right_contact_GEOM_4_z_after_IK",
    "Right_contact_GEOM_1_z_error_after_IK",
    "Right_contact_GEOM_2_z_error_after_IK",
    "Right_contact_GEOM_3_z_error_after_IK",
    "Right_contact_GEOM_4_z_error_after_IK",
    "Right_minimum_GEOM_z_after_IK",
    "Main_IK_iterations_used",
    "Main_IK_converged",
    "Main_IK_final_max_joint_delta_deg",
    "Global_contact_state",
    "Global_translation_x",
    "Global_translation_y",
    "Left_contact_active",
    "Left_corrected_GCP",
    "Left_minimum_GEOM_name",
    "Left_minimum_GEOM_z",
    "Left_anchor_GEOM_name",
    "Left_anchor_world_x",
    "Left_anchor_world_y",
    "Left_required_translation_x",
    "Left_required_translation_y",
    "Left_anchor_error_x_after",
    "Left_anchor_error_y_after",
    "Right_contact_active",
    "Right_corrected_GCP",
    "Right_minimum_GEOM_name",
    "Right_minimum_GEOM_z",
    "Right_anchor_GEOM_name",
    "Right_anchor_world_x",
    "Right_anchor_world_y",
    "Right_required_translation_x",
    "Right_required_translation_y",
    "Right_anchor_error_x_after",
    "Right_anchor_error_y_after",
    "Left_weight",
    "Right_weight",
]


def repo_root_from(config_path: Path) -> Path:
    config_path = config_path.resolve()
    for candidate in [config_path.parent, *config_path.parents]:
        if (candidate / "server").is_dir() and (candidate / "workspace").is_dir():
            return candidate
    raise RuntimeError(f"Could not locate repository root from {config_path}")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_pickle(path: Path, obj: dict) -> None:
    with path.open("wb") as f:
        pickle.dump(obj, f)


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def _json_safe(value):
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if isinstance(value, np.generic):
        value = value.item()
    if isinstance(value, float) and not np.isfinite(value):
        return None
    return value


def write_json(path: Path, data: dict) -> None:
    path.write_text(
        json.dumps(_json_safe(data), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def run_main(config_path: Path) -> tuple[Path, Path]:
    config_path = config_path.resolve()
    cfg = load_json(config_path)
    root = repo_root_from(config_path)
    output_dir = config_path.parent
    main_id = output_dir.name
    primary_run_id = str(cfg.get("primary_run_id") or main_id)
    is_legacy_nested_main = output_dir.parent.name.lower() == "main"
    if is_legacy_nested_main:
        primary_dir = output_dir.parent.parent
    elif output_dir.name == primary_run_id:
        # Read-only compatibility for the original flat Main artifacts.
        primary_dir = output_dir
    else:
        primary_dir = output_dir.parent

    primary_pkl = primary_dir / f"{primary_run_id}_primary.pkl"
    if not primary_pkl.exists():
        # Backward-compatible fallback if an older run used a generic name.
        legacy = primary_dir / "primary.pkl"
        if legacy.exists():
            primary_pkl = legacy
        else:
            raise FileNotFoundError(f"Primary PKL not found in {primary_dir}")

    primary_post_csv = primary_dir / f"{primary_run_id}_primary_post.csv"
    if not primary_post_csv.exists():
        # Read-only compatibility for Primary runs created before the rename.
        legacy_primary_post = primary_dir / f"{primary_run_id}_main_input.csv"
        if legacy_primary_post.exists():
            primary_post_csv = legacy_primary_post
        else:
            raise FileNotFoundError(f"Primary post CSV not found in {primary_dir}")
    primary_target_npz = primary_dir / f"{primary_run_id}_primary_target.npz"
    if not primary_target_npz.exists():
        raise FileNotFoundError(
            f"Primary target NPZ is required for Main: {primary_target_npz}"
        )

    meva_csv = (root / cfg["source"]["file"]).resolve()
    robot_xml = (root / cfg["robot"]["mjcf"]).resolve()

    main_cfg = dict(cfg.get("main", {}))
    ground_cfg = dict(cfg.get("ground_contact_estimation", {}))
    offset_cfg = dict(cfg.get("foot_to_ground_offset", {}))
    gcp_smoothing_ms = float(main_cfg.get("gcp_smoothing_ms", 150.0))
    gcp_min_offset = float(main_cfg.get("gcp_min_offset", 0.2))
    gcp_max_offset = float(main_cfg.get("gcp_max_offset", 0.99))
    gcp_power_number = float(main_cfg.get(
        "gcp_power_number",
        main_cfg.get("gcp_multiplier", 2.0),
    ))
    robot_foot_ground_height = float(offset_cfg.get(
        "robot_m", ground_cfg.get("robot_foot_ground_height_m", 0.035)
    ))
    meva_foot_ground_height = float(offset_cfg.get("meva_m", 0.030))
    if not np.isfinite(robot_foot_ground_height) or robot_foot_ground_height < 0.0:
        raise ValueError("main.robot_foot_ground_height_m must be finite and non-negative")
    height_cfg = dict(main_cfg.get("ground_contact_height_correction", {}))
    full_correction_height = float(height_cfg.get("full_correction_height_m", 0.02))
    no_correction_height = float(height_cfg.get("no_correction_height_m", 0.04))
    flying_min_percent = float(main_cfg.get("flying_min_percent", 0.0))
    flying_max_percent = float(main_cfg.get("flying_max_percent", 0.0))
    anchoring_cfg = dict(main_cfg.get("global_contact_anchoring", {}))
    anchoring_settings = GlobalContactAnchoringSettings(
        enabled=bool(anchoring_cfg.get("enabled", True)),
    )

    def progress(done: int, total: int, source_frame: int) -> None:
        if done % 25 == 0 or done == total:
            print(f"[{done}/{total}] frame {source_frame}", flush=True)

    preparation = prepare_main(
        config_path=config_path,
        primary_pkl=primary_pkl,
        primary_post_csv=primary_post_csv,
        primary_target_npz=primary_target_npz,
        meva_csv=meva_csv,
        robot_xml=robot_xml,
        cfg=cfg,
        calibration_settings=CalibrationSettings(
            geom_flatness_threshold_m=0.0,
            gcp_contact_threshold=0.0,
            gcp_smoothing_ms=gcp_smoothing_ms,
            gcp_min_offset=gcp_min_offset,
            gcp_max_offset=gcp_max_offset,
            gcp_power_number=gcp_power_number,
        ),
        robot_foot_ground_height_m=robot_foot_ground_height,
        full_correction_height_m=full_correction_height,
        no_correction_height_m=no_correction_height,
        flying_min_percent=flying_min_percent,
        flying_max_percent=flying_max_percent,
        sole_position_weights=height_cfg.get("sole_position_weights", {}),
        progress_callback=progress,
    )
    main_target_path = output_dir / f"{main_id}_main_target.npz"
    target_build = build_main_target(
        output_path=main_target_path,
        primary=preparation.primary_motion,
        primary_target_path=primary_target_npz,
        model=preparation.model,
        cfg=cfg,
        contact_geometry=preparation.contact_geometry,
        mapping_offset_path=preparation.mapping_offset_path,
        fallback_common_scale=preparation.scale_common,
        meva_foot_to_ground_offset_m=meva_foot_ground_height,
        robot_foot_to_ground_offset_m=robot_foot_ground_height,
        gcp_smoothing_ms=gcp_smoothing_ms,
        gcp_min_offset=gcp_min_offset,
        gcp_max_offset=gcp_max_offset,
        gcp_power_number=gcp_power_number,
    )
    main_target = load_main_target(
        main_target_path,
        expected_frames=len(preparation.rows),
        expected_fps=float(preparation.primary_motion.get("fps", 30.0)),
    )
    # Support State remains a separate anchoring/audit value.  Main IK targets
    # below come exclusively from main_target.npz.
    for frame_index, row in enumerate(preparation.rows):
        left_corrected = float(main_target["left_gcp_corrected"][frame_index])
        right_corrected = float(main_target["right_gcp_corrected"][frame_index])
        state, left_used, right_used = _support_state_and_used_gcp(
            left_corrected=left_corrected,
            right_corrected=right_corrected,
            left_angle_deg=float(row["MEVA_Left_Pelvis_to_Foot_vertical_angle_deg"]),
            right_angle_deg=float(row["MEVA_Right_Pelvis_to_Foot_vertical_angle_deg"]),
            flying_max_percent=flying_max_percent,
        )
        row["Left_corrected_GCP"] = left_corrected
        row["Right_corrected_GCP"] = right_corrected
        row["Left_used_GCP"] = left_used
        row["Right_used_GCP"] = right_used
        row["Support_State"] = int(state)
        preparation.pelvis_targets_z[frame_index] = float(
            main_target["pelvis_target_xyz"][frame_index, 2]
        )
        for side, title in (("left", "Left"), ("right", "Right")):
            preparation.sole_targets_xyz[side][frame_index, :, 2] = (
                main_target[f"{side}_geom_target_z"][frame_index]
            )
            for geom_index in range(4):
                row[f"{title}_contact_GEOM_{geom_index + 1}_current_z"] = float(
                    target_build.base_z[side][frame_index, geom_index]
                )
                row[f"{title}_contact_GEOM_{geom_index + 1}_target_z"] = float(
                    main_target[f"{side}_geom_target_z"][frame_index, geom_index]
                )
    ik_preparation = prepare_main_ik_from_target(
        primary_pkl=primary_pkl,
        main_target_npz=main_target_path,
        robot_xml=robot_xml,
        cfg=cfg,
        sole_position_weights=height_cfg.get("sole_position_weights", {}),
    )
    preparation.initial_configuration = ik_preparation.initial_configuration
    preparation.solver_frame_specs = ik_preparation.solver_frame_specs
    preparation.solver_settings = ik_preparation.solver_settings
    preparation.diagnostic_keys = ik_preparation.diagnostic_keys
    rows = preparation.rows
    summary = preparation.calibration_summary
    contact_geometry = preparation.contact_geometry
    meva_foot_z_at_ground = preparation.meva_foot_z_at_ground_m
    scale_common = preparation.scale_common
    scale_left = preparation.scale_left
    scale_right = preparation.scale_right
    scale_rmse = preparation.scale_rmse_m
    scale_r2 = preparation.scale_r2
    sole_targets = preparation.sole_targets_xyz
    print("Main target:", main_target_path, flush=True)
    print("Main IK: common Mink solver", flush=True)
    ik_result = solve_ik_sequence(
        model=preparation.model,
        initial_configuration=preparation.initial_configuration,
        frame_specs=preparation.solver_frame_specs,
        solver_settings=preparation.solver_settings,
        diagnostic_keys=preparation.diagnostic_keys,
    )
    print("Main postprocess: Global Contact Anchoring (World X/Y only)", flush=True)
    postprocess_result = apply_global_contact_anchoring(
        model=preparation.model,
        qpos=ik_result.qpos,
        rows=rows,
        contact_geometry=contact_geometry,
        settings=anchoring_settings,
    )
    for row, diagnostics in zip(rows, postprocess_result.diagnostics):
        row.update(diagnostics)
    final_ik_result = replace(ik_result, qpos=postprocess_result.qpos)
    out = apply_main_ik_result(preparation, final_ik_result)

    calibration_result = {
        "pelvis_foot_scale": {
            "common": scale_common,
            "left": scale_left,
            "right": scale_right,
            "common_rmse_m": scale_rmse,
            "common_r2": scale_r2,
            "sample_count_per_side": int(len(rows)),
        },
        "meva_ground_reference": {
            "foot_z_at_ground_m": meva_foot_z_at_ground,
            "sample_count_left": int(summary["left_ground_sample_count"]),
            "sample_count_right": int(summary["right_ground_sample_count"]),
            "sample_count_total": int(summary["ground_sample_count_total"]),
            "left_sample_mean_m": summary.get("left_ground_sample_mean_m"),
            "right_sample_mean_m": summary.get("right_ground_sample_mean_m"),
        },
        "foot_to_ground_offset": {
            "meva_m": meva_foot_z_at_ground,
            "robot_m": robot_foot_ground_height,
        },
        "gcp_preprocessing": {
            "smoothing_ms": gcp_smoothing_ms,
            "smoothing_frames": int(summary["gcp_smoothing_frames"]),
            "min_offset": gcp_min_offset,
            "max_offset": gcp_max_offset,
            "power_number": gcp_power_number,
            "correction_formula": (
                "clip((smoothed_gcp - min_offset) / "
                "(max_offset - min_offset), 0, 1) ** power_number"
            ),
        },
        "ground_contact_height_correction": {
            "full_correction_height_m": full_correction_height,
            "no_correction_height_m": no_correction_height,
            "target_formula": "(1 - corrected_gcp) * max(base_min_geom_z, 0)",
            "common_translation_per_foot": True,
            "foot_base_geometry_source": "final postprocessed Primary FK",
            "uses_pelvis_initial_shift_for_sole_targets": False,
            "applied_to_main_ik": True,
        },
        "support_state": {
            "flying_min_percent": flying_min_percent,
            "flying_max_percent": flying_max_percent,
            "decision_stage": "before_main_ik",
            "input": "in-memory pre-Main decision (not part of Main target)",
        },
        "global_contact_anchoring": {
            "enabled": anchoring_settings.enabled,
            "modified_qpos_components": ["root_world_x", "root_world_y"],
            "support_source": "in-memory pre-Main SupportState",
            "state_counts": postprocess_result.state_counts,
            "validation": postprocess_result.validation,
        },
    }
    cfg["main_id"] = main_id
    cfg["primary_run_id"] = primary_run_id
    cfg["primary_post_csv"] = primary_post_csv.name
    cfg["primary_target_npz"] = primary_target_npz.name
    cfg.pop("main_input_csv", None)
    cfg["main_target_npz"] = main_target_path.name
    cfg["main_calibration"] = calibration_result
    write_json(config_path, cfg)

    metadata = dict(out.get("metadata", {}))
    metadata.update({
        "main_retarget": True,
        "main_stage_version": "main-target-npz-v1",
        "main_source_primary": primary_pkl.name,
        "main_source_primary_post": primary_post_csv.name,
        "main_source_primary_target": primary_target_npz.name,
        "main_target_npz": main_target_path.name,
        "main_result_json": config_path.name,
        "main_calibration": {
            "scale_common": scale_common,
            "scale_left": scale_left,
            "scale_right": scale_right,
            "scale_common_rmse_m": scale_rmse,
            "scale_common_r2": scale_r2,
            "meva_foot_z_at_ground_m": meva_foot_z_at_ground,
            "left_ground_sample_count": int(summary["left_ground_sample_count"]),
            "right_ground_sample_count": int(summary["right_ground_sample_count"]),
            "robot_foot_ground_height_m": robot_foot_ground_height,
            "full_correction_height_m": full_correction_height,
            "no_correction_height_m": no_correction_height,
            "sole_target_base": "final postprocessed Primary contact GEOM XYZ",
            "sole_targets_use_pelvis_initial_shift": False,
            "sole_targets_applied_to_ik": True,
        },
    })
    metadata["main_sole_targets"] = {
        "coordinate_frame": "world",
        "geom_order": {
            "left": list(contact_geometry["left"]["display_names"]),
            "right": list(contact_geometry["right"]["display_names"]),
        },
        "position_weights": deepcopy(height_cfg.get("sole_position_weights", {})),
        "active_axes": ["z"],
        "base_z_source": "final postprocessed Primary FK",
        "primary_pose_usage": "full initial pose and Pelvis target",
        "uses_pelvis_initial_shift": False,
        "left_target_z": main_target["left_geom_target_z"],
        "right_target_z": main_target["right_geom_target_z"],
        "target_file": main_target_path.name,
        "applied_to_ik": True,
    }
    metadata["global_contact_anchoring"] = {
        "enabled": anchoring_settings.enabled,
        "input": "Main IK qpos plus persisted Support_State",
        "support_source": "in-memory pre-Main SupportState",
        "placement_dofs": "free-joint World X/Y only",
        "uses_meva_foot_xy": False,
        "runs_ik": False,
        "fixed_side": "SupportState main side only",
        "flight": "no fixed side; previous global translation retained",
        "state_counts": deepcopy(postprocess_result.state_counts),
        "validation": deepcopy(postprocess_result.validation),
    }
    converged_count = sum(bool(row[4]) for row in ik_result.diagnostics)
    mapping_residual_summary = {}
    for mapping in cfg.get("mappings", []):
        link = str(mapping["target_link"])
        values = np.asarray(
            ik_result.diagnostic_values_by_key.get(link, []), dtype=float
        )
        mapping_residual_summary[link] = {
            "source_segment": mapping["source_segment"],
            "target_link": link,
            "orientation_mode": mapping.get("orientation_mode", "full"),
            "orientation_weight": float(mapping["orientation_weight"]),
            "mean_error_deg": float(np.mean(values)) if len(values) else 0.0,
            "p95_error_deg": float(np.percentile(values, 95)) if len(values) else 0.0,
            "max_error_deg": float(np.max(values)) if len(values) else 0.0,
        }
    settings = preparation.solver_settings
    joint_default = dict(settings.joint_limit_avoidance.get("default", {}))
    metadata["main_ik"] = {
        "solver": settings.solver_name,
        "max_iterations_per_frame": settings.max_iterations,
        "converged_frames": int(converged_count),
        "frame_count": int(len(ik_result.diagnostics)),
        "initial_pose": "same-frame qpos assembled directly from Primary PKL",
        "pelvis_task": {
            "position": "main_target.npz pelvis_target_xyz",
            "orientation": "main_target.npz pelvis_target_quat",
        },
        "mapping_orientation_tasks": mapping_residual_summary,
        "sole_tasks": "four world-Z-only GEOM tasks per foot from main_target.npz",
        "foot_origin_task": False,
        "foot_origin_position_task": False,
        "foot_orientation_task": "Primary FK orientation from main_target.npz",
        "pelvis_to_foot_direction_task": {
            "enabled": bool(cfg.get("spatial_constraints", {}).get(
                "pelvis_foot_direction", {}
            ).get("enabled", False)),
            "target": "Primary FK direction from main_target.npz",
        },
        "temporal_reference": "previous Main final q",
        "temporal_dofs": "all articulated joints (Mink excludes floating base)",
        "diagnostic_values_by_key": ik_result.diagnostic_values_by_key,
    }
    metadata["orientation_residual_summary_deg"] = mapping_residual_summary
    metadata["solver_convergence"] = {
        "max_iterations_per_frame": int(settings.max_iterations),
        "joint_delta_threshold_deg": float(settings.convergence_joint_delta_deg),
        "consecutive_iterations_required": int(
            settings.convergence_consecutive_iterations
        ),
        "criterion": "max_abs_hinge_joint_delta_between_iterations",
    }
    metadata["joint_velocity_limit"] = {
        "enabled": bool(settings.velocity_limit_enabled),
        "default_rad_s": float(settings.velocity_limit_default_rad_s),
        "overrides": deepcopy(cfg.get(
            "interframe_joint_velocity_limit", {}
        ).get("overrides", {})),
        "reference": "previous_output_frame_final_q",
        "frame_dt_s": float(settings.output_frame_dt_s),
    }
    metadata["interframe_joint_velocity_limit"] = deepcopy(
        metadata["joint_velocity_limit"]
    )
    metadata["interframe_joint_acceleration_limit"] = {
        "enabled": bool(settings.acceleration_limit_enabled),
        "mode": "per_iteration_soft_boundary_task",
        "weight_at_2x_limit": float(settings.acceleration_weight_at_2x_limit),
        "limits_rad_s2": deepcopy(settings.acceleration_limit_by_joint),
        "reference": "two_previous_output_frame_final_q",
        "frame_dt_s": float(settings.output_frame_dt_s),
    }
    metadata["joint_limit_avoidance"] = {
        "enabled": bool(settings.joint_limit_avoidance.get("enabled", False)),
        "enforce_hard_xml_limits": bool(settings.enforce_hard_xml_limits),
        "mode": "dynamic_dof_damping",
        "default": deepcopy(joint_default),
        "overrides": deepcopy(settings.joint_limit_avoidance.get("overrides", {})),
    }
    metadata["temporal_regularization"] = {
        "enabled": bool(settings.temporal_regularization_enabled),
        "cost": float(settings.temporal_regularization_cost),
        "first_frame_regularized": False,
        "reference": "previous_retargeted_frame_final_q",
        "dofs": "all articulated joints; floating base excluded by Mink PostureTask",
    }
    metadata["mapping_offset_asset"] = str(preparation.mapping_offset_path)
    metadata["resolved_mapping_offsets_wxyz"] = {
        link: [float(x) for x in value]
        for link, value in preparation.mapping_offsets.items()
    }
    diagnostics_path = output_dir / f"{main_id}_main_diagnostics.csv"
    source_frame_indices = np.asarray(out.get("source_frame_indices"), dtype=np.int64)
    fps = float(out.get("fps", out.get("metadata", {}).get("fps", 1.0 / settings.output_frame_dt_s)))
    joint_names = [name for _, name, _, _, _, _, _ in hinge_info(preparation.model)]
    write_main_diagnostics_csv(
        diagnostics_path,
        diagnostics=ik_result.diagnostics,
        dof_pos=np.asarray(out["dof_pos"], dtype=float),
        source_frame_indices=source_frame_indices,
        fps=fps,
        joint_names=joint_names,
        acceleration_limits=settings.acceleration_limit_by_joint,
        weight_at_2x_limit=float(settings.acceleration_weight_at_2x_limit),
    )
    metadata["main_ik"]["diagnostics_csv"] = diagnostics_path.name
    metadata["diagnostics_csv"] = diagnostics_path.name
    out["metadata"] = metadata

    validation_metadata_path = write_stage_validation_artifacts(
        output_dir=output_dir,
        file_id=main_id,
        stage="main",
        repo_root=root,
        config=cfg,
        motion=out,
    )
    out["metadata"]["frame_validation"] = {
        "metadata_file": validation_metadata_path.name,
        "precomputed_after_stage": True,
    }

    csv_path = output_dir / f"{main_id}_main_targets.csv"
    pkl_path = output_dir / f"{main_id}_main.pkl"
    write_csv(csv_path, rows)
    save_pickle(pkl_path, out)

    print(f"Scale common: {scale_common:.9f}")
    print(f"MEVA Foot Z @ ground: {meva_foot_z_at_ground:.9f} m")
    print(f"Robot Foot Z @ ground: {robot_foot_ground_height:.9f} m")
    print(f"Main IK convergence: {converged_count}/{len(ik_result.diagnostics)}")
    print(
        "Global anchoring unchanged max |root Z|/|root quat|/|hinge qpos|: "
        f"{postprocess_result.validation['max_abs_root_z_diff']:.3e} / "
        f"{postprocess_result.validation['max_abs_root_quaternion_diff']:.3e} / "
        f"{postprocess_result.validation['max_abs_hinge_qpos_diff']:.3e}"
    )
    print(f"Main JSON: {config_path}")
    print(f"Main CSV: {csv_path}")
    print(f"Main diagnostics CSV: {diagnostics_path}")
    print(f"Main target NPZ: {main_target_path}")
    print(f"Main PKL: {pkl_path}")
    print(f"Main frame validation: {validation_metadata_path}")
    return csv_path, pkl_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path, help="Main-specific <id>_main_config.json")
    args = parser.parse_args()
    run_main(args.config)


if __name__ == "__main__":
    main()
