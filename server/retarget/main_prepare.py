# -*- coding: utf-8 -*-
"""Prepare Main initial motion, Pelvis targets, and Foot Sole IK tasks."""
from __future__ import annotations

import json
import csv
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import numpy as np
import mujoco
import mink

from ik_solver import (
    IKDiagnosticTarget,
    IKFrameSpec,
    IKSequenceResult,
    PreparedIKFrame,
    SolverSettings,
    build_solver_settings,
    extract_output,
)
from mapping_tasks import (
    MappingTaskSet,
    RelativeDirectionTask,
    axis_angle_deg,
    quat_angle_deg,
    quat_rotate_vec,
    required_quaternion_columns,
)
from main_calibration import (
    CalibrationSettings,
    _free_joint_qpos_addr,
    _hinge_joints,
    _mapped_link,
    _qpos_from_primary_frame,
    analyze_main_calibration,
    contact_geom_display_name,
    foot_contact_geom_ids,
    preprocess_gcp,
)
from check_offsets import compute_offsets
from support_state import SupportState
from main_target import load_main_target
from motion_io import load_motion


@dataclass
class MainPreparation:
    model: Any
    initial_configuration: Any
    rows: list[dict]
    calibration_summary: dict
    primary_motion: dict
    initial_motion: dict
    pelvis_targets_z: np.ndarray
    pelvis_initial_shifts_z: np.ndarray
    sole_targets_xyz: dict[str, np.ndarray]
    contact_geometry: dict
    scale_common: float
    scale_left: float
    scale_right: float
    scale_rmse_m: float
    scale_r2: float
    meva_foot_z_at_ground_m: float
    sole_position_weights: dict[str, Any]
    mapping_offsets: dict[str, np.ndarray]
    mapping_offset_path: Path
    solver_frame_specs: list[IKFrameSpec]
    solver_settings: SolverSettings
    diagnostic_keys: list[str]


@dataclass
class MainIKPreparation:
    """Solver inputs whose only motion sources are Primary motion and Main target NPZ."""
    model: Any
    initial_configuration: Any
    solver_frame_specs: list[IKFrameSpec]
    solver_settings: SolverSettings
    diagnostic_keys: list[str]


MAIN_INPUT_FIELDS = [
    "frame",
    "source_frame",
    "time_s",
    "Primary_Pelvis_x",
    "Primary_Pelvis_y",
    "Primary_Pelvis_z",
    "MEVA_Left_Pelvis_to_Foot_vertical_angle_deg",
    "MEVA_Right_Pelvis_to_Foot_vertical_angle_deg",
    "Left_corrected_GCP",
    "Right_corrected_GCP",
    "Left_used_GCP",
    "Right_used_GCP",
    "Support_State",
] + [
    f"{title}_contact_GEOM_{geom_index}_{phase}_z"
    for title in ("Left", "Right")
    for phase in ("current", "target")
    for geom_index in range(1, 5)
]


def write_main_input_csv(path: Path, preparation: MainPreparation) -> Path:
    """Persist the exact Ground-preprocessed values consumed by Main IK."""
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=MAIN_INPUT_FIELDS)
        writer.writeheader()
        for row in preparation.rows:
            writer.writerow({field: row[field] for field in MAIN_INPUT_FIELDS})
    return path


def load_main_input_csv(path: Path, preparation: MainPreparation) -> list[SupportState]:
    """Reload persisted Main input and apply its targets to the prepared IK."""
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        saved_rows = list(csv.DictReader(stream))
    if len(saved_rows) != len(preparation.rows):
        raise ValueError("Main input CSV frame count does not match preparation")
    states: list[SupportState] = []
    for frame_index, (saved, row) in enumerate(zip(saved_rows, preparation.rows)):
        if int(saved["source_frame"]) != int(row["source_frame"]):
            raise ValueError("Main input CSV source frames do not match preparation")
        state = SupportState(int(saved["Support_State"]))
        states.append(state)
        row["Support_State"] = int(state)
        for field in (
            "Left_corrected_GCP", "Right_corrected_GCP",
            "Left_used_GCP", "Right_used_GCP",
        ):
            row[field] = float(saved[field])
        for side, title in (("left", "Left"), ("right", "Right")):
            for geom_index in range(4):
                current_field = f"{title}_contact_GEOM_{geom_index + 1}_current_z"
                target_field = f"{title}_contact_GEOM_{geom_index + 1}_target_z"
                row[current_field] = float(saved[current_field])
                row[target_field] = float(saved[target_field])
                preparation.sole_targets_xyz[side][frame_index, geom_index, 2] = float(
                    saved[target_field]
                )
    return states


