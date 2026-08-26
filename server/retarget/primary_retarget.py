# -*- coding: utf-8 -*-
"""Primary retarget flow: prepare targets, solve with common IK, write outputs."""
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import traceback
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from ik_solver import IKSequenceFailure, extract_output, hinge_info, solve_ik_sequence
from main_calibration import CalibrationSettings
from main_input_diagnostics import (
    build_primary_post_diagnostics,
    write_primary_post_diagnostics,
)
from motion_io import canonical_motion, save_motion_npz
from primary_prepare import prepare_primary
from primary_target import build_primary_target, load_primary_target
from primary_viewer import write_primary_viewer
from validation_data import write_stage_validation_artifacts


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def repo_root_from(path: Path):
    for candidate in [path.parent, *path.parents]:
        if (candidate / "server").exists() and (candidate / "workspace").exists():
            return candidate
    raise FileNotFoundError("repo root not found")


def next_run_dir(robot_dir: Path, setting: str, overwrite_existing: bool = False):
    if setting != "auto":
        path = robot_dir / setting
        if path.exists():
            if not overwrite_existing:
                raise FileExistsError(f"Retarget run already exists: {path}")
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=False)
        return path
    prefix = datetime.now().strftime("%y%m%d")
    vals = []
    for path in robot_dir.iterdir():
        match = re.fullmatch(prefix + r"(\d{4})", path.name)
        if path.is_dir() and match:
            vals.append(int(match.group(1)))
    path = robot_dir / f"{prefix}{(max(vals) + 1 if vals else 1):04d}"
    path.mkdir()
    return path


def _write_iteration_diagnostics(run, cfg, result):
    iteration_residuals = result.iteration_diagnostic_values
    if iteration_residuals is None:
        return
    mapped_links = [mapping["target_link"] for mapping in cfg["mappings"]]
    path = run / "iteration_orientation_residual_summary.csv"
    fieldnames = (
        ["iteration", "frames_reaching_iteration"]
        + [f"{link}_mean_error_deg" for link in mapped_links]
        + [f"{link}_p95_error_deg" for link in mapped_links]
    )
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for iteration_index in sorted(iteration_residuals):
            frame_count = max(
                (len(iteration_residuals[iteration_index][link]) for link in mapped_links),
                default=0,
            )
            if frame_count == 0:
                continue
            row = {
                "iteration": int(iteration_index),
                "frames_reaching_iteration": int(frame_count),
            }
            for link in mapped_links:
                values = np.asarray(iteration_residuals[iteration_index][link], dtype=float)
                row[f"{link}_mean_error_deg"] = float(np.mean(values)) if len(values) else ""
                row[f"{link}_p95_error_deg"] = (
                    float(np.percentile(values, 95)) if len(values) else ""
                )
            writer.writerow(row)
    print("Iteration diagnostics:", path)

    joint_deltas = result.iteration_joint_deltas
    diagnostic_hinges = result.diagnostic_hinges
    if joint_deltas is None or diagnostic_hinges is None:
        return
    joint_names = [name for name, _ in diagnostic_hinges]
    summary_path = run / "iteration_joint_delta_summary.csv"
    raw_path = run / "iteration_joint_delta_by_frame.csv"
    joint_fields = (
        [
            "iteration", "frames_reaching_iteration",
            "all_joints_mean_abs_delta_deg", "all_joints_p95_abs_delta_deg",
            "all_joints_max_abs_delta_deg",
        ]
        + [f"{name}_mean_abs_delta_deg" for name in joint_names]
        + [f"{name}_p95_abs_delta_deg" for name in joint_names]
        + [f"{name}_max_abs_delta_deg" for name in joint_names]
    )
    with summary_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=joint_fields)
        writer.writeheader()
        for iteration_index in sorted(joint_deltas):
            frame_count = max(
                (len(joint_deltas[iteration_index][name]) for name in joint_names),
                default=0,
            )
            if frame_count == 0:
                continue
            row = {"iteration": int(iteration_index), "frames_reaching_iteration": int(frame_count)}
            all_abs = np.abs(np.concatenate([
                np.asarray(joint_deltas[iteration_index][name], dtype=float)
                for name in joint_names
            ]))
            row["all_joints_mean_abs_delta_deg"] = float(np.mean(all_abs)) if len(all_abs) else 0.0
            row["all_joints_p95_abs_delta_deg"] = float(np.percentile(all_abs, 95)) if len(all_abs) else 0.0
            row["all_joints_max_abs_delta_deg"] = float(np.max(all_abs)) if len(all_abs) else 0.0
            for name in joint_names:
                values = np.abs(np.asarray(joint_deltas[iteration_index][name], dtype=float))
                row[f"{name}_mean_abs_delta_deg"] = float(np.mean(values)) if len(values) else 0.0
                row[f"{name}_p95_abs_delta_deg"] = float(np.percentile(values, 95)) if len(values) else 0.0
                row[f"{name}_max_abs_delta_deg"] = float(np.max(values)) if len(values) else 0.0
            writer.writerow(row)
    with raw_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "source_frame", "iteration", "joint_name", "delta_deg", "abs_delta_deg"
        ])
        writer.writeheader()
        writer.writerows(result.iteration_joint_delta_rows or [])
    print("Joint delta summary :", summary_path)
    print("Joint delta by frame:", raw_path)

    acceleration_rows = result.acceleration_soft_limit_rows
    if acceleration_rows is not None:
        acceleration_path = run / "iteration_acceleration_soft_limit.csv"
        with acceleration_path.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "source_frame", "joint_name", "acceleration_limit_rad_s2",
                "actual_acceleration_rad_s2", "acceleration_ratio", "soft_weight",
            ])
            writer.writeheader()
            writer.writerows(acceleration_rows)
        print("Acceleration soft limit:", acceleration_path)


