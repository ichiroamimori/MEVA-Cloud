# -*- coding: utf-8 -*-
"""Shared Primary-post/Main calibration for MEVA -> Robot retargeting.

This module deliberately does *not* modify the retargeted motion.
It derives two quantities from an existing Primary result:

1. Pelvis-Foot Z scale between MEVA and G1 (least-squares through origin).
2. The fixed MEVA Foot-origin-to-ground offset inherited from Primary.

MEVA source columns are fixed.  No header-name search is used for Pelvis/Foot
positions or GCP values.
"""
from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

import mujoco
import numpy as np

try:
    from .mapping_tasks import required_quaternion_columns
    from .meva_schema import (
        MEVA_GCP_COLUMN_INDICES,
        MEVA_HEADER_ROW_1BASED,
        MEVA_POSITION_COLUMN_INDICES,
    )
    from .primary_target import load_primary_target
    from .motion_io import load_motion
except ImportError:
    from mapping_tasks import required_quaternion_columns
    from meva_schema import (
        MEVA_GCP_COLUMN_INDICES,
        MEVA_HEADER_ROW_1BASED,
        MEVA_POSITION_COLUMN_INDICES,
    )
    from primary_target import load_primary_target
    from motion_io import load_motion


@dataclass(frozen=True)
class CalibrationSettings:
    geom_flatness_threshold_m: float = 0.005
    gcp_contact_threshold: float = 0.99
    gcp_smoothing_ms: float = 150.0
    gcp_min_offset: float = 0.2
    gcp_max_offset: float = 0.99
    gcp_power_number: float = 2.0


ProgressCallback = Callable[[int, int, int], None]


def _validate_settings(settings: CalibrationSettings) -> None:
    if (
        not np.isfinite(settings.geom_flatness_threshold_m)
        or settings.geom_flatness_threshold_m < 0.0
    ):
        raise ValueError("geom_flatness_threshold_m must be a finite non-negative number")
    if (
        not np.isfinite(settings.gcp_contact_threshold)
        or settings.gcp_contact_threshold < 0.0
        or settings.gcp_contact_threshold > 1.0
    ):
        raise ValueError("gcp_contact_threshold must be in [0, 1]")
    for name, value in (
        ("gcp_smoothing_ms", settings.gcp_smoothing_ms),
        ("gcp_min_offset", settings.gcp_min_offset),
        ("gcp_max_offset", settings.gcp_max_offset),
        ("gcp_power_number", settings.gcp_power_number),
    ):
        if not np.isfinite(value) or value < 0.0:
            raise ValueError(f"{name} must be a finite non-negative number")
    if settings.gcp_power_number <= 0.0:
        raise ValueError("gcp_power_number must be greater than zero")
    if not 0.0 <= settings.gcp_min_offset < settings.gcp_max_offset <= 1.0:
        raise ValueError("GCP offsets require 0 <= min_offset < max_offset <= 1")


def centered_moving_average(values: np.ndarray, window_frames: int) -> np.ndarray:
    """Average with the specified asymmetric convention for even windows."""
    values = np.asarray(values, dtype=np.float64)
    window_frames = max(1, int(window_frames))
    if window_frames % 2:
        before = after = (window_frames - 1) // 2
    else:
        before = window_frames // 2 - 1
        after = window_frames // 2
    out = np.empty_like(values)
    for i in range(len(values)):
        lo = max(0, i - before)
        hi = min(len(values), i + after + 1)
        out[i] = float(np.mean(values[lo:hi]))
    return out


def preprocess_gcp(
    values: np.ndarray,
    *,
    sampling_rate_hz: float,
    smoothing_ms: float = 150.0,
    min_offset: float = 0.2,
    max_offset: float = 0.99,
    power_number: float = 2.0,
) -> tuple[np.ndarray, np.ndarray, int]:
    """Return smoothed/corrected GCP and the effective averaging window."""
    window_frames = max(
        1,
        int(np.floor(smoothing_ms * sampling_rate_hz / 1000.0 + 0.5)),
    )
    smoothed = centered_moving_average(values, window_frames)
    normalized = np.clip(
        (smoothed - min_offset) / (max_offset - min_offset),
        0.0,
        1.0,
    )
    corrected = np.power(normalized, power_number)
    return smoothed, corrected, window_frames