class GeomPositionTask(mink.Task):
    """World-XYZ position task for a MuJoCo GEOM selected by numeric id.

    The G1 sole contact spheres have no MJCF ``name`` attribute, so Mink's
    name-based FrameTask cannot address them.  Numeric ids remain the MJCF
    declaration order used by calibration and the UI.
    """

    k = 3

    def __init__(self, model, geom_id: int, cost, gain=1.0, lm_damping=0.0):
        cost = np.asarray(cost, dtype=float)
        if cost.shape != (3,) or not np.all(np.isfinite(cost)) or np.any(cost < 0.0):
            raise ValueError("GeomPositionTask cost must be three non-negative values")
        super().__init__(cost=cost, gain=gain, lm_damping=lm_damping)
        self.model = model
        self.geom_id = int(geom_id)
        self.target_xyz: np.ndarray | None = None

    def set_target(self, target_xyz) -> None:
        target = np.asarray(target_xyz, dtype=float)
        if target.shape != (3,) or not np.all(np.isfinite(target)):
            raise ValueError("GeomPositionTask target must be a finite XYZ vector")
        self.target_xyz = target.copy()

    def compute_error(self, configuration) -> np.ndarray:
        if self.target_xyz is None:
            raise RuntimeError("GeomPositionTask target is not set")
        return configuration.data.geom_xpos[self.geom_id] - self.target_xyz

    def compute_jacobian(self, configuration) -> np.ndarray:
        jac_pos = np.empty((3, self.model.nv), dtype=float)
        jac_rot = np.empty((3, self.model.nv), dtype=float)
        mujoco.mj_jacGeom(
            self.model, configuration.data, jac_pos, jac_rot, self.geom_id
        )
        return jac_pos


class GeomZTask(mink.Task):
    """One-axis world-Z task; X/Y are deliberately absent from the objective."""

    k = 1

    def __init__(self, model, geom_id: int, cost: float, gain=1.0, lm_damping=0.0):
        value = float(cost)
        if not np.isfinite(value) or value < 0.0:
            raise ValueError("GeomZTask cost must be finite and non-negative")
        super().__init__(cost=np.asarray([value]), gain=gain, lm_damping=lm_damping)
        self.model = model
        self.geom_id = int(geom_id)
        self.target_z: float | None = None

    def set_target(self, target_z: float) -> None:
        value = float(target_z)
        if not np.isfinite(value):
            raise ValueError("GeomZTask target must be finite")
        self.target_z = value

    def compute_error(self, configuration) -> np.ndarray:
        if self.target_z is None:
            raise RuntimeError("GeomZTask target is not set")
        return np.asarray([
            float(configuration.data.geom_xpos[self.geom_id, 2]) - self.target_z
        ])

    def compute_jacobian(self, configuration) -> np.ndarray:
        jac_pos = np.empty((3, self.model.nv), dtype=float)
        jac_rot = np.empty((3, self.model.nv), dtype=float)
        mujoco.mj_jacGeom(
            self.model, configuration.data, jac_pos, jac_rot, self.geom_id
        )
        return jac_pos[2:3]


def load_pickle(path: Path) -> dict:
    obj = load_motion(path)
    if not isinstance(obj, dict):
        raise TypeError(f"Expected dict in {path}, got {type(obj).__name__}")
    return obj


def height_attenuation(z_m: float, full_m: float, none_m: float) -> float:
    if not (np.isfinite(full_m) and np.isfinite(none_m) and 0.0 <= full_m < none_m):
        raise ValueError(
            "ground_contact_height_correction requires "
            "0 <= full_correction_height_m < no_correction_height_m"
        )
    z_m = float(z_m)
    if z_m <= full_m:
        return 1.0
    if z_m >= none_m:
        return 0.0
    phase = np.pi * (z_m - full_m) / (none_m - full_m)
    return float(0.5 * (1.0 + np.cos(phase)))


def sole_contact_targets(
    current_xyz: np.ndarray,
    used_gcp: float,
) -> tuple[np.ndarray, dict]:
    current_xyz = np.asarray(current_xyz, dtype=np.float64)
    if current_xyz.shape != (4, 3):
        raise ValueError(f"Expected four XYZ sole points, got {current_xyz.shape}")
    min_index = int(np.argmin(current_xyz[:, 2]))
    z_min = float(current_xyz[min_index, 2])
    z_safe = max(z_min, 0.0)
    z_target_min = (1.0 - float(used_gcp)) * z_safe
    delta_z = float(z_target_min - z_min)
    target_xyz = current_xyz.copy()
    target_xyz[:, 2] += delta_z
    return target_xyz, {
        "min_index": min_index,
        "z_min": z_min,
        "z_safe": z_safe,
        "strength": float(used_gcp),
        "delta_z": delta_z,
        "z_target_min": float(target_xyz[min_index, 2]),
    }


def _read_primary_post(path: Path, expected_frames: list[int]) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Primary post CSV not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    source_frames = [int(row["source_frame"]) for row in rows]
    if source_frames != expected_frames:
        raise ValueError("Primary post CSV frames do not match Primary PKL frames")
    return rows