def _write_primary_outputs(*, config_path, cfg, preparation, result, iteration_diagnostics):
    roots, rots, dofs = [], [], []
    for q in result.qpos:
        pos, rot, dof = extract_output(
            preparation.model, q, cfg["output"]["root_rot_order"]
        )
        roots.append(pos)
        rots.append(rot)
        dofs.append(dof)

    print()
    print("Orientation residual summary (target vs solved Mink pose)")
    print("========================================================")
    print(
        f"{'Source segment':16s}  {'Target link':28s}  "
        f"{'Weight':>6s}  {'Mean':>9s}  {'P95':>9s}  {'Max':>9s}"
    )
    print(f"{'-'*16}  {'-'*28}  {'-'*6}  {'-'*9}  {'-'*9}  {'-'*9}")
    residual_summary = {}
    for mapping in cfg["mappings"]:
        link = mapping["target_link"]
        values = np.asarray(result.diagnostic_values_by_key[link], dtype=float)
        mean_deg = float(np.mean(values)) if len(values) else 0.0
        p95_deg = float(np.percentile(values, 95)) if len(values) else 0.0
        max_deg = float(np.max(values)) if len(values) else 0.0
        residual_summary[link] = {
            "source_segment": mapping["source_segment"],
            "orientation_weight": float(mapping["orientation_weight"]),
            "mean_error_deg": mean_deg,
            "p95_error_deg": p95_deg,
            "max_error_deg": max_deg,
        }
        print(
            f"{mapping['source_segment']:16s}  {link:28s}  "
            f"{float(mapping['orientation_weight']):6.2f}  "
            f"{mean_deg:9.3f}  {p95_deg:9.3f}  {max_deg:9.3f}"
        )
    print()

    run = next_run_dir(
        config_path.parent,
        cfg["output"]["run_id"],
        overwrite_existing=bool(cfg["output"].get("overwrite_existing", False)),
    )
    snapshot = dict(cfg)
    snapshot["schema_version"] = str(snapshot.get("schema_version") or "1.0")
    snapshot["name"] = str(
        snapshot.get("name") or snapshot.get("config_name") or config_path.stem
    )
    (run / f"{run.name}_primary_config.json").write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    debug_artifacts = bool(
        iteration_diagnostics
        or cfg.get("output", {}).get("save_debug_artifacts", False)
    )
    if debug_artifacts:
        residual_rows = []
        for row in result.diagnostic_rows:
            converted = dict(row)
            converted["orientation_error_deg"] = converted.pop("value")
            residual_rows.append(converted)
        with (run / "orientation_residuals.csv").open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "source_frame", "source_segment", "target_link", "orientation_weight",
                "orientation_mode", "orientation_error_deg",
            ])
            writer.writeheader()
            writer.writerows(residual_rows)
        _write_iteration_diagnostics(run, cfg, result)

    resolved_offsets = {
        mapping["target_link"]: [
            float(x) for x in preparation.mapping_offsets[mapping["target_link"]]
        ]
        for mapping in cfg["mappings"]
    }
    settings = preparation.solver_settings
    out = {
        "root_pos": np.asarray(roots),
        "root_rot": np.asarray(rots),
        "dof_pos": np.asarray(dofs),
        "fps": float(preparation.target_fps),
        "source_frame_indices": np.asarray(preparation.source_frame_indices, dtype=np.int32),
        "source_frame_float": np.asarray(preparation.source_frame_float, dtype=np.float64),
        "time_s": np.asarray(preparation.time_s, dtype=np.float64),
        "metadata": {
            "capsule_id": cfg["capsule_id"],
            "robot": cfg["robot"],
            "root_rot_order": cfg["output"]["root_rot_order"],
            "primary_retarget": True,
            "timeline": {
                "authoritative": "time_s/source_frame_float",
                "target_fps": float(preparation.target_fps),
                "source_fps": float(cfg["source"]["sampling_rate_hz"]),
                "primary_target_npz": f"{run.name}_primary_target.npz",
            },
            "mapping_offset_method": "meva_canonical_mjcf_geometry_cached",
            "mapping_offset_asset": str(preparation.offset_path),
            "resolved_mapping_offsets_wxyz": resolved_offsets,
            "orientation_residual_summary_deg": residual_summary,
            "iteration_diagnostics_enabled": bool(iteration_diagnostics),
            "iteration_joint_delta_diagnostics_enabled": bool(iteration_diagnostics),
            "solver_convergence": {
                "max_iterations_per_frame": int(settings.max_iterations),
                "joint_delta_threshold_deg": float(settings.convergence_joint_delta_deg),
                "consecutive_iterations_required": int(
                    settings.convergence_consecutive_iterations
                ),
                "criterion": "max_abs_hinge_joint_delta_between_iterations",
            },
            "joint_velocity_limit": {
                "enabled": bool(settings.velocity_limit_enabled),
                "default_rad_s": float(settings.velocity_limit_default_rad_s),
                "reference": "previous_output_frame_final_q",
                "frame_dt_s": float(settings.output_frame_dt_s),
            },
            "interframe_joint_velocity_limit": {
                "enabled": bool(settings.velocity_limit_enabled),
                "default_rad_s": float(settings.velocity_limit_default_rad_s),
                "reference": "previous_output_frame_final_q",
                "frame_dt_s": float(settings.output_frame_dt_s),
            },
            "interframe_joint_acceleration_limit": {
                "enabled": bool(settings.acceleration_limit_enabled),
                "mode": "per_iteration_soft_boundary_task",
                "weight_at_2x_limit": float(settings.acceleration_weight_at_2x_limit),
                "limits_rad_s2": dict(settings.acceleration_limit_by_joint),
                "reference": "two_previous_output_frame_final_q",
                "frame_dt_s": float(settings.output_frame_dt_s),
            },
            "joint_limit_avoidance": {
                "enabled": bool(settings.joint_limit_avoidance.get("enabled", False)),
                "mode": "dynamic_dof_damping",
                "limit_zone_percent": float(preparation.joint_limit_zone_percent),
                "default_base_cost": float(preparation.joint_limit_base_cost),
                "default_max_cost": float(preparation.joint_limit_max_cost),
            },
            "temporal_regularization": {
                "enabled": bool(settings.temporal_regularization_enabled),
                "cost": float(settings.temporal_regularization_cost),
                "first_frame_regularized": False,
                "reference": "previous_retargeted_frame_final_q",
            },
        },
    }
    offset_settings = dict(cfg.get("foot_to_ground_offset", {}))
    diagnostics = build_primary_post_diagnostics(
        primary_motion=out,
        meva_csv=(repo_root_from(config_path) / cfg["source"]["file"]).resolve(),
        robot_xml=(repo_root_from(config_path) / cfg["robot"]["mjcf"]).resolve(),
        config=cfg,
        primary_target_npz=preparation.primary_target_path,
        calibration_settings=CalibrationSettings(
            geom_flatness_threshold_m=0.0,
            gcp_contact_threshold=0.0,
            # Corrected GCP is intentionally not persisted in this dataset.
            # Corrected GCP belongs to Main/view. These defaults are only used
            # by the shared analyzer and corrected values are not persisted.
            gcp_smoothing_ms=150.0,
            gcp_min_offset=0.2,
            gcp_max_offset=0.99,
            gcp_power_number=2.0,
        ),
        robot_foot_ground_height_m=float(offset_settings.get("robot_m", 0.035)),
    )
    final_target_path = run / f"{run.name}_primary_target.npz"
    shutil.move(str(preparation.primary_target_path), final_target_path)
    out["metadata"]["timeline"]["primary_target_npz"] = final_target_path.name
    out["metadata"]["primary_post_diagnostics"] = {
        "pelvis_foot_scale_g": diagnostics.metadata["pelvis_foot_scale_g"],
    }
    out["primary_post_root_pos"] = diagnostics.postprocessed_root_pos
    out["primary_post_pelvis_targets_z"] = diagnostics.pelvis_targets_z
    out["primary_post_pelvis_shifts_z"] = diagnostics.pelvis_shifts_z
    out["metadata"]["primary_postprocess"] = diagnostics.metadata[
        "primary_postprocess"
    ]
    # Primary's persisted motion is the post-processed motion.  root_rot and
    # dof_pos are unchanged; replacing root_pos applies the same frame-wise Z
    # translation to Pelvis, both Feet, and all contact GEOMs during FK.
    if diagnostics.metadata["primary_postprocess"]["completed"]:
        out["root_pos"] = diagnostics.postprocessed_root_pos.copy()
    joint_names = [name for _, name, _, _, _, _, _ in hinge_info(preparation.model)]
    motion_path = run / f"{run.name}_primary.npz"
    canonical = save_motion_npz(
        motion_path,
        out,
        joint_names=joint_names,
        root_rot_order=str(cfg["output"].get("root_rot_order", "xyzw")),
    )
    target = load_primary_target(final_target_path)
    viewer_path = write_primary_viewer(
        path=run / f"{run.name}_primary_viewer.bin",
        repo_root=repo_root_from(config_path),
        config=cfg,
        motion=canonical,
        target=target,
        result=result,
        mapping_offsets=preparation.mapping_offsets,
        post_diagnostics=diagnostics,
    )
    if debug_artifacts:
        primary_post_path, _ = write_primary_post_diagnostics(
            run / f"{run.name}_primary_post.csv", diagnostics
        )
        validation_metadata_path = write_stage_validation_artifacts(
            output_dir=run,
            file_id=run.name,
            stage="primary",
            repo_root=repo_root_from(config_path),
            config=cfg,
            motion=out,
        )
        print("Primary post debug data:", primary_post_path)
        print("Primary frame validation debug data:", validation_metadata_path)
    if debug_artifacts and cfg["output"].get("save_diagnostics_csv", True):
        with (run / "diagnostics.csv").open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "source_frame", "max_joint_limit_cost", "max_orientation_error_deg",
                "iterations_used", "converged", "final_max_joint_delta_deg",
            ])
            writer.writerows(result.diagnostics)
    converged_count = sum(1 for row in result.diagnostics if bool(row[4]))
    print(
        "Convergence:",
        f"{converged_count}/{len(result.diagnostics)} frames converged before/at the ceiling",
        f"(max_iterations={settings.max_iterations}, "
        f"delta_threshold={settings.convergence_joint_delta_deg:g} deg)",
    )
    print("Done:", run)
    print("Primary target:", final_target_path)
    print("Primary motion:", motion_path)
    print("Primary viewer:", viewer_path)
    print("dof_pos shape:", out["dof_pos"].shape)
    return run, out