def _load_pickle(path: Path) -> dict:
    obj = load_motion(path)
    if not isinstance(obj, dict):
        raise TypeError(f"Primary motion must contain dict, got {type(obj).__name__}")
    for key in ("root_pos", "root_rot", "dof_pos"):
        if key not in obj:
            raise KeyError(f"Primary motion is missing {key!r}")
    return obj


def _source_frames(motion: dict, n_frames: int) -> np.ndarray:
    src = motion.get("source_frame_indices")
    if src is None:
        return np.arange(n_frames, dtype=np.int64)
    src = np.asarray(src, dtype=np.int64)
    if src.shape != (n_frames,):
        raise ValueError("source_frame_indices length does not match Primary frame count")
    return src


def _read_selected_meva_rows(
    path: Path, source_frames: np.ndarray
) -> tuple[list[str], list[list[str]]]:
    """Read the MEVA header and selected rows, where source_frame is zero-based."""
    wanted = {int(x) for x in source_frames.tolist()}
    if not wanted:
        return [], []
    if min(wanted) < 0:
        raise ValueError("source_frame_indices contains a negative frame")

    max_required_col = max(
        max(v) for v in MEVA_POSITION_COLUMN_INDICES.values()
    )
    max_required_col = max(max_required_col, max(MEVA_GCP_COLUMN_INDICES.values()))

    found: dict[int, list[str]] = {}
    max_wanted = max(wanted)
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        for _ in range(MEVA_HEADER_ROW_1BASED - 1):
            next(reader, None)
        header = next(reader, None)
        if header is None:
            raise ValueError("MEVA CSV has no header row")
        if len(header) <= max_required_col:
            raise ValueError(
                f"MEVA CSV has only {len(header)} columns; "
                f"fixed Main analysis requires at least {max_required_col + 1}."
            )

        for row_index, row in enumerate(reader):
            if row_index > max_wanted:
                break
            if row_index not in wanted:
                continue
            if len(row) <= max_required_col:
                raise ValueError(
                    f"MEVA data row {row_index} has only {len(row)} columns; "
                    f"requires at least {max_required_col + 1}."
                )
            found[row_index] = row

    missing = sorted(wanted.difference(found))
    if missing:
        preview = missing[:10]
        suffix = "..." if len(missing) > 10 else ""
        raise IndexError(f"MEVA CSV is missing source frames {preview}{suffix}")

    # Preserve Primary frame order, even if source frames are not contiguous.
    return header, [found[int(frame)] for frame in source_frames]


def _xyz(row: list[str], name: str) -> np.ndarray:
    idx = MEVA_POSITION_COLUMN_INDICES[name]
    out = np.asarray([float(row[i]) for i in idx], dtype=np.float64)
    if not np.all(np.isfinite(out)):
        raise ValueError(f"MEVA {name} xyz contains non-finite value: {out}")
    return out


def _gcp(row: list[str], name: str) -> float:
    value = float(row[MEVA_GCP_COLUMN_INDICES[name]])
    if not np.isfinite(value):
        raise ValueError(f"MEVA GCP {name} contains non-finite value: {value}")
    return float(np.clip(value, 0.0, 1.0))


def _hinge_joints(model: mujoco.MjModel) -> list[tuple[int, int]]:
    """Return (joint_id, qpos_addr) in the exact order used by Primary output."""
    out: list[tuple[int, int]] = []
    for jid in range(model.njnt):
        if int(model.jnt_type[jid]) == int(mujoco.mjtJoint.mjJNT_HINGE):
            out.append((jid, int(model.jnt_qposadr[jid])))
    return out


def _free_joint_qpos_addr(model: mujoco.MjModel) -> int:
    free = [
        jid
        for jid in range(model.njnt)
        if int(model.jnt_type[jid]) == int(mujoco.mjtJoint.mjJNT_FREE)
    ]
    if len(free) != 1:
        raise ValueError(f"Expected one free joint, got {len(free)}")
    return int(model.jnt_qposadr[free[0]])


def _wxyz(root_rot: np.ndarray, order: str) -> np.ndarray:
    q = np.asarray(root_rot, dtype=np.float64)
    if q.shape != (4,):
        raise ValueError(f"root_rot must have 4 values, got {q.shape}")
    if order == "xyzw":
        q = q[[3, 0, 1, 2]]
    elif order != "wxyz":
        raise ValueError(f"Unsupported root_rot_order {order!r}")
    n = float(np.linalg.norm(q))
    if n < 1e-12:
        raise ValueError("root quaternion norm is zero")
    return q / n