def _support_state_and_used_gcp(
    *,
    left_corrected: float,
    right_corrected: float,
    left_angle_deg: float,
    right_angle_deg: float,
    flying_max_percent: float,
) -> tuple[SupportState, float, float]:
    if not all(np.isfinite(value) for value in (
        left_corrected, right_corrected, left_angle_deg, right_angle_deg
    )):
        raise ValueError("Support State inputs must be finite")
    left_used = float(left_corrected)
    right_used = float(right_corrected)
    left_main = left_angle_deg <= right_angle_deg
    left_contact = left_corrected == 1.0
    right_contact = right_corrected == 1.0
    if left_contact and right_contact:
        state = (
            SupportState.DOUBLE_LEFT_MAIN
            if left_main else SupportState.DOUBLE_RIGHT_MAIN
        )
    elif left_contact:
        state = SupportState.SINGLE_LEFT
    elif right_contact:
        state = SupportState.SINGLE_RIGHT
    elif flying_max_percent == 0.0:
        if left_main:
            left_used = 1.0
            state = SupportState.SINGLE_LEFT
        else:
            right_used = 1.0
            state = SupportState.SINGLE_RIGHT
    else:
        # Percentage adjustment for Flying max > 0 is intentionally deferred.
        state = SupportState.FLYING
    return state, left_used, right_used


def virtual_foot_contact_geometry(
    primary_geom_xyz: np.ndarray,
    primary_foot_z: float,
    foot_z_base: float,
) -> tuple[np.ndarray, float]:
    primary_geom_xyz = np.asarray(primary_geom_xyz, dtype=np.float64)
    if primary_geom_xyz.shape != (4, 3):
        raise ValueError(f"Expected four Primary XYZ sole points, got {primary_geom_xyz.shape}")
    foot_delta_z = float(foot_z_base) - float(primary_foot_z)
    base_xyz = primary_geom_xyz.copy()
    base_xyz[:, 2] += foot_delta_z
    return base_xyz, foot_delta_z


def _sole_weights(raw: dict) -> dict[str, list[np.ndarray]]:
    result: dict[str, list[np.ndarray]] = {}
    for side in ("left", "right"):
        rows = raw.get(side, []) if isinstance(raw, dict) else []
        if len(rows) != 4:
            raise ValueError(f"{side} sole requires four position weight rows")
        result[side] = []
        for values in rows:
            weight = np.asarray(
                [values[axis] for axis in ("x", "y", "z")], dtype=float
            )
            if not np.all(np.isfinite(weight)) or np.any(weight < 0.0):
                raise ValueError("Sole position weights must be finite and non-negative")
            result[side].append(weight)
    return result


