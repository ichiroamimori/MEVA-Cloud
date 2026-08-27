# -*- coding: utf-8 -*-
"""Final Main-stage World-XY placement from persistent foot-contact anchors.

This module is deliberately not an IK stage.  It treats every solved Main pose
as a rigid articulated configuration and changes only the free-joint World X/Y
translation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import mujoco
import numpy as np

from support_state import SupportState, main_support_side


@dataclass(frozen=True)
class GlobalContactAnchoringSettings:
    enabled: bool = True


@dataclass
class FootAnchorState:
    active: bool = False
    geom_index: int | None = None
    geom_id: int | None = None
    anchor_world_xy: np.ndarray | None = None


@dataclass
class PostprocessResult:
    qpos: np.ndarray
    diagnostics: list[dict[str, Any]]
    validation: dict[str, float]
    state_counts: dict[str, int] = field(default_factory=dict)


def _validate_settings(settings: GlobalContactAnchoringSettings) -> None:
    if not isinstance(settings.enabled, bool):
        raise ValueError("Global Contact Anchoring enabled must be boolean")


def _free_joint(model: mujoco.MjModel) -> tuple[int, int, int]:
    free_joints = [
        joint_id
        for joint_id in range(model.njnt)
        if int(model.jnt_type[joint_id]) == int(mujoco.mjtJoint.mjJNT_FREE)
    ]
    if len(free_joints) != 1:
        raise ValueError(f"Expected exactly one free joint, found {free_joints}")
    joint_id = free_joints[0]
    return (
        joint_id,
        int(model.jnt_qposadr[joint_id]),
        int(model.jnt_bodyid[joint_id]),
    )


def _hinge_qpos_addresses(model: mujoco.MjModel) -> list[int]:
    return [
        int(model.jnt_qposadr[joint_id])
        for joint_id in range(model.njnt)
        if int(model.jnt_type[joint_id]) == int(mujoco.mjtJoint.mjJNT_HINGE)
    ]


def _blank_or_float(value: float | None) -> float | str:
    return "" if value is None else float(value)


def apply_global_contact_anchoring(
    *,
    model: mujoco.MjModel,
    qpos: np.ndarray,
    rows: list[dict[str, Any]],
    contact_geometry: dict[str, Any],
    settings: GlobalContactAnchoringSettings,
) -> PostprocessResult:
    """Anchor the saved Support State's main foot in World XY only."""
    _validate_settings(settings)
    raw_qpos = np.asarray(qpos, dtype=np.float64)
    if raw_qpos.ndim != 2 or raw_qpos.shape[1] != model.nq:
        raise ValueError(f"Expected qpos shape (frames, {model.nq}), got {raw_qpos.shape}")
    if len(rows) != len(raw_qpos):
        raise ValueError("Main rows and IK qpos frame counts differ")

    _, free_qadr, free_body_id = _free_joint(model)
    hinge_qadrs = _hinge_qpos_addresses(model)
    sides = (("left", "Left"), ("right", "Right"))
    support_names = {
        side: [str(value) for value in contact_geometry[side]["display_names"]]
        for side, _ in sides
    }
    if any(len(support_names[side]) != 4 for side, _ in sides):
        raise ValueError("Each Foot Contact Anchoring input requires four Support Points")

    def support_xyz(side: str, data: mujoco.MjData) -> np.ndarray:
        geometry = contact_geometry[side]
        body_id = int(geometry["body_id"])
        rotation = np.asarray(data.xmat[body_id], dtype=np.float64).reshape(3, 3)
        return (
            np.asarray(data.xpos[body_id], dtype=np.float64)[None, :]
            + np.asarray(geometry["local_positions"], dtype=np.float64) @ rotation.T
        )

    post_qpos = raw_qpos.copy()
    active_side: str | None = None
    anchor = FootAnchorState()
    global_translation = np.zeros(2, dtype=np.float64)
    diagnostics: list[dict[str, Any]] = []
    state_counts = {state.name: 0 for state in SupportState}
    data = mujoco.MjData(model)
    max_pelvis_z_diff = 0.0
    max_contact_geom_z_diff = 0.0
    max_anchor_error = 0.0

    for frame_index, (raw_q, row) in enumerate(zip(raw_qpos, rows)):
        state = SupportState(int(row["Support_State"]))
        state_counts[state.name] += 1
        requested_side = main_support_side(state) if settings.enabled else None
        data.qpos[:] = raw_q
        mujoco.mj_forward(model, data)
        raw_pelvis_z = float(data.xpos[free_body_id, 2])
        raw_xyz = {
            side: support_xyz(side, data)
            for side, _ in sides
        }
        minimum_index = {
            side: int(np.argmin(raw_xyz[side][:, 2])) for side, _ in sides
        }

        if requested_side != active_side:
            active_side = requested_side
            anchor = FootAnchorState()
            if active_side is not None:
                min_index = minimum_index[active_side]
                anchor.active = True
                anchor.geom_index = min_index
                anchor.anchor_world_xy = (
                    raw_xyz[active_side][min_index, :2] + global_translation
                ).copy()

        required_translation = {"left": None, "right": None}
        if active_side is not None:
            if anchor.geom_index is None or anchor.anchor_world_xy is None:
                raise RuntimeError("Active Support State anchor is incomplete")
            required_translation[active_side] = (
                anchor.anchor_world_xy
                - raw_xyz[active_side][anchor.geom_index, :2]
            )
            global_translation = required_translation[active_side].copy()
        # FLYING (when enabled by a future non-zero maximum) keeps the previous
        # translation but creates no fixed side.

        post_qpos[frame_index, free_qadr:free_qadr + 2] = (
            raw_q[free_qadr:free_qadr + 2] + global_translation
        )
        data.qpos[:] = post_qpos[frame_index]
        mujoco.mj_forward(model, data)
        post_pelvis_z = float(data.xpos[free_body_id, 2])
        post_xyz = {
            side: support_xyz(side, data)
            for side, _ in sides
        }
        max_pelvis_z_diff = max(max_pelvis_z_diff, abs(post_pelvis_z - raw_pelvis_z))
        for side, _ in sides:
            max_contact_geom_z_diff = max(
                max_contact_geom_z_diff,
                float(np.max(np.abs(post_xyz[side][:, 2] - raw_xyz[side][:, 2]))),
            )

        anchor_error = None
        if active_side is not None and anchor.geom_index is not None and anchor.anchor_world_xy is not None:
            anchor_error = post_xyz[active_side][anchor.geom_index, :2] - anchor.anchor_world_xy
            max_anchor_error = max(max_anchor_error, float(np.max(np.abs(anchor_error))))

        diag: dict[str, Any] = {
            "Global_contact_state": state.name,
            "Global_translation_x": float(global_translation[0]),
            "Global_translation_y": float(global_translation[1]),
            "Left_weight": "",
            "Right_weight": "",
        }
        for side, title in sides:
            min_index = minimum_index[side]
            required = required_translation[side]
            side_active = side == active_side
            error = anchor_error if side_active else None
            diag.update({
                f"{title}_contact_active": side_active,
                f"{title}_corrected_GCP": float(row[f"{title}_corrected_GCP"]),
                f"{title}_minimum_GEOM_name": support_names[side][min_index],
                f"{title}_minimum_GEOM_z": float(raw_xyz[side][min_index, 2]),
                f"{title}_anchor_GEOM_name": (
                    support_names[side][anchor.geom_index]
                    if side_active and anchor.geom_index is not None else ""
                ),
                f"{title}_anchor_world_x": _blank_or_float(
                    None if not side_active or anchor.anchor_world_xy is None else anchor.anchor_world_xy[0]
                ),
                f"{title}_anchor_world_y": _blank_or_float(
                    None if not side_active or anchor.anchor_world_xy is None else anchor.anchor_world_xy[1]
                ),
                f"{title}_required_translation_x": _blank_or_float(None if required is None else required[0]),
                f"{title}_required_translation_y": _blank_or_float(None if required is None else required[1]),
                f"{title}_anchor_error_x_after": _blank_or_float(None if error is None else error[0]),
                f"{title}_anchor_error_y_after": _blank_or_float(None if error is None else error[1]),
            })
        diagnostics.append(diag)

    validation = {
        "max_abs_root_z_diff": float(np.max(np.abs(
            post_qpos[:, free_qadr + 2] - raw_qpos[:, free_qadr + 2]
        ))) if len(raw_qpos) else 0.0,
        "max_abs_root_quaternion_diff": float(np.max(np.abs(
            post_qpos[:, free_qadr + 3:free_qadr + 7]
            - raw_qpos[:, free_qadr + 3:free_qadr + 7]
        ))) if len(raw_qpos) else 0.0,
        "max_abs_hinge_qpos_diff": float(np.max(np.abs(
            post_qpos[:, hinge_qadrs] - raw_qpos[:, hinge_qadrs]
        ))) if len(raw_qpos) and hinge_qadrs else 0.0,
        "max_abs_pelvis_world_z_diff": float(max_pelvis_z_diff),
        "max_abs_contact_geom_z_diff": float(max_contact_geom_z_diff),
        "max_abs_single_support_anchor_xy_error": float(max_anchor_error),
        "max_abs_global_translation_xy": float(np.max(np.abs(
            post_qpos[:, free_qadr:free_qadr + 2]
            - raw_qpos[:, free_qadr:free_qadr + 2]
        ))) if len(raw_qpos) else 0.0,
    }
    return PostprocessResult(
        qpos=post_qpos,
        diagnostics=diagnostics,
        validation=validation,
        state_counts=state_counts,
    )