def _qpos_from_primary_frame(
    model: mujoco.MjModel,
    motion: dict,
    frame_index: int,
    free_qadr: int,
    hinges: list[tuple[int, int]],
) -> np.ndarray:
    qpos = np.asarray(model.qpos0, dtype=np.float64).copy()
    qpos[free_qadr:free_qadr + 3] = np.asarray(motion["root_pos"])[frame_index]
    order = str(motion.get("metadata", {}).get("root_rot_order", "xyzw"))
    qpos[free_qadr + 3:free_qadr + 7] = _wxyz(
        np.asarray(motion["root_rot"])[frame_index], order
    )

    dof = np.asarray(motion["dof_pos"])[frame_index]
    if len(dof) != len(hinges):
        raise ValueError(
            f"Primary dof_pos has {len(dof)} values but robot has "
            f"{len(hinges)} hinge joints"
        )
    for value, (_, qadr) in zip(dof, hinges):
        qpos[qadr] = float(value)
    return qpos


def _mapped_link(config: dict | None, source_segment: str, fallback: str) -> str:
    if config:
        for mapping in config.get("mappings", []):
            if mapping.get("source_segment") == source_segment:
                target = mapping.get("target_link")
                if target:
                    return str(target)
    return fallback


def _body_id(model: mujoco.MjModel, name: str) -> int:
    bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, name)
    if bid < 0:
        raise KeyError(f"Robot body not found: {name}")
    return int(bid)


def foot_contact_geom_ids(model: mujoco.MjModel, foot_body_name: str) -> dict[str, int]:
    """Identify the four spherical sole-contact GEOMs on a G1 Foot body."""
    body_id = _body_id(model, foot_body_name)
    start = int(model.body_geomadr[body_id])
    count = int(model.body_geomnum[body_id])
    gids = [
        gid
        for gid in range(start, start + count)
        if int(model.geom_type[gid]) == int(mujoco.mjtGeom.mjGEOM_SPHERE)
    ]
    if len(gids) != 4:
        raise ValueError(
            f"Expected 4 spherical contact GEOMs directly on {foot_body_name}; "
            f"found {len(gids)}"
        )

    # Smaller local X = CA (heel), larger local X = FF (forefoot).
    by_x = sorted(gids, key=lambda gid: float(model.geom_pos[gid, 0]))
    ca_pair = by_x[:2]
    ff_pair = by_x[2:]

    def pair_labels(pair: Iterable[int], prefix: str) -> dict[str, int]:
        pair = list(pair)
        ypos = max(pair, key=lambda gid: float(model.geom_pos[gid, 1]))
        yneg = min(pair, key=lambda gid: float(model.geom_pos[gid, 1]))
        return {f"{prefix}_ypos": int(ypos), f"{prefix}_yneg": int(yneg)}

    out: dict[str, int] = {}
    out.update(pair_labels(ca_pair, "CA"))
    out.update(pair_labels(ff_pair, "FF"))
    return out


def contact_geom_display_name(model: mujoco.MjModel, geom_id: int) -> str:
    """Use the XML name, or an XML-attribute representation for unnamed GEOMs."""
    name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_GEOM, int(geom_id))
    if name:
        return str(name)
    pos = " ".join(f"{float(value):g}" for value in model.geom_pos[geom_id])
    if int(model.geom_type[geom_id]) == int(mujoco.mjtGeom.mjGEOM_SPHERE):
        size = f"{float(model.geom_size[geom_id, 0]):g}"
    else:
        size = " ".join(f"{float(value):g}" for value in model.geom_size[geom_id])
    return f'geom pos="{pos}" size="{size}"'


def _fit_scale_through_origin(x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]
    if len(x) == 0:
        raise ValueError("No samples for Pelvis-Foot scale fit")
    denom = float(np.dot(x, x))
    if denom < 1e-12:
        raise ValueError("Pelvis-Foot scale fit is degenerate")
    scale = float(np.dot(x, y) / denom)
    pred = scale * x
    residual = y - pred
    rmse = float(np.sqrt(np.mean(residual * residual)))
    ss_res = float(np.sum(residual * residual))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = float(1.0 - ss_res / ss_tot) if ss_tot > 1e-12 else float("nan")
    return {"scale": scale, "rmse_m": rmse, "r2": r2, "n": int(len(x))}