def prepare_main(
    *,
    config_path: Path,
    primary_pkl: Path,
    primary_target_npz: Path | None,
    robot_xml: Path,
    cfg: dict,
    calibration_settings: CalibrationSettings,
    robot_foot_ground_height_m: float,
    full_correction_height_m: float,
    no_correction_height_m: float,
    flying_min_percent: float,
    flying_max_percent: float,
    sole_position_weights: dict,
    progress_callback: Callable[[int, int, int], None] | None = None,
) -> MainPreparation:
    """Prepare Main calibration, targets, initial qpos, and common-Solver specs."""
    primary = load_pickle(primary_pkl)
    rows, summary, contact_geometry = analyze_main_calibration(
        primary_motion=primary,
        meva_csv=None,
        primary_target_npz=primary_target_npz,
        robot_xml=robot_xml,
        settings=calibration_settings,
        config=cfg,
        progress_callback=progress_callback,
    )
    if not (
        np.isfinite(flying_min_percent)
        and np.isfinite(flying_max_percent)
        and 0.0 <= flying_min_percent <= flying_max_percent <= 100.0
    ):
        raise ValueError("Flying percentages require 0 <= min <= max <= 100")
    fps = float(primary.get("fps", cfg.get("source", {}).get("sampling_rate_hz", 100.0)))
    left_raw = np.asarray([
        float(row["Left_selected_GCP_raw"]) for row in rows
    ])
    right_raw = np.asarray([
        float(row["Right_selected_GCP_raw"]) for row in rows
    ])
    left_smoothed, left_corrected, _ = preprocess_gcp(
        left_raw,
        sampling_rate_hz=fps,
        smoothing_ms=calibration_settings.gcp_smoothing_ms,
        min_offset=calibration_settings.gcp_min_offset,
        max_offset=calibration_settings.gcp_max_offset,
        power_number=calibration_settings.gcp_power_number,
    )
    right_smoothed, right_corrected, _ = preprocess_gcp(
        right_raw,
        sampling_rate_hz=fps,
        smoothing_ms=calibration_settings.gcp_smoothing_ms,
        min_offset=calibration_settings.gcp_min_offset,
        max_offset=calibration_settings.gcp_max_offset,
        power_number=calibration_settings.gcp_power_number,
    )
    for index, row in enumerate(rows):
        row["Left_selected_GCP_raw"] = float(left_raw[index])
        row["Right_selected_GCP_raw"] = float(right_raw[index])
        row["Left_selected_GCP_smoothed"] = float(left_smoothed[index])
        row["Right_selected_GCP_smoothed"] = float(right_smoothed[index])
        row["Left_selected_GCP_corrected"] = float(left_corrected[index])
        row["Right_selected_GCP_corrected"] = float(right_corrected[index])
    primary_metadata = dict(primary.get("metadata", {}))
    postprocess = dict(primary_metadata.get("primary_postprocess", {}))
    saved_scale = dict(
        dict(primary_metadata.get(
            "primary_post_diagnostics",
            primary_metadata.get("main_input_diagnostics", {}),
        )).get(
            "pelvis_foot_scale_g", {}
        )
    )
    post_root_key = (
        "primary_post_root_pos" if "primary_post_root_pos" in primary
        else "main_input_root_pos"
    )
    post_targets_key = (
        "primary_post_pelvis_targets_z"
        if "primary_post_pelvis_targets_z" in primary
        else "main_input_pelvis_targets_z"
    )
    post_shifts_key = (
        "primary_post_pelvis_shifts_z"
        if "primary_post_pelvis_shifts_z" in primary
        else "main_input_pelvis_shifts_z"
    )
    has_primary_postprocess = bool(primary_metadata.get("canonical_motion_npz")) or (
        post_root_key in primary
        and post_targets_key in primary
        and post_shifts_key in primary
        and bool(postprocess.get("completed", False))
    )
    primary_root_shift_applied = bool(
        primary_metadata.get("canonical_motion_npz")
        or (has_primary_postprocess and postprocess.get("root_pos_shift_applied", False))
    )
    meva_ground = float(
        postprocess.get(
            "meva_ground_reference_hM_m",
            summary["meva_foot_z_at_ground_m"],
        )
    )
    if not np.isfinite(meva_ground):
        raise RuntimeError("MEVA Foot-to-ground offset is unavailable")
    scale_common = float(saved_scale.get("common", summary["scale_common"]["scale"]))
    scale_left = float(saved_scale.get("left", summary["scale_left"]["scale"]))
    scale_right = float(saved_scale.get("right", summary["scale_right"]["scale"]))
    scale_rmse = float(summary["scale_common"]["rmse_m"])
    scale_r2 = float(summary["scale_common"]["r2"])

    root_pos = np.asarray(primary["root_pos"], dtype=np.float64)
    if len(root_pos) != len(rows):
        raise ValueError("Calibration row count does not match Primary frame count")
    initial_motion = deepcopy(primary)
    if has_primary_postprocess and not primary_metadata.get("canonical_motion_npz"):
        pelvis_targets = np.asarray(primary[post_targets_key], dtype=np.float64).copy()
        if primary_root_shift_applied:
            out_root_pos = root_pos.copy()
            shifts = np.zeros(len(rows), dtype=np.float64)
        else:
            out_root_pos = np.asarray(primary[post_root_key], dtype=np.float64).copy()
            shifts = np.asarray(primary[post_shifts_key], dtype=np.float64).copy()
        if any(values.shape != (len(rows),) for values in (shifts, pelvis_targets)):
            raise ValueError("Primary Main-input Pelvis arrays do not match frame count")
        if out_root_pos.shape != root_pos.shape:
            raise ValueError("Primary main_input_root_pos shape does not match root_pos")
    else:
        out_root_pos = root_pos.copy()
        shifts = np.empty(len(rows), dtype=np.float64)
        pelvis_targets = np.empty(len(rows), dtype=np.float64)
    sole_targets = {
        "left": np.empty_like(contact_geometry["left"]["xyz"]),
        "right": np.empty_like(contact_geometry["right"]["xyz"]),
    }

    for i, row in enumerate(rows):
        if primary_root_shift_applied:
            # Ground preprocessing must not translate the Robot again.  Main
            # preserves the Pelvis height already stored in final Primary.
            pelvis_target = float(row["Primary_Pelvis_z"])
            pelvis_targets[i] = pelvis_target
            shift = 0.0
        elif has_primary_postprocess:
            pelvis_target = float(pelvis_targets[i])
            shift = float(shifts[i])
        else:
            pelvis_target = (
                robot_foot_ground_height_m
                + scale_common * (float(row["MEVA_Pelvis_z"]) - meva_ground)
            )
            shift = pelvis_target - float(row["Primary_Pelvis_z"])
            pelvis_targets[i] = pelvis_target
            shifts[i] = shift
            out_root_pos[i, 2] += shift
        row["G1_Pelvis_z_target_ground_corrected"] = pelvis_target
        row["G1_global_z_shift_to_Pelvis_target"] = shift
        row["G1_Pelvis_z_initial_after_shift"] = float(out_root_pos[i, 2])

        state, left_used, right_used = _support_state_and_used_gcp(
            left_corrected=float(row["Left_selected_GCP_corrected"]),
            right_corrected=float(row["Right_selected_GCP_corrected"]),
            left_angle_deg=float(row["MEVA_Left_Pelvis_to_Foot_vertical_angle_deg"]),
            right_angle_deg=float(row["MEVA_Right_Pelvis_to_Foot_vertical_angle_deg"]),
            flying_max_percent=float(flying_max_percent),
        )
        row["Left_corrected_GCP"] = float(row["Left_selected_GCP_corrected"])
        row["Right_corrected_GCP"] = float(row["Right_selected_GCP_corrected"])
        row["Left_used_GCP"] = left_used
        row["Right_used_GCP"] = right_used
        row["Support_State"] = int(state)

        for side, title in (("left", "Left"), ("right", "Right")):
            base_xyz = np.asarray(
                contact_geometry[side]["xyz"][i], dtype=np.float64
            ).copy()
            if not primary_root_shift_applied:
                base_xyz[:, 2] += shift
            used_gcp = left_used if side == "left" else right_used
            target_xyz, diag = sole_contact_targets(
                base_xyz,
                used_gcp,
            )
            sole_targets[side][i] = target_xyz
            min_index = int(diag["min_index"])
            row[f"G1_{title}Foot_z_base"] = float(row[f"Primary_{title}Foot_z"])
            for geom_index in range(4):
                row[f"{title}_contact_GEOM_{geom_index + 1}_current_z"] = float(
                    base_xyz[geom_index, 2]
                )
                row[f"{title}_contact_GEOM_{geom_index + 1}_base_z"] = float(
                    base_xyz[geom_index, 2]
                )
            row[f"{title}_minimum_GEOM_z_base"] = diag["z_min"]
            row[f"{title}_selected_GEOM_name"] = (
                contact_geometry[side]["display_names"][min_index]
            )
            row[f"{title}_ground_contact_height_weight_H"] = 1.0
            row[f"{title}_ground_contact_correction_strength_a"] = diag["strength"]
            row[f"{title}_ground_contact_delta_z"] = diag["delta_z"]
            row[f"{title}_minimum_GEOM_z_target"] = diag["z_target_min"]
            for geom_index in range(4):
                row[f"{title}_contact_GEOM_{geom_index + 1}_target_z"] = float(
                    target_xyz[geom_index, 2]
                )

    if flying_max_percent == 0.0 and any(
        SupportState(int(row["Support_State"])) is SupportState.FLYING
        for row in rows
    ):
        raise AssertionError("Flying max 0 must not leave FLYING in Main input")

    initial_motion["root_pos"] = out_root_pos

    mapping_offsets, mapping_offset_path, _ = compute_offsets(
        config_path,
        force=bool(cfg.get("offsets", {}).get("force_recompute", False)),
    )
    mapping_offset_asset = json.loads(
        mapping_offset_path.read_text(encoding="utf-8")
    )
    offset_details = dict(mapping_offset_asset.get("details", {}))

    model = mujoco.MjModel.from_xml_path(str(robot_xml))
    free_qadr = _free_joint_qpos_addr(model)
    hinges = _hinge_joints(model)
    pelvis_link = _mapped_link(cfg, "Pelvis", "pelvis")
    weights = _sole_weights(sole_position_weights)
    lm_damping = float(cfg["solver"]["task_lm_damping"])

    mapping_fields = list(contact_geometry.get("_meva_fields", []))
    raw_mapping_rows = list(contact_geometry.get("_meva_rows", []))
    if len(raw_mapping_rows) != len(rows):
        raise ValueError("Selected MEVA Mapping rows do not match Main frame count")
    required_mapping_fields = required_quaternion_columns(cfg)
    missing = sorted(required_mapping_fields - set(mapping_fields))
    if missing:
        raise KeyError("Missing MEVA columns:\n  " + "\n  ".join(missing))
    mapping_field_indices = {
        field: mapping_fields.index(field) for field in required_mapping_fields
    }
    mapping_rows = [
        {
            field: raw_row[index]
            for field, index in mapping_field_indices.items()
        }
        for raw_row in raw_mapping_rows
    ]

    position_cost_by_link = {
        str(mapping["target_link"]): (
            float(cfg["root"]["position_cost"])
            if str(mapping["target_link"]) == pelvis_link else 0.0
        )
        for mapping in cfg.get("mappings", [])
    }
    mapping_tasks = MappingTaskSet(
        model=model,
        cfg=cfg,
        mapping_offsets=mapping_offsets,
        offset_details=offset_details,
        position_cost_by_link=position_cost_by_link,
    )
    pelvis_position_task = None
    if pelvis_link not in mapping_tasks.tasks_by_link:
        # The Main Pelvis position target exists independently of whether the
        # user configures a Pelvis orientation Mapping.
        pelvis_position_task = mink.FrameTask(
            pelvis_link,
            "body",
            position_cost=float(cfg["root"]["position_cost"]),
            orientation_cost=0.0,
            gain=1.0,
            lm_damping=lm_damping,
        )

    initial_qpos = np.empty((len(rows), model.nq), dtype=float)
    pelvis_target_xyz = np.empty((len(rows), 3), dtype=float)
    fk_configuration = mink.Configuration(model)
    for i in range(len(rows)):
        q_primary = _qpos_from_primary_frame(
            model, primary, i, free_qadr, hinges
        )
        fk_configuration.update(q=q_primary)
        pelvis_transform = fk_configuration.get_transform_frame_to_world(
            pelvis_link, "body"
        )
        pelvis_target_xyz[i] = pelvis_transform.translation()
        pelvis_target_xyz[i, 2] = pelvis_targets[i]
        q_initial = q_primary.copy()
        q_initial[free_qadr + 2] += shifts[i]
        initial_qpos[i] = q_initial

    sole_tasks: dict[str, list[GeomPositionTask]] = {"left": [], "right": []}
    for side in ("left", "right"):
        for geom_id, weight in zip(contact_geometry[side]["geom_ids"], weights[side]):
            sole_tasks[side].append(GeomPositionTask(
                model, geom_id, cost=weight, gain=1.0, lm_damping=lm_damping
            ))

    frame_specs: list[IKFrameSpec] = []
    diagnostic_keys = [
        str(mapping["target_link"]) for mapping in cfg.get("mappings", [])
    ] + ["pelvis_position_m"] + [
        f"{side}_sole_{geom_index + 1}_active_position_m"
        for side in ("left", "right") for geom_index in range(4)
    ]
    for frame_index, row in enumerate(rows):
        source_frame = int(row["source_frame"])

        def prepare_frame(configuration, frame_index=frame_index, source_frame=source_frame):
            prepared_mapping = mapping_tasks.prepare(
                row=mapping_rows[frame_index],
                configuration=configuration,
                source_frame=source_frame,
                position_targets_by_link={
                    pelvis_link: pelvis_target_xyz[frame_index]
                },
            )
            active_tasks = list(prepared_mapping.tasks)
            if pelvis_position_task is not None:
                pelvis_position_task.set_target(
                    mink.SE3.from_rotation_and_translation(
                        configuration.get_transform_frame_to_world(
                            pelvis_link, "body"
                        ).rotation(),
                        pelvis_target_xyz[frame_index],
                    )
                )
                active_tasks.append(pelvis_position_task)
            for side in ("left", "right"):
                for geom_index, task in enumerate(sole_tasks[side]):
                    task.set_target(sole_targets[side][frame_index, geom_index])
                    active_tasks.append(task)

            diagnostics = list(prepared_mapping.diagnostics)
            diagnostics.append(
                IKDiagnosticTarget(
                    key="pelvis_position_m",
                    metadata={"source_frame": source_frame, "target": "pelvis_position"},
                    measure=lambda current, frame_index=frame_index: float(np.max(np.abs(
                        current.get_transform_frame_to_world(pelvis_link, "body").translation()
                        - pelvis_target_xyz[frame_index]
                    ))),
                )
            )
            for side in ("left", "right"):
                for geom_index, task in enumerate(sole_tasks[side]):
                    active_axes = weights[side][geom_index] > 0.0

                    def measure(current, side=side, geom_index=geom_index,
                                task=task, active_axes=active_axes):
                        error = (
                            current.data.geom_xpos[task.geom_id]
                            - sole_targets[side][frame_index, geom_index]
                        )
                        return float(np.max(np.abs(error[active_axes]))) if np.any(active_axes) else 0.0

                    diagnostics.append(IKDiagnosticTarget(
                        key=f"{side}_sole_{geom_index + 1}_active_position_m",
                        metadata={
                            "source_frame": source_frame,
                            "target": f"{side}_sole_{geom_index + 1}",
                            "geom": contact_geometry[side]["display_names"][geom_index],
                        },
                        measure=measure,
                    ))
            return PreparedIKFrame(tasks=active_tasks, diagnostics=diagnostics)

        frame_specs.append(IKFrameSpec(
            source_frame=source_frame,
            prepare=prepare_frame,
            initial_q=initial_qpos[frame_index],
        ))

    solver_settings = build_solver_settings(
        model=model,
        cfg=cfg,
        output_frame_dt_s=1.0 / float(primary.get("fps", 30.0)),
        iteration_diagnostics=False,
    )

    return MainPreparation(
        model=model,
        initial_configuration=mink.Configuration(model, q=initial_qpos[0]),
        rows=rows,
        calibration_summary=summary,
        primary_motion=primary,
        initial_motion=initial_motion,
        pelvis_targets_z=pelvis_targets,
        pelvis_initial_shifts_z=shifts,
        sole_targets_xyz=sole_targets,
        contact_geometry=contact_geometry,
        scale_common=scale_common,
        scale_left=scale_left,
        scale_right=scale_right,
        scale_rmse_m=scale_rmse,
        scale_r2=scale_r2,
        meva_foot_z_at_ground_m=meva_ground,
        sole_position_weights=deepcopy(sole_position_weights),
        mapping_offsets={
            str(link): np.asarray(value, dtype=float).copy()
            for link, value in mapping_offsets.items()
        },
        mapping_offset_path=mapping_offset_path,
        solver_frame_specs=frame_specs,
        solver_settings=solver_settings,
        diagnostic_keys=diagnostic_keys,
    )


