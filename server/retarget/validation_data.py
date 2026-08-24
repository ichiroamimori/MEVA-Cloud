# -*- coding: utf-8 -*-
"""Precomputed frame validation artifacts for Retargeting result views.

All FK, MuJoCo collision distance, threshold evaluation, and severity
calculation lives here. The browser only transposes persisted wide CSVs and
applies the shared severity color LUT.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import mujoco
import numpy as np

try:
    from .robot_model_info import collision_pair_descriptors, joint_descriptors
except ImportError:
    from robot_model_info import collision_pair_descriptors, joint_descriptors


FORMAT_VERSION = 1


def _set_qpos(model, data, motion, frame: int, order: str, hinges):
    data.qpos[:] = model.qpos0
    free = next(jid for jid in range(model.njnt) if model.jnt_type[jid] == mujoco.mjtJoint.mjJNT_FREE)
    address = int(model.jnt_qposadr[free])
    data.qpos[address:address + 3] = motion["root_pos"][frame]
    rotation = np.asarray(motion["root_rot"][frame], dtype=float)
    data.qpos[address + 3:address + 7] = rotation[[3, 0, 1, 2]] if order == "xyzw" else rotation
    for index, joint in enumerate(hinges):
        data.qpos[joint["qpos_address"]] = motion["dof_pos"][frame][index]
    mujoco.mj_forward(model, data)


def joint_limit_severity(margin_rad: float, zone_rad: float) -> int:
    """Continuous severity: 2x zone=blue, zone=yellow, limit=red."""
    if zone_rad <= 0.0:
        return 255 if margin_rad <= 0.0 else 0
    if margin_rad >= 2.0 * zone_rad:
        return 0
    if margin_rad >= zone_rad:
        t = (2.0 * zone_rad - margin_rad) / zone_rad
        return int(np.clip(np.rint(191.0 * t), 0, 191))
    if margin_rad > 0.0:
        t = (zone_rad - margin_rad) / zone_rad
        return int(np.clip(np.rint(191.0 + 64.0 * t), 191, 255))
    return 255


def self_collision_severity(distance_m: float, damping_zone_m: float) -> int:
    """Self-collision deliberately uses only blue/yellow/red LUT entries."""
    if distance_m < 0.0:
        return 255
    if distance_m < damping_zone_m:
        return 191
    return 0


def _write_wide_csv(path: Path, frames: list[int], columns: list[str], values: np.ndarray, *, integer: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["frame", *columns])
        for frame, row in zip(frames, values):
            cells = [int(x) for x in row] if integer else [format(float(x), ".12g") for x in row]
            writer.writerow([int(frame), *cells])


def write_stage_validation_artifacts(*, output_dir: Path, file_id: str, stage: str, repo_root: Path, config: dict[str, Any], motion: dict[str, Any]) -> Path:
    """Compute and persist all frame-view values immediately after a stage."""
    xml_path = (repo_root / str(config["robot"]["mjcf"])).resolve()
    model = mujoco.MjModel.from_xml_path(str(xml_path))
    data = mujoco.MjData(model)
    joints = joint_descriptors(model)
    hinges = [item for item in joints if item["type"] == int(mujoco.mjtJoint.mjJNT_HINGE)]
    limited_hinges = [item for item in hinges if item["limited"]]
    frame_count = int(len(motion["root_pos"]))
    # Validation matrices share the local trajectory time line.  MEVA source
    # frame mapping is metadata, not the matrix column coordinate.
    frames = np.arange(frame_count, dtype=int).tolist()
    order = motion.get("metadata", {}).get("root_rot_order") or config.get("output", {}).get("root_rot_order", "xyzw")

    joint_cfg = dict(config.get("joint_limit_avoidance", {}))
    default_zone_percent = float(joint_cfg.get("default", {}).get("limit_zone_percent", 10.0))
    joint_columns = [f"joint_{index:03d}" for index in range(1, len(limited_hinges) + 1)]
    joint_actual = np.empty((frame_count, len(limited_hinges)), dtype=float)
    joint_margin = np.empty_like(joint_actual)
    joint_severity = np.empty_like(joint_actual, dtype=np.uint8)
    joint_metadata = []
    for column, joint in zip(joint_columns, limited_hinges):
        override = dict(joint_cfg.get("overrides", {}).get(joint["name"], {}))
        zone_percent = float(override.get("limit_zone_percent", default_zone_percent))
        lo, hi = map(float, joint["range"])
        zone_rad = max(0.0, (hi - lo) * zone_percent / 100.0)
        joint_metadata.append({
            "column": column, "key": joint["name"], "label": joint["name"],
            "lower_limit_rad": lo, "upper_limit_rad": hi,
            "limit_zone_percent": zone_percent, "limit_zone_rad": zone_rad,
        })

    collision_cfg = dict(config.get("self_collision_avoidance", {}))
    damping_cfg = dict(collision_cfg.get("damping", {}))
    if "limit_zone_m" not in damping_cfg:
        raise ValueError("Primary config is missing self_collision_avoidance.damping.limit_zone_m")
    collision_zone = float(damping_cfg["limit_zone_m"])
    if not np.isfinite(collision_zone) or collision_zone < 0.0:
        raise ValueError("Self-collision damping Limit zone must be non-negative")
    pairs = collision_pair_descriptors(model, xml_path)
    pair_columns = [f"pair_{index:03d}" for index in range(1, len(pairs) + 1)]
    pair_distance = np.empty((frame_count, len(pairs)), dtype=float)
    pair_severity = np.empty_like(pair_distance, dtype=np.uint8)
    pair_metadata = [{
        "column": column, "key": pair["key"], "label": pair["label"],
        "geom_a_id": pair["geom_a_id"], "geom_b_id": pair["geom_b_id"],
    } for column, pair in zip(pair_columns, pairs)]

    mapped = {str(item.get("source_segment")): str(item.get("target_link")) for item in config.get("mappings", [])}
    foot_entries = []
    for side, segment in (("left", "LeftFoot"), ("right", "RightFoot")):
        body_name = mapped.get(segment)
        body_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, body_name) if body_name else -1
        geom_ids = [gid for gid in range(model.ngeom) if int(model.geom_bodyid[gid]) == body_id and (int(model.geom_contype[gid]) or int(model.geom_conaffinity[gid]))][:4]
        for index, geom_id in enumerate(geom_ids, 1):
            foot_entries.append({"column": f"{side}_geom_{index}", "side": side, "geom_id": geom_id, "label": f"{side.title()} Foot GEOM {index} Z"})
        foot_entries.append({"column": f"{side}_minimum", "side": side, "geom_id": None, "label": f"{side.title()} Foot GEOM MIN Z", "source_geom_ids": geom_ids})
    foot_columns = [entry["column"] for entry in foot_entries]
    foot_z = np.empty((frame_count, len(foot_entries)), dtype=float)

    for frame_index in range(frame_count):
        _set_qpos(model, data, motion, frame_index, order, hinges)
        for joint_index, joint in enumerate(limited_hinges):
            q = float(data.qpos[joint["qpos_address"]])
            lo, hi = map(float, joint["range"])
            margin = min(q - lo, hi - q)
            zone = float(joint_metadata[joint_index]["limit_zone_rad"])
            joint_actual[frame_index, joint_index] = q
            joint_margin[frame_index, joint_index] = margin
            joint_severity[frame_index, joint_index] = joint_limit_severity(margin, zone)
        for pair_index, pair in enumerate(pairs):
            distance = float(mujoco.mj_geomDistance(model, data, int(pair["geom_a_id"]), int(pair["geom_b_id"]), 1e6, np.empty(6, dtype=float)))
            pair_distance[frame_index, pair_index] = distance
            pair_severity[frame_index, pair_index] = self_collision_severity(distance, collision_zone)
        for entry_index, entry in enumerate(foot_entries):
            if entry["geom_id"] is not None:
                value = float(data.geom_xpos[int(entry["geom_id"]), 2])
            else:
                source_ids = entry["source_geom_ids"]
                value = min(float(data.geom_xpos[int(gid), 2]) for gid in source_ids) if source_ids else np.nan
            foot_z[frame_index, entry_index] = value

    prefix = f"{file_id}_{stage}_validation"
    files = {
        "joint_limit_severity": f"{prefix}_joint_limit_severity.csv",
        "joint_limit_actual": f"{prefix}_joint_limit_actual_rad.csv",
        "joint_limit_margin": f"{prefix}_joint_limit_margin_rad.csv",
        "self_collision_severity": f"{prefix}_self_collision_severity.csv",
        "self_collision_distance": f"{prefix}_self_collision_signed_distance_m.csv",
        "foot_geom_z": f"{prefix}_foot_geom_z_m.csv",
    }
    _write_wide_csv(output_dir / files["joint_limit_severity"], frames, joint_columns, joint_severity, integer=True)
    _write_wide_csv(output_dir / files["joint_limit_actual"], frames, joint_columns, joint_actual)
    _write_wide_csv(output_dir / files["joint_limit_margin"], frames, joint_columns, joint_margin)
    _write_wide_csv(output_dir / files["self_collision_severity"], frames, pair_columns, pair_severity, integer=True)
    _write_wide_csv(output_dir / files["self_collision_distance"], frames, pair_columns, pair_distance)
    _write_wide_csv(output_dir / files["foot_geom_z"], frames, foot_columns, foot_z)

    metadata = {
        "format": "MEVA Frame Validation Wide CSV", "format_version": FORMAT_VERSION,
        "stage": stage, "file_id": file_id, "frame_count": frame_count,
        "frame_column": "frame", "severity_range": [0, 255], "files": files,
        "joint_limit": {"columns": joint_metadata, "severity_formula": "piecewise continuous: 2x zone=0, 1x zone=191, limit/violation=255", "actual_unit": "rad", "margin_unit": "rad"},
        "self_collision": {"columns": pair_metadata, "damping_limit_zone_m": collision_zone, "severity_values": {"safe": 0, "damping_zone": 191, "penetration": 255}, "severity_formula": "d < 0:255; 0 <= d < D:191; d >= D:0", "raw_unit": "m"},
        "foot_geom": {"columns": foot_entries, "raw_unit": "m"},
    }
    metadata_path = output_dir / f"{prefix}.json"
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return metadata_path


def validation_metadata_path(run_dir: Path, run_id: str, stage: str, main_id: str = "legacy") -> Path:
    if stage == "main" and main_id != "legacy":
        preferred = run_dir / main_id
        legacy = run_dir / "main" / main_id
        result_dir = preferred if preferred.exists() or not legacy.exists() else legacy
        return result_dir / f"{main_id}_main_validation.json"
    return run_dir / f"{run_id}_{stage}_validation.json"