def analyze_main_calibration(
    *,
    primary_pkl: Path | None = None,
    primary_motion: dict | None = None,
    meva_csv: Path | None,
    primary_target_npz: Path | None = None,
    robot_xml: Path,
    settings: CalibrationSettings,
    config: dict | None = None,
    progress_callback: ProgressCallback | None = None,
) -> tuple[list[dict], dict, dict]:
    """Return analysis rows, calibration summary, and FK contact geometry."""
    _validate_settings(settings)

    if (primary_pkl is None) == (primary_motion is None):
        raise ValueError("Provide exactly one of primary_pkl or primary_motion")
    motion = _load_pickle(primary_pkl) if primary_motion is None else primary_motion
    if not isinstance(motion, dict):
        raise TypeError("primary_motion must be a dict")
    root_pos = np.asarray(motion["root_pos"], dtype=np.float64)
    root_rot = np.asarray(motion["root_rot"], dtype=np.float64)
    dof_pos = np.asarray(motion["dof_pos"], dtype=np.float64)
    n = len(root_pos)
    if root_rot.shape[0] != n or dof_pos.shape[0] != n:
        raise ValueError("Primary root_pos/root_rot/dof_pos frame counts differ")
    target = (
        load_primary_target(primary_target_npz)
        if primary_target_npz is not None and primary_target_npz.exists()
        else None
    )
    if target is None:
        if meva_csv is None:
            raise ValueError("Legacy calibration requires a MEVA CSV")
        source_frames = _source_frames(motion, n)
        meva_fields, meva_rows = _read_selected_meva_rows(meva_csv, source_frames)
    else:
        if len(target["frame"]) != n:
            raise ValueError("Primary target and Primary trajectory frame counts differ")
        source_frames = np.asarray(target["source_frame_nearest"], dtype=np.int64)
        # Canonical Main preparation reads values from Primary target arrays;
        # these transient dictionaries only feed the existing MappingTask
        # preparation and never reopen the Capsule CSV.
        source_config = dict((config or {}).get("source", {}))
        pattern = str(source_config.get(
            "quaternion_columns", "{segment}_q_gs_{component}"
        ))
        segment_names = [str(value) for value in target["segment_names"].tolist()]
        segment_index = {name: index for index, name in enumerate(segment_names)}
        meva_fields = sorted(
            pattern.format(segment=segment, component=component)
            for segment in segment_names for component in "wxyz"
        )
        meva_rows = []
        for frame_index in range(n):
            values = {
                pattern.format(segment=segment, component=component): str(float(
                    target["segment_quat"][frame_index, index, component_index]
                ))
                for segment, index in segment_index.items()
                for component_index, component in enumerate("wxyz")
            }
            meva_rows.append([values[field] for field in meva_fields])

    model = mujoco.MjModel.from_xml_path(str(robot_xml))
    data = mujoco.MjData(model)
    free_qadr = _free_joint_qpos_addr(model)
    hinges = _hinge_joints(model)

    pelvis_link = _mapped_link(config, "Pelvis", "pelvis")
    left_foot_link = _mapped_link(config, "LeftFoot", "left_ankle_roll_link")
    right_foot_link = _mapped_link(config, "RightFoot", "right_ankle_roll_link")
    pelvis_bid = _body_id(model, pelvis_link)
    left_bid = _body_id(model, left_foot_link)
    right_bid = _body_id(model, right_foot_link)
    left_geoms = foot_contact_geom_ids(model, left_foot_link)
    right_geoms = foot_contact_geom_ids(model, right_foot_link)

    fps = float(motion.get("fps", 100.0))
    rows: list[dict] = []
    meva_left_rel: list[float] = []
    meva_right_rel: list[float] = []
    g1_left_rel: list[float] = []
    g1_right_rel: list[float] = []
    left_selected_gcp: list[float] = []
    right_selected_gcp: list[float] = []
    left_contact_xyz: list[np.ndarray] = []
    right_contact_xyz: list[np.ndarray] = []
    # MuJoCo GEOM ids retain MJCF declaration order; keep that order for the
    # UI/config arrays and the pre-IK target arrays.
    left_geom_items = sorted(left_geoms.items(), key=lambda item: item[1])
    right_geom_items = sorted(right_geoms.items(), key=lambda item: item[1])

    for i, (source_frame, meva_row) in enumerate(zip(source_frames, meva_rows)):
        if target is None:
            meva_pelvis = _xyz(meva_row, "Pelvis")
            meva_left = _xyz(meva_row, "LeftFoot")
            meva_right = _xyz(meva_row, "RightFoot")
            gcp_left_ff = _gcp(meva_row, "left_ff")
            gcp_left_ca = _gcp(meva_row, "left_ca")
            gcp_right_ff = _gcp(meva_row, "right_ff")
            gcp_right_ca = _gcp(meva_row, "right_ca")
        else:
            meva_pelvis = np.asarray(target["pelvis_xyz_m"][i], dtype=np.float64)
            meva_left = np.asarray(target["left_foot_xyz_m"][i], dtype=np.float64)
            meva_right = np.asarray(target["right_foot_xyz_m"][i], dtype=np.float64)
            gcp_left_ff = float(target["gcp_left_ff"][i])
            gcp_left_ca = float(target["gcp_left_ca"][i])
            gcp_right_ff = float(target["gcp_right_ff"][i])
            gcp_right_ca = float(target["gcp_right_ca"][i])

        data.qpos[:] = _qpos_from_primary_frame(
            model, motion, i, free_qadr, hinges
        )
        mujoco.mj_forward(model, data)

        left_contact_xyz.append(np.asarray([
            data.geom_xpos[gid].copy() for _, gid in left_geom_items
        ], dtype=np.float64))
        right_contact_xyz.append(np.asarray([
            data.geom_xpos[gid].copy() for _, gid in right_geom_items
        ], dtype=np.float64))

        g1_pelvis = np.asarray(data.xpos[pelvis_bid], dtype=np.float64).copy()
        g1_left = np.asarray(data.xpos[left_bid], dtype=np.float64).copy()
        g1_right = np.asarray(data.xpos[right_bid], dtype=np.float64).copy()
        g1_pelvis_z = float(g1_pelvis[2])
        g1_left_z = float(g1_left[2])
        g1_right_z = float(g1_right[2])

        ml = float(meva_pelvis[2] - meva_left[2])
        mr = float(meva_pelvis[2] - meva_right[2])
        gl = float(g1_pelvis_z - g1_left_z)
        gr = float(g1_pelvis_z - g1_right_z)
        meva_left_rel.append(ml)
        meva_right_rel.append(mr)
        g1_left_rel.append(gl)
        g1_right_rel.append(gr)

        def shifted_geom_z(
            geom_map: dict[str, int],
            meva_foot_z: float,
            g1_foot_z: float,
        ) -> dict[str, float]:
            shift = float(meva_foot_z - g1_foot_z)
            return {
                label: float(data.geom_xpos[gid, 2]) + shift
                for label, gid in geom_map.items()
            }

        left_geom_z = shifted_geom_z(left_geoms, float(meva_left[2]), g1_left_z)
        right_geom_z = shifted_geom_z(right_geoms, float(meva_right[2]), g1_right_z)
        left_min_label = min(left_geom_z, key=left_geom_z.get)
        right_min_label = min(right_geom_z, key=right_geom_z.get)
        left_contact = "CA" if left_min_label.startswith("CA_") else "FF"
        right_contact = "CA" if right_min_label.startswith("CA_") else "FF"
        left_gcp_raw = gcp_left_ca if left_contact == "CA" else gcp_left_ff
        right_gcp_raw = gcp_right_ca if right_contact == "CA" else gcp_right_ff
        left_selected_gcp.append(left_gcp_raw)
        right_selected_gcp.append(right_gcp_raw)

        def vertical_down_angle_deg(foot: np.ndarray) -> float:
            vector = np.asarray(foot - meva_pelvis, dtype=np.float64)
            norm = float(np.linalg.norm(vector))
            if norm < 1e-12:
                return float("nan")
            cosine = float(np.clip(-vector[2] / norm, -1.0, 1.0))
            return float(np.degrees(np.arccos(cosine)))

        rows.append({
            "frame": int(i),
            "source_frame": int(source_frame),
            "source_frame_float": float(target["source_frame_float"][i]) if target is not None else float(source_frame),
            "time_s": float(target["time_s"][i]) if target is not None else float(i / fps),
            "MEVA_Pelvis_x": float(meva_pelvis[0]),
            "MEVA_Pelvis_y": float(meva_pelvis[1]),
            "MEVA_Pelvis_z": float(meva_pelvis[2]),
            "MEVA_LeftFoot_x": float(meva_left[0]),
            "MEVA_LeftFoot_y": float(meva_left[1]),
            "MEVA_LeftFoot_z": float(meva_left[2]),
            "MEVA_RightFoot_x": float(meva_right[0]),
            "MEVA_RightFoot_y": float(meva_right[1]),
            "MEVA_RightFoot_z": float(meva_right[2]),
            "MEVA_LeftFoot_GCP_FF": gcp_left_ff,
            "MEVA_LeftFoot_GCP_CA": gcp_left_ca,
            "MEVA_RightFoot_GCP_FF": gcp_right_ff,
            "MEVA_RightFoot_GCP_CA": gcp_right_ca,
            "Primary_Pelvis_x": float(g1_pelvis[0]),
            "Primary_Pelvis_y": float(g1_pelvis[1]),
            "Primary_Pelvis_z": g1_pelvis_z,
            "Primary_LeftFoot_x": float(g1_left[0]),
            "Primary_LeftFoot_y": float(g1_left[1]),
            "Primary_LeftFoot_z": g1_left_z,
            "Primary_RightFoot_x": float(g1_right[0]),
            "Primary_RightFoot_y": float(g1_right[1]),
            "Primary_RightFoot_z": g1_right_z,
            "MEVA_Pelvis_z-LeftFoot_z": ml,
            "MEVA_Pelvis_z-RightFoot_z": mr,
            "Primary_Pelvis_z-LeftFoot_z": gl,
            "Primary_Pelvis_z-RightFoot_z": gr,
            "MEVA_Left_Pelvis_to_Foot_vertical_angle_deg": vertical_down_angle_deg(
                meva_left
            ),
            "MEVA_Right_Pelvis_to_Foot_vertical_angle_deg": vertical_down_angle_deg(
                meva_right
            ),
            "Left_CA_ypos_z_at_MEVA_Foot_z": left_geom_z["CA_ypos"],
            "Left_CA_yneg_z_at_MEVA_Foot_z": left_geom_z["CA_yneg"],
            "Left_FF_ypos_z_at_MEVA_Foot_z": left_geom_z["FF_ypos"],
            "Left_FF_yneg_z_at_MEVA_Foot_z": left_geom_z["FF_yneg"],
            "Left_min_GEOM_contact": left_contact,
            "Left_selected_GCP_raw": left_gcp_raw,
            "Right_CA_ypos_z_at_MEVA_Foot_z": right_geom_z["CA_ypos"],
            "Right_CA_yneg_z_at_MEVA_Foot_z": right_geom_z["CA_yneg"],
            "Right_FF_ypos_z_at_MEVA_Foot_z": right_geom_z["FF_ypos"],
            "Right_FF_yneg_z_at_MEVA_Foot_z": right_geom_z["FF_yneg"],
            "Right_min_GEOM_contact": right_contact,
            "Right_selected_GCP_raw": right_gcp_raw,
        })

        if progress_callback is not None:
            progress_callback(i + 1, n, int(source_frame))

    # Convert milliseconds to frames using the trajectory's actual fps and
    # ordinary half-up rounding.
    left_smoothed, left_corrected, window_frames = preprocess_gcp(
        left_selected_gcp,
        sampling_rate_hz=fps,
        smoothing_ms=settings.gcp_smoothing_ms,
        min_offset=settings.gcp_min_offset,
        max_offset=settings.gcp_max_offset,
        power_number=settings.gcp_power_number,
    )
    right_smoothed, right_corrected, right_window_frames = preprocess_gcp(
        right_selected_gcp,
        sampling_rate_hz=fps,
        smoothing_ms=settings.gcp_smoothing_ms,
        min_offset=settings.gcp_min_offset,
        max_offset=settings.gcp_max_offset,
        power_number=settings.gcp_power_number,
    )
    if right_window_frames != window_frames:
        raise AssertionError("Left/right GCP windows differ")
    for i, row in enumerate(rows):
        row["Left_selected_GCP_smoothed"] = float(left_smoothed[i])
        row["Left_selected_GCP_corrected"] = float(left_corrected[i])
        row["Right_selected_GCP_smoothed"] = float(right_smoothed[i])
        row["Right_selected_GCP_corrected"] = float(right_corrected[i])

    x_left = np.asarray(meva_left_rel)
    x_right = np.asarray(meva_right_rel)
    y_left = np.asarray(g1_left_rel)
    y_right = np.asarray(g1_right_rel)
    scale_left = _fit_scale_through_origin(x_left, y_left)
    scale_right = _fit_scale_through_origin(x_right, y_right)
    scale_common = _fit_scale_through_origin(
        np.concatenate([x_left, x_right]),
        np.concatenate([y_left, y_right]),
    )

    meva_foot_z_at_ground = float(
        target["meva_foot_to_ground_offset_m"]
        if target is not None
        else (config or {}).get("foot_to_ground_offset", {}).get("meva_m", 0.030)
    )

    summary = {
        "scale_common": scale_common,
        "scale_left": scale_left,
        "scale_right": scale_right,
        "geom_flatness_threshold_m": float(settings.geom_flatness_threshold_m),
        "gcp_contact_threshold": float(settings.gcp_contact_threshold),
        "gcp_smoothing_ms": float(settings.gcp_smoothing_ms),
        "gcp_smoothing_frames": int(window_frames),
        "gcp_min_offset": float(settings.gcp_min_offset),
        "gcp_max_offset": float(settings.gcp_max_offset),
        "gcp_power_number": float(settings.gcp_power_number),
        "meva_foot_z_at_ground_m": meva_foot_z_at_ground,
        "ground_reference_method": "fixed_foot_to_ground_offset",
        "left_ground_sample_count": 0,
        "right_ground_sample_count": 0,
        "ground_sample_count_total": 0,
        "pelvis_link": pelvis_link,
        "left_foot_link": left_foot_link,
        "right_foot_link": right_foot_link,
    }
    contact_geometry = {
        # Reuse the already-selected full MEVA rows when Main builds common
        # Mapping targets.  This avoids parsing the large source CSV twice.
        "_meva_fields": meva_fields,
        "_meva_rows": meva_rows,
        "left": {
            "labels": [label for label, _ in left_geom_items],
            "display_names": [
                contact_geom_display_name(model, gid) for _, gid in left_geom_items
            ],
            "geom_ids": [int(gid) for _, gid in left_geom_items],
            "xyz": np.asarray(left_contact_xyz, dtype=np.float64),
        },
        "right": {
            "labels": [label for label, _ in right_geom_items],
            "display_names": [
                contact_geom_display_name(model, gid) for _, gid in right_geom_items
            ],
            "geom_ids": [int(gid) for _, gid in right_geom_items],
            "xyz": np.asarray(right_contact_xyz, dtype=np.float64),
        },
    }
    return rows, summary, contact_geometry