def prepare_main_ik_from_target(
    *,
    primary_pkl: Path,
    main_target_npz: Path,
    robot_xml: Path,
    cfg: dict,
    sole_position_weights: dict,
) -> MainIKPreparation:
    """Build Main solver frames from Primary motion + Main target only."""
    primary = load_pickle(primary_pkl)
    n = len(np.asarray(primary["root_pos"]))
    primary_fps = float(primary.get("fps", 30.0))
    target = load_main_target(
        main_target_npz, expected_frames=n, expected_fps=primary_fps
    )
    model = mujoco.MjModel.from_xml_path(str(robot_xml))
    free_qadr = _free_joint_qpos_addr(model)
    hinges = _hinge_joints(model)
    pelvis_link = _mapped_link(cfg, "Pelvis", "pelvis")
    lm_damping = float(cfg["solver"]["task_lm_damping"])
    weights = _sole_weights(sole_position_weights)

    mappings = list(cfg.get("mappings", []))
    link_names = [str(value) for value in target["link_names"]]
    config_link_names = [str(mapping["target_link"]) for mapping in mappings]
    if link_names != config_link_names:
        raise ValueError("Main target Mapping link order does not match Main config")
    modes = [str(value) for value in target["link_orientation_mode"]]
    config_modes = [str(mapping.get("orientation_mode", "full")) for mapping in mappings]
    if modes != config_modes:
        raise ValueError("Main target Mapping modes do not match Main config")

    mapping_tasks: dict[str, mink.Task] = {}
    for link_index, mapping in enumerate(mappings):
        link = str(mapping["target_link"])
        mode = modes[link_index]
        orientation_cost = float(mapping["orientation_weight"])
        if mode == "full":
            mapping_tasks[link] = mink.FrameTask(
                link,
                "body",
                position_cost=(
                    float(cfg["root"]["position_cost"])
                    if link == pelvis_link else 0.0
                ),
                orientation_cost=orientation_cost,
                gain=1.0,
                lm_damping=lm_damping,
            )
        else:
            mapping_tasks[link] = mink.AxisAlignTask(
                frame_name=link,
                frame_type="body",
                axis=np.asarray(target["link_axis_local"][link_index], dtype=float),
                cost=orientation_cost,
            )
    if pelvis_link not in mapping_tasks or modes[link_names.index(pelvis_link)] != "full":
        raise ValueError("Main Pelvis Mapping must be a full orientation task")

    spatial_cfg = dict(cfg.get("spatial_constraints", {}).get(
        "pelvis_foot_direction", {}
    ))
    spatial_tasks: dict[str, RelativeDirectionTask] = {}
    if bool(spatial_cfg.get("enabled", False)):
        for side, source, fallback in (
            ("left", "LeftFoot", "left_ankle_roll_link"),
            ("right", "RightFoot", "right_ankle_roll_link"),
        ):
            cost = float(spatial_cfg.get(f"{side}_cost", 0.0))
            if cost > 0.0:
                spatial_tasks[side] = RelativeDirectionTask(
                    pelvis_link,
                    _mapped_link(cfg, source, fallback),
                    cost=cost,
                    gain=1.0,
                    lm_damping=lm_damping,
                )

    geom_ids: dict[str, list[int]] = {}
    geom_tasks: dict[str, list[GeomZTask]] = {"left": [], "right": []}
    for side, segment, fallback in (
        ("left", "LeftFoot", "left_ankle_roll_link"),
        ("right", "RightFoot", "right_ankle_roll_link"),
    ):
        foot_link = _mapped_link(cfg, segment, fallback)
        ordered = foot_contact_geom_ids(model, foot_link)
        geom_ids[side] = list(ordered.values())
        actual_names = [contact_geom_display_name(model, geom_id) for geom_id in geom_ids[side]]
        saved_names = [str(value) for value in target[f"{side}_geom_names"]]
        if actual_names != saved_names:
            raise ValueError(f"{side} Main target GEOM order does not match Robot XML")
        for geom_id, weight in zip(geom_ids[side], weights[side]):
            geom_tasks[side].append(GeomZTask(
                model, geom_id, cost=float(weight[2]), gain=1.0,
                lm_damping=lm_damping,
            ))

    initial_qpos = np.asarray([
        _qpos_from_primary_frame(model, primary, i, free_qadr, hinges)
        for i in range(n)
    ])
    source_frames = np.asarray(
        primary.get("source_frame_indices", np.arange(n)), dtype=np.int64
    )
    frame_specs: list[IKFrameSpec] = []
    for frame_index in range(n):
        source_frame = int(source_frames[frame_index])

        def prepare_frame(configuration, frame_index=frame_index, source_frame=source_frame):
            tasks: list[mink.Task] = []
            target_quats: dict[str, np.ndarray] = {}
            target_axes: dict[str, np.ndarray] = {}
            diagnostics: list[IKDiagnosticTarget] = []
            for link_index, mapping in enumerate(mappings):
                link = str(mapping["target_link"])
                mode = modes[link_index]
                q_target = np.asarray(
                    target["link_target_quat"][frame_index, link_index], dtype=float
                )
                target_quats[link] = q_target
                task = mapping_tasks[link]
                if mode == "full":
                    translation = (
                        np.asarray(target["pelvis_target_xyz"][frame_index], dtype=float)
                        if link == pelvis_link
                        else configuration.get_transform_frame_to_world(
                            link, "body"
                        ).translation()
                    )
                    task.set_target(mink.SE3.from_rotation_and_translation(
                        mink.SO3(wxyz=q_target), translation
                    ))
                else:
                    target_axis = quat_rotate_vec(
                        q_target,
                        np.asarray(target["link_axis_local"][link_index], dtype=float),
                    )
                    target_axes[link] = target_axis
                    task.set_target(target_axis)
                tasks.append(task)

                def measure_orientation(
                    current, link=link, mode=mode, link_index=link_index,
                    q_target=q_target, target_axis=target_axes.get(link),
                ):
                    actual_q = current.get_transform_frame_to_world(
                        link, "body"
                    ).rotation().wxyz
                    if mode == "axis":
                        actual_axis = quat_rotate_vec(
                            actual_q,
                            np.asarray(target["link_axis_local"][link_index], dtype=float),
                        )
                        return axis_angle_deg(target_axis, actual_axis)
                    return quat_angle_deg(q_target, actual_q)

                diagnostics.append(IKDiagnosticTarget(
                    key=link,
                    metadata={
                        "source_frame": source_frame,
                        "target": "Primary FK orientation in main_target.npz",
                        "orientation_mode": mode,
                    },
                    measure=measure_orientation,
                ))

            for side, task in spatial_tasks.items():
                task.set_target(target[f"{side}_pelvis_to_foot_direction"][frame_index])
                tasks.append(task)

            diagnostics = [IKDiagnosticTarget(
                key="pelvis_position_m",
                metadata={"source_frame": source_frame, "target": "main_target_npz"},
                measure=lambda current, frame_index=frame_index: float(np.max(np.abs(
                    current.get_transform_frame_to_world(pelvis_link, "body").translation()
                    - target["pelvis_target_xyz"][frame_index]
                ))),
            )] + diagnostics
            for side in ("left", "right"):
                for geom_index, task in enumerate(geom_tasks[side]):
                    task.set_target(float(target[f"{side}_geom_target_z"][frame_index, geom_index]))
                    tasks.append(task)
                    diagnostics.append(IKDiagnosticTarget(
                        key=f"{side}_sole_{geom_index + 1}_z_m",
                        metadata={
                            "source_frame": source_frame,
                            "target": "main_target_npz_z_only",
                            "geom": str(target[f"{side}_geom_names"][geom_index]),
                        },
                        measure=lambda current, side=side, geom_index=geom_index, task=task,
                            frame_index=frame_index: abs(float(
                                current.data.geom_xpos[task.geom_id, 2]
                                - target[f"{side}_geom_target_z"][frame_index, geom_index]
                            )),
                    ))
            return PreparedIKFrame(tasks=tasks, diagnostics=diagnostics)

        frame_specs.append(IKFrameSpec(
            source_frame=source_frame,
            prepare=prepare_frame,
            initial_q=initial_qpos[frame_index].copy(),
        ))
    diagnostic_keys = config_link_names + ["pelvis_position_m"] + [
        f"{side}_sole_{index + 1}_z_m"
        for side in ("left", "right") for index in range(4)
    ]
    settings = build_solver_settings(
        model=model,
        cfg=cfg,
        output_frame_dt_s=1.0 / primary_fps,
        iteration_diagnostics=False,
    )
    return MainIKPreparation(
        model=model,
        initial_configuration=mink.Configuration(model, q=initial_qpos[0]),
        solver_frame_specs=frame_specs,
        solver_settings=settings,
        diagnostic_keys=diagnostic_keys,
    )