def _write_primary_failure_outputs(
    *, config_path: Path, cfg: dict, preparation, failure: IKSequenceFailure,
    initial_q: np.ndarray,
) -> Path:
    run_id = str(cfg["output"]["run_id"])
    run = next_run_dir(
        config_path.parent, run_id,
        overwrite_existing=bool(cfg["output"].get("overwrite_existing", False)),
    )
    total = len(preparation.frame_specs)
    completed = len(failure.result.qpos)
    fallback = (
        np.asarray(failure.result.qpos[-1], dtype=float)
        if completed else np.asarray(initial_q, dtype=float)
    )
    qpos = []
    for index, frame_spec in enumerate(preparation.frame_specs):
        if index < completed:
            qpos.append(failure.result.qpos[index])
        elif frame_spec.initial_q is not None:
            qpos.append(np.asarray(frame_spec.initial_q, dtype=float))
        else:
            qpos.append(fallback.copy())
    frame_status = np.full(total, 3, dtype=np.uint8)
    frame_status[:completed] = np.asarray(
        [0 if bool(row[4]) else 1 for row in failure.result.diagnostics],
        dtype=np.uint8,
    )
    frame_status[failure.output_index] = 2
    diagnostics = list(failure.result.diagnostics)
    for index in range(completed, total):
        diagnostics.append((
            int(preparation.frame_specs[index].source_frame),
            0.0, 0.0, 0, False, 0.0,
        ))
    diagnostic_values = {
        key: list(values) + [0.0] * (total - len(values))
        for key, values in failure.result.diagnostic_values_by_key.items()
    }
    partial_result = replace(
        failure.result, qpos=np.asarray(qpos), diagnostics=diagnostics,
        diagnostic_values_by_key=diagnostic_values,
    )
    roots, rotations, joints = [], [], []
    root_order = str(cfg["output"].get("root_rot_order", "xyzw"))
    for q in partial_result.qpos:
        pos, rot, dof = extract_output(preparation.model, q, root_order)
        roots.append(pos);rotations.append(rot);joints.append(dof)
    motion = canonical_motion({
        "root_pos": np.asarray(roots),
        "root_rot": np.asarray(rotations),
        "dof_pos": np.asarray(joints),
        "fps": float(preparation.target_fps),
        "source_frame_indices": np.asarray(preparation.source_frame_indices, dtype=np.int32),
        "source_frame_float": np.asarray(preparation.source_frame_float, dtype=np.float64),
        "time_s": np.asarray(preparation.time_s, dtype=np.float64),
    }, joint_names=[name for _, name, _, _, _, _, _ in hinge_info(preparation.model)],
       root_rot_order=root_order)
    frame_errors = [{
        "frame_index": failure.output_index,
        "source_frame": failure.source_frame,
        "status": "solver error",
        "error": str(failure),
    }]
    snapshot = dict(cfg)
    snapshot["schema_version"] = str(snapshot.get("schema_version") or "1.0")
    snapshot["name"] = str(
        snapshot.get("name") or snapshot.get("config_name") or config_path.stem
    )
    snapshot["run_status"] = "partial"
    snapshot["primary_runtime_context"] = {
        "capsule_id": cfg.get("capsule_id"),
        "fps": float(preparation.target_fps),
        "frame_count": total,
        "completed_frame_count": completed,
        "failed_output_frame": failure.output_index,
        "failed_source_frame": failure.source_frame,
        "frame_range": cfg.get("frame_range", {}),
    }
    snapshot["frame_errors"] = frame_errors
    (run / f"{run_id}_primary_config.json").write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    target = load_primary_target(preparation.primary_target_path)
    write_primary_viewer(
        path=run / f"{run_id}_primary_viewer.bin",
        repo_root=repo_root_from(config_path), config=snapshot,
        motion=motion, target=target, result=partial_result,
        mapping_offsets=preparation.mapping_offsets, post_diagnostics=None,
        frame_status=frame_status, frame_errors=frame_errors,
    )
    (run / f"{run_id}_error.log").write_text(
        "\n".join((
            f"timestamp_utc: {datetime.now(timezone.utc).isoformat()}",
            f"capsule_id: {cfg.get('capsule_id', '')}",
            f"primary_id: {run_id}",
            f"completed_frames: {completed} / {total}",
            f"failed_output_frame: {failure.output_index}",
            f"failed_source_frame: {failure.source_frame}",
            f"error: {type(failure).__name__}: {failure}",
            "", "traceback:", "".join(traceback.format_exception(failure)),
        )) + "\n",
        encoding="utf-8",
    )
    preparation.primary_target_path.unlink(missing_ok=True)
    print(f"Primary partial viewer: {run / f'{run_id}_primary_viewer.bin'}", flush=True)
    print(f"Primary error log: {run / f'{run_id}_error.log'}", flush=True)
    return run