def _json_safe(value):
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    if isinstance(value, float) and not np.isfinite(value):
        return None
    return value


def _main_cli() -> None:
    parser = argparse.ArgumentParser(description="Compute Main-stage scale and MEVA ground calibration")
    parser.add_argument("--primary-pkl", type=Path, required=True)
    parser.add_argument("--meva-csv", type=Path, required=True)
    parser.add_argument("--robot-xml", type=Path, required=True)
    parser.add_argument("--config-json", type=Path)
    parser.add_argument("--geom-flatness-threshold-m", type=float, default=0.005)
    parser.add_argument("--gcp-contact-threshold", type=float, default=0.99)
    parser.add_argument("--gcp-smoothing-ms", type=float, default=150.0)
    parser.add_argument("--gcp-min-offset", type=float, default=0.2)
    parser.add_argument("--gcp-max-offset", type=float, default=0.99)
    parser.add_argument("--gcp-power-number", type=float, default=2.0)
    parser.add_argument("--output-json", type=Path)
    args = parser.parse_args()

    config = None
    if args.config_json:
        config = json.loads(args.config_json.read_text(encoding="utf-8"))

    _, summary, _ = analyze_main_calibration(
        primary_pkl=args.primary_pkl,
        meva_csv=args.meva_csv,
        robot_xml=args.robot_xml,
        settings=CalibrationSettings(
            geom_flatness_threshold_m=args.geom_flatness_threshold_m,
            gcp_contact_threshold=args.gcp_contact_threshold,
            gcp_smoothing_ms=args.gcp_smoothing_ms,
            gcp_min_offset=args.gcp_min_offset,
            gcp_max_offset=args.gcp_max_offset,
            gcp_power_number=args.gcp_power_number,
        ),
        config=config,
    )
    text = json.dumps(_json_safe(summary), ensure_ascii=False, indent=2) + "\n"
    if args.output_json:
        args.output_json.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    _main_cli()