def apply_main_ik_result(
    preparation: MainPreparation, result: IKSequenceResult
) -> dict:
    """Convert common-Solver qpos to the in-memory motion representation."""
    primary = preparation.primary_motion
    output = deepcopy(primary)
    order = str(primary.get("metadata", {}).get("root_rot_order", "xyzw"))
    root_pos = []
    root_rot = []
    dof_pos = []
    data = mujoco.MjData(preparation.model)
    for frame_index, q in enumerate(result.qpos):
        pos, rot, dof = extract_output(preparation.model, q, order)
        root_pos.append(pos)
        root_rot.append(rot)
        dof_pos.append(dof)
        data.qpos[:] = q
        mujoco.mj_forward(preparation.model, data)
        row = preparation.rows[frame_index]
        pelvis_link = str(preparation.calibration_summary["pelvis_link"])
        pelvis_id = mujoco.mj_name2id(
            preparation.model, mujoco.mjtObj.mjOBJ_BODY, pelvis_link
        )
        pelvis_actual_z = float(data.xpos[pelvis_id, 2])
        row["G1_Pelvis_z_after_IK"] = pelvis_actual_z
        row["Pelvis_z_target_error_after_IK"] = (
            pelvis_actual_z - float(preparation.pelvis_targets_z[frame_index])
        )
        for side, title in (("left", "Left"), ("right", "Right")):
            actual_z = np.asarray([
                data.geom_xpos[geom_id, 2]
                for geom_id in preparation.contact_geometry[side]["geom_ids"]
            ], dtype=float)
            target_z = preparation.sole_targets_xyz[side][frame_index, :, 2]
            for geom_index in range(4):
                row[f"{title}_contact_GEOM_{geom_index + 1}_z_after_IK"] = float(
                    actual_z[geom_index]
                )
                row[f"{title}_contact_GEOM_{geom_index + 1}_z_error_after_IK"] = float(
                    actual_z[geom_index] - target_z[geom_index]
                )
            row[f"{title}_minimum_GEOM_z_after_IK"] = float(np.min(actual_z))
        diag = result.diagnostics[frame_index]
        row["Main_IK_iterations_used"] = int(diag[3])
        row["Main_IK_converged"] = bool(diag[4])
        row["Main_IK_final_max_joint_delta_deg"] = float(diag[5])

    output["root_pos"] = np.asarray(root_pos)
    output["root_rot"] = np.asarray(root_rot)
    output["dof_pos"] = np.asarray(dof_pos)
    return output