def main(config_path: Path, iteration_diagnostics: bool = False):
    config_path = config_path.resolve()
    cfg = load_json(config_path)
    run_id = str(cfg.get("output", {}).get("run_id", "auto"))
    if run_id == "auto":
        raise ValueError("Primary target generation requires an allocated run ID")
    primary_target_path = config_path.parent / f".{run_id}_primary_target.npz"
    build_primary_target(
        cfg=cfg,
        repo_root=repo_root_from(config_path),
        output_path=primary_target_path,
    )
    preparation = prepare_primary(
        config_path=config_path,
        cfg=cfg,
        repo_root=repo_root_from(config_path),
        primary_target_path=primary_target_path,
        iteration_diagnostics=iteration_diagnostics,
    )
    initial_q = preparation.initial_configuration.q.copy()
    try:
        result = solve_ik_sequence(
            model=preparation.model,
            initial_configuration=preparation.initial_configuration,
            frame_specs=preparation.frame_specs,
            solver_settings=preparation.solver_settings,
            diagnostic_keys=preparation.diagnostic_keys,
        )
    except IKSequenceFailure as failure:
        _write_primary_failure_outputs(
            config_path=config_path, cfg=cfg, preparation=preparation,
            failure=failure, initial_q=initial_q,
        )
        raise RuntimeError(str(failure)) from failure
    return _write_primary_outputs(
        config_path=config_path,
        cfg=cfg,
        preparation=preparation,
        result=result,
        iteration_diagnostics=iteration_diagnostics,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    parser.add_argument(
        "--iteration-diagnostics",
        action="store_true",
        help=(
            "Write per-iteration orientation residuals and hinge-joint "
            "delta diagnostics."
        ),
    )
    args = parser.parse_args()
    main(args.config, iteration_diagnostics=args.iteration_diagnostics)
