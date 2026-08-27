# -*- coding: utf-8 -*-
"""
modify_z.py

Pipeline
--------
1. Load primary.pkl and fixed-layout MEVA CSV.
2. Compute one scale factor s between MEVA and G1 Pelvis-Foot world-Z differences:
       G1_rel_z ~= s * MEVA_rel_z
   using left + right feet together, least-squares through the origin.
3. For every primary frame:
   a. Find the lowest surface point among the 8 foot contact spheres
      (4 left + 4 right).
   b. Shift the whole robot in world Z so that this lowest point is z=0.
   c. Use the shifted primary pose as the initial Mink configuration.
   d. Solve only the world-Z differences:
          LeftFoot_z  - Pelvis_z = s * (MEVA_LeftFoot_z  - MEVA_Pelvis_z)
          RightFoot_z - Pelvis_z = s * (MEVA_RightFoot_z - MEVA_Pelvis_z)
      with relative-Z cost 0.8 by default.
   e. A weak PostureTask keeps the solution close to primary joint angles.
4. Save z_modified.pkl and diagnostics CSV.

Fixed MEVA CSV layout
---------------------
Header row: 8
Data starts: row 9

BF = LeftFoot_z   -> zero-based index 57
LY = Pelvis_z     -> zero-based index 336
NK = RightFoot_z  -> zero-based index 374

Notes
-----
- Pelvis/Foot Z differences are WORLD-Z differences, not Pelvis-local Z.
- Root/global Z translation cancels from the custom relative-Z task, so the
  ground-placement shift is not used to satisfy the relative-Z constraint.
- Final re-grounding after IK is OFF by default. Diagnostics report the final
  lowest contact Z so this can be judged before enabling it.
"""

from __future__ import annotations

import argparse
import csv
import json
import pickle
from pathlib import Path
from typing import Dict, List, Tuple

import mujoco
import numpy as np
import mink
from mink.tasks.task import Task


# ============================================================================
# Fixed MEVA layout
# ============================================================================

MEVA_DATA_START_ROW = 9

COL_LEFT_FOOT_Z = 57    # BF
COL_PELVIS_Z = 336      # LY
COL_RIGHT_FOOT_Z = 374  # NK

REQUIRED_MAX_COL = COL_RIGHT_FOOT_Z


# ============================================================================
# Robot frame names
# ============================================================================

PELVIS_BODY = "pelvis"
LEFT_FOOT_BODY = "left_ankle_roll_link"
RIGHT_FOOT_BODY = "right_ankle_roll_link"


# ============================================================================
# Utilities
# ============================================================================

def load_pickle(path: Path) -> Dict:
    with path.open("rb") as f:
        obj = pickle.load(f)
    if not isinstance(obj, dict):
        raise TypeError(f"Expected dict in PKL: {path}")
    return obj


def save_pickle(path: Path, obj: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        pickle.dump(obj, f)


def xyzw_to_wxyz(q: np.ndarray) -> np.ndarray:
    return np.asarray([q[3], q[0], q[1], q[2]], dtype=float)


def wxyz_to_xyzw(q: np.ndarray) -> np.ndarray:
    return np.asarray([q[1], q[2], q[3], q[0]], dtype=float)


def normalize_quat(q: np.ndarray) -> np.ndarray:
    q = np.asarray(q, dtype=float)
    n = np.linalg.norm(q)
    if n <= 0.0:
        raise ValueError("Zero-length quaternion.")
    return q / n


def get_free_joint_qpos_address(model: mujoco.MjModel) -> int:
    ids = np.where(model.jnt_type == mujoco.mjtJoint.mjJNT_FREE)[0]
    if len(ids) != 1:
        raise ValueError(
            f"Expected exactly one free joint, found {len(ids)}."
        )
    return int(model.jnt_qposadr[int(ids[0])])


def actuator_joint_ids(model: mujoco.MjModel) -> np.ndarray:
    ids = np.asarray(model.actuator_trnid[:, 0], dtype=int)
    if np.any(ids < 0):
        raise ValueError("Could not resolve actuator joint IDs.")
    return ids


def motion_frame_to_qpos(
    model: mujoco.MjModel,
    root_pos: np.ndarray,
    root_rot: np.ndarray,
    dof_pos: np.ndarray,
    root_rot_order: str,
    joint_ids: np.ndarray,
) -> np.ndarray:
    q = model.qpos0.copy()

    free_qadr = get_free_joint_qpos_address(model)
    q[free_qadr:free_qadr + 3] = root_pos

    if root_rot_order.lower() == "xyzw":
        root_q_wxyz = xyzw_to_wxyz(root_rot)
    elif root_rot_order.lower() == "wxyz":
        root_q_wxyz = np.asarray(root_rot, dtype=float)
    else:
        raise ValueError(f"Unsupported root_rot_order: {root_rot_order}")

    q[free_qadr + 3:free_qadr + 7] = normalize_quat(root_q_wxyz)

    if len(dof_pos) != len(joint_ids):
        raise ValueError(
            f"dof_pos has {len(dof_pos)} values but model has "
            f"{len(joint_ids)} actuated joints."
        )

    for value, joint_id in zip(dof_pos, joint_ids):
        qadr = int(model.jnt_qposadr[int(joint_id)])
        q[qadr] = float(value)

    return q


def qpos_to_motion_frame(
    model: mujoco.MjModel,
    q: np.ndarray,
    joint_ids: np.ndarray,
    root_rot_order: str,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    free_qadr = get_free_joint_qpos_address(model)

    root_pos = np.asarray(q[free_qadr:free_qadr + 3], dtype=float).copy()
    root_q_wxyz = normalize_quat(
        np.asarray(q[free_qadr + 3:free_qadr + 7], dtype=float)
    )

    if root_rot_order.lower() == "xyzw":
        root_rot = wxyz_to_xyzw(root_q_wxyz)
    elif root_rot_order.lower() == "wxyz":
        root_rot = root_q_wxyz.copy()
    else:
        raise ValueError(f"Unsupported root_rot_order: {root_rot_order}")

    dof = np.asarray(
        [q[int(model.jnt_qposadr[int(jid)])] for jid in joint_ids],
        dtype=float,
    )

    return root_pos, root_rot, dof


# ============================================================================
# MEVA fixed-column reader
# ============================================================================

def read_meva_z_fixed(path: Path) -> Dict[str, np.ndarray]:
    pelvis = []
    left_foot = []
    right_foot = []

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)

        for row_number, row in enumerate(reader, start=1):
            if row_number < MEVA_DATA_START_ROW:
                continue

            if not row or not any(cell.strip() for cell in row):
                continue

            if len(row) <= REQUIRED_MAX_COL:
                raise ValueError(
                    f"MEVA CSV row {row_number} has only {len(row)} columns; "
                    f"at least {REQUIRED_MAX_COL + 1} are required."
                )

            try:
                left_foot.append(float(row[COL_LEFT_FOOT_Z]))
                pelvis.append(float(row[COL_PELVIS_Z]))
                right_foot.append(float(row[COL_RIGHT_FOOT_Z]))
            except ValueError as exc:
                raise ValueError(
                    f"Non-numeric Pelvis/Foot Z value at MEVA CSV row "
                    f"{row_number}."
                ) from exc

    if not pelvis:
        raise ValueError(f"No MEVA motion rows found in: {path}")

    return {
        "pelvis_z": np.asarray(pelvis, dtype=float),
        "left_foot_z": np.asarray(left_foot, dtype=float),
        "right_foot_z": np.asarray(right_foot, dtype=float),
    }


def align_meva_to_primary(
    meva: Dict[str, np.ndarray],
    motion: Dict,
    n_frames: int,
) -> Dict[str, np.ndarray]:
    n_meva = len(meva["pelvis_z"])

    if n_meva == n_frames:
        return {k: v.copy() for k, v in meva.items()}

    src = motion.get("source_frame_indices")
    if src is None:
        raise ValueError(
            f"MEVA has {n_meva} frames but primary has {n_frames}, "
            "and primary.pkl has no source_frame_indices."
        )

    src = np.asarray(src, dtype=int)

    if len(src) != n_frames:
        raise ValueError(
            "source_frame_indices length does not match primary frame count."
        )

    if src.min() < 0 or src.max() >= n_meva:
        raise IndexError(
            f"source_frame_indices [{src.min()}, {src.max()}] outside "
            f"MEVA range [0, {n_meva - 1}]."
        )

    return {k: v[src] for k, v in meva.items()}


# ============================================================================
# G1 kinematics / contact geometry
# ============================================================================

def body_id(model: mujoco.MjModel, name: str) -> int:
    bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, name)
    if bid < 0:
        raise KeyError(f"Body not found in MJCF: {name}")
    return int(bid)


def find_foot_contact_spheres(
    model: mujoco.MjModel,
    foot_body_name: str,
) -> List[int]:
    bid = body_id(model, foot_body_name)

    geom_ids = np.where(
        (model.geom_bodyid == bid)
        & (model.geom_type == mujoco.mjtGeom.mjGEOM_SPHERE)
    )[0].astype(int).tolist()

    if len(geom_ids) != 4:
        raise ValueError(
            f"{foot_body_name}: expected exactly 4 contact sphere geoms, "
            f"found {len(geom_ids)}."
        )

    return geom_ids


def lowest_contact_surface_z(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    contact_geom_ids: List[int],
) -> Tuple[float, int]:
    """
    Lowest WORLD-Z surface point among spherical contact geoms.

    For a sphere:
        surface_min_z = geom_center_world_z - radius
    """
    z_values = []

    for gid in contact_geom_ids:
        center_z = float(data.geom_xpos[gid, 2])
        radius = float(model.geom_size[gid, 0])
        z_values.append(center_z - radius)

    local_i = int(np.argmin(z_values))
    return float(z_values[local_i]), int(contact_geom_ids[local_i])


def get_world_body_z(data: mujoco.MjData, bid: int) -> float:
    return float(data.xpos[bid, 2])


def primary_world_z_arrays(
    model: mujoco.MjModel,
    motion: Dict,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    root_pos = np.asarray(motion["root_pos"], dtype=float)
    root_rot = np.asarray(motion["root_rot"], dtype=float)
    dof_pos = np.asarray(motion["dof_pos"], dtype=float)

    n_frames = len(root_pos)
    order = motion.get("metadata", {}).get("root_rot_order", "xyzw")
    joint_ids = actuator_joint_ids(model)

    pelvis_bid = body_id(model, PELVIS_BODY)
    left_bid = body_id(model, LEFT_FOOT_BODY)
    right_bid = body_id(model, RIGHT_FOOT_BODY)

    data = mujoco.MjData(model)

    pelvis_z = np.empty(n_frames)
    left_z = np.empty(n_frames)
    right_z = np.empty(n_frames)

    for i in range(n_frames):
        q = motion_frame_to_qpos(
            model,
            root_pos[i],
            root_rot[i],
            dof_pos[i],
            order,
            joint_ids,
        )
        data.qpos[:] = q
        mujoco.mj_forward(model, data)

        pelvis_z[i] = get_world_body_z(data, pelvis_bid)
        left_z[i] = get_world_body_z(data, left_bid)
        right_z[i] = get_world_body_z(data, right_bid)

    return pelvis_z, left_z, right_z


# ============================================================================
# Scale fitting
# ============================================================================

def fit_scale_through_origin(
    meva_pelvis_z: np.ndarray,
    meva_left_z: np.ndarray,
    meva_right_z: np.ndarray,
    g1_pelvis_z: np.ndarray,
    g1_left_z: np.ndarray,
    g1_right_z: np.ndarray,
) -> Tuple[float, float, float]:
    """
    Fit one common scale:
        g1_rel = s * meva_rel

    where rel = Foot_z - Pelvis_z.

    Left and right samples are concatenated for the common coefficient.
    Separate left/right coefficients are also returned for diagnostics.
    """
    meva_l = meva_left_z - meva_pelvis_z
    meva_r = meva_right_z - meva_pelvis_z
    g1_l = g1_left_z - g1_pelvis_z
    g1_r = g1_right_z - g1_pelvis_z

    def fit(x: np.ndarray, y: np.ndarray) -> float:
        mask = np.isfinite(x) & np.isfinite(y)
        x = x[mask]
        y = y[mask]

        denom = float(x @ x)
        if denom <= 1e-12:
            raise ValueError("Cannot fit scale: MEVA relative-Z variance is zero.")

        return float((x @ y) / denom)

    s_left = fit(meva_l, g1_l)
    s_right = fit(meva_r, g1_r)
    s_common = fit(
        np.concatenate([meva_l, meva_r]),
        np.concatenate([g1_l, g1_r]),
    )

    return s_common, s_left, s_right


# ============================================================================
# Custom Mink task: WORLD-Z difference only
# ============================================================================

class WorldZDifferenceTask(Task):
    """
    Regulate:
        (frame_world_z - root_world_z) - target_delta_z = 0

    This is deliberately WORLD-Z, not root-frame local Z.
    """

    def __init__(
        self,
        model: mujoco.MjModel,
        frame_name: str,
        root_name: str,
        cost: float,
        gain: float = 1.0,
        lm_damping: float = 1e-6,
    ):
        super().__init__(
            cost=np.asarray([float(cost)], dtype=float),
            gain=float(gain),
            lm_damping=float(lm_damping),
        )

        self.model = model
        self.frame_name = frame_name
        self.root_name = root_name
        self.frame_id = body_id(model, frame_name)
        self.root_id = body_id(model, root_name)
        self.target_delta_z = 0.0

    def set_target_delta_z(self, value: float) -> None:
        self.target_delta_z = float(value)

    def compute_error(self, configuration: mink.Configuration) -> np.ndarray:
        data = configuration.data
        current = (
            float(data.xpos[self.frame_id, 2])
            - float(data.xpos[self.root_id, 2])
        )
        return np.asarray(
            [current - self.target_delta_z],
            dtype=float,
        )

    def compute_jacobian(
        self,
        configuration: mink.Configuration,
    ) -> np.ndarray:
        """
        MuJoCo mj_jacBody returns position Jacobians aligned with WORLD axes,
        so subtracting their Z rows directly gives the desired WORLD-Z
        difference Jacobian.
        """
        data = configuration.data
        nv = self.model.nv

        jac_frame_pos = np.zeros((3, nv))
        jac_frame_rot = np.zeros((3, nv))
        jac_root_pos = np.zeros((3, nv))
        jac_root_rot = np.zeros((3, nv))

        mujoco.mj_jacBody(
            self.model,
            data,
            jac_frame_pos,
            jac_frame_rot,
            self.frame_id,
        )
        mujoco.mj_jacBody(
            self.model,
            data,
            jac_root_pos,
            jac_root_rot,
            self.root_id,
        )

        jac = jac_frame_pos[2] - jac_root_pos[2]
        return jac.reshape(1, -1)


# ============================================================================
# Main processing
# ============================================================================

def process(args: argparse.Namespace) -> None:
    motion = load_pickle(args.input_pkl)

    root_pos = np.asarray(motion["root_pos"], dtype=float)
    root_rot = np.asarray(motion["root_rot"], dtype=float)
    dof_pos = np.asarray(motion["dof_pos"], dtype=float)

    if root_pos.ndim != 2 or root_pos.shape[1] != 3:
        raise ValueError("root_pos must have shape (N, 3).")
    if root_rot.ndim != 2 or root_rot.shape[1] != 4:
        raise ValueError("root_rot must have shape (N, 4).")
    if dof_pos.ndim != 2:
        raise ValueError("dof_pos must have shape (N, ndof).")

    n_frames = len(root_pos)
    fps = float(motion.get("fps", 100.0))
    root_rot_order = motion.get("metadata", {}).get(
        "root_rot_order",
        "xyzw",
    )

    model = mujoco.MjModel.from_xml_path(str(args.robot_xml))
    joint_ids = actuator_joint_ids(model)

    # ------------------------------------------------------------------
    # MEVA
    # ------------------------------------------------------------------
    meva_all = read_meva_z_fixed(args.meva_csv)
    meva = align_meva_to_primary(meva_all, motion, n_frames)

    # ------------------------------------------------------------------
    # Primary G1 Pelvis / Foot Z and scale fit
    # ------------------------------------------------------------------
    g1_pelvis_primary, g1_left_primary, g1_right_primary = (
        primary_world_z_arrays(model, motion)
    )

    scale, scale_left, scale_right = fit_scale_through_origin(
        meva["pelvis_z"],
        meva["left_foot_z"],
        meva["right_foot_z"],
        g1_pelvis_primary,
        g1_left_primary,
        g1_right_primary,
    )

    print(f"Scale common : {scale:.8f}")
    print(f"Scale left   : {scale_left:.8f}")
    print(f"Scale right  : {scale_right:.8f}")

    # ------------------------------------------------------------------
    # Contact geoms
    # ------------------------------------------------------------------
    left_contact_ids = find_foot_contact_spheres(
        model,
        LEFT_FOOT_BODY,
    )
    right_contact_ids = find_foot_contact_spheres(
        model,
        RIGHT_FOOT_BODY,
    )
    contact_ids = left_contact_ids + right_contact_ids

    # ------------------------------------------------------------------
    # Mink setup
    # ------------------------------------------------------------------
    configuration = mink.Configuration(model)

    left_task = WorldZDifferenceTask(
        model=model,
        frame_name=LEFT_FOOT_BODY,
        root_name=PELVIS_BODY,
        cost=args.relative_z_cost,
        gain=args.task_gain,
        lm_damping=args.task_lm_damping,
    )
    right_task = WorldZDifferenceTask(
        model=model,
        frame_name=RIGHT_FOOT_BODY,
        root_name=PELVIS_BODY,
        cost=args.relative_z_cost,
        gain=args.task_gain,
        lm_damping=args.task_lm_damping,
    )

    tasks = [left_task, right_task]

    posture_task = None
    if args.posture_cost > 0.0:
        posture_task = mink.PostureTask(
            model,
            cost=float(args.posture_cost),
        )
        tasks.append(posture_task)

    # IDs for diagnostics.
    pelvis_bid = body_id(model, PELVIS_BODY)
    left_bid = body_id(model, LEFT_FOOT_BODY)
    right_bid = body_id(model, RIGHT_FOOT_BODY)

    # Output arrays.
    out_root_pos = root_pos.copy()
    out_root_rot = root_rot.copy()
    out_dof_pos = dof_pos.copy()

    source_frames = np.asarray(
        motion.get("source_frame_indices", np.arange(n_frames)),
        dtype=int,
    )

    diagnostic_rows = []

    for i in range(n_frames):
        # ==============================================================
        # A) Primary q
        # ==============================================================
        q_primary = motion_frame_to_qpos(
            model,
            root_pos[i],
            root_rot[i],
            dof_pos[i],
            root_rot_order,
            joint_ids,
        )

        configuration.update(q_primary)

        # ==============================================================
        # B) Pure global Z shift:
        #    lowest of 8 contact sphere surfaces -> z = 0
        # ==============================================================
        min_contact_before, min_gid_before = lowest_contact_surface_z(
            model,
            configuration.data,
            contact_ids,
        )

        delta_z_ground = -min_contact_before

        q_shifted = configuration.q
        free_qadr = get_free_joint_qpos_address(model)
        q_shifted[free_qadr + 2] += delta_z_ground
        configuration.update(q_shifted)

        min_contact_shifted, _ = lowest_contact_surface_z(
            model,
            configuration.data,
            contact_ids,
        )

        pelvis_z_shifted = get_world_body_z(
            configuration.data,
            pelvis_bid,
        )

        # ==============================================================
        # C) World-Z Pelvis-Foot targets from MEVA * fitted scale
        # ==============================================================
        meva_left_rel = (
            meva["left_foot_z"][i]
            - meva["pelvis_z"][i]
        )
        meva_right_rel = (
            meva["right_foot_z"][i]
            - meva["pelvis_z"][i]
        )

        target_left_rel = scale * meva_left_rel
        target_right_rel = scale * meva_right_rel

        left_task.set_target_delta_z(target_left_rel)
        right_task.set_target_delta_z(target_right_rel)

        if posture_task is not None:
            # Keep actuated joints close to the shifted primary pose.
            # PostureTask ignores the floating base.
            posture_task.set_target(configuration.q)

        # ==============================================================
        # D) Mink IK
        # ==============================================================
        iterations = 0

        for iteration in range(args.max_iterations):
            current_left_rel = (
                get_world_body_z(configuration.data, left_bid)
                - get_world_body_z(configuration.data, pelvis_bid)
            )
            current_right_rel = (
                get_world_body_z(configuration.data, right_bid)
                - get_world_body_z(configuration.data, pelvis_bid)
            )

            max_error = max(
                abs(current_left_rel - target_left_rel),
                abs(current_right_rel - target_right_rel),
            )

            if max_error <= args.tolerance_m:
                break

            velocity = mink.solve_ik(
                configuration=configuration,
                tasks=tasks,
                dt=args.dt,
                solver=args.solver,
                damping=args.solver_damping,
                safety_break=False,
            )
            configuration.integrate_inplace(velocity, args.dt)
            iterations = iteration + 1

        # ==============================================================
        # E) Diagnostics after IK
        # ==============================================================
        pelvis_z_after = get_world_body_z(
            configuration.data,
            pelvis_bid,
        )
        left_z_after = get_world_body_z(
            configuration.data,
            left_bid,
        )
        right_z_after = get_world_body_z(
            configuration.data,
            right_bid,
        )

        left_rel_after = left_z_after - pelvis_z_after
        right_rel_after = right_z_after - pelvis_z_after

        min_contact_after_ik, min_gid_after = lowest_contact_surface_z(
            model,
            configuration.data,
            contact_ids,
        )

        # Optional final pure-Z re-grounding.
        final_reground_dz = 0.0
        if args.final_reground:
            final_reground_dz = -min_contact_after_ik
            q_final = configuration.q
            q_final[free_qadr + 2] += final_reground_dz
            configuration.update(q_final)

        min_contact_final, _ = lowest_contact_surface_z(
            model,
            configuration.data,
            contact_ids,
        )

        # Save back to PKL representation.
        root_pos_i, root_rot_i, dof_i = qpos_to_motion_frame(
            model,
            configuration.q,
            joint_ids,
            root_rot_order,
        )

        out_root_pos[i] = root_pos_i
        out_root_rot[i] = root_rot_i
        out_dof_pos[i] = dof_i

        diagnostic_rows.append({
            "frame": i,
            "source_frame": int(source_frames[i]),
            "time_s": i / fps,

            "scale_common": scale,
            "scale_left": scale_left,
            "scale_right": scale_right,

            "meva_pelvis_z_m": meva["pelvis_z"][i],
            "meva_left_foot_z_m": meva["left_foot_z"][i],
            "meva_right_foot_z_m": meva["right_foot_z"][i],
            "meva_left_rel_z_m": meva_left_rel,
            "meva_right_rel_z_m": meva_right_rel,

            "g1_primary_pelvis_z_m": g1_pelvis_primary[i],
            "g1_primary_left_foot_z_m": g1_left_primary[i],
            "g1_primary_right_foot_z_m": g1_right_primary[i],
            "g1_primary_left_rel_z_m":
                g1_left_primary[i] - g1_pelvis_primary[i],
            "g1_primary_right_rel_z_m":
                g1_right_primary[i] - g1_pelvis_primary[i],

            "contact_min_z_primary_m": min_contact_before,
            "ground_shift_delta_z_m": delta_z_ground,
            "contact_min_z_after_initial_shift_m": min_contact_shifted,
            "pelvis_z_after_initial_shift_m": pelvis_z_shifted,

            "target_left_rel_z_m": target_left_rel,
            "target_right_rel_z_m": target_right_rel,

            "left_rel_z_after_ik_m": left_rel_after,
            "right_rel_z_after_ik_m": right_rel_after,
            "left_rel_z_error_after_ik_m":
                left_rel_after - target_left_rel,
            "right_rel_z_error_after_ik_m":
                right_rel_after - target_right_rel,

            "contact_min_z_after_ik_m": min_contact_after_ik,
            "final_reground_delta_z_m": final_reground_dz,
            "contact_min_z_final_m": min_contact_final,

            "ik_iterations": iterations,
            "min_contact_geom_id_primary": min_gid_before,
            "min_contact_geom_id_after_ik": min_gid_after,
        })

        if (i + 1) % 100 == 0 or i == n_frames - 1:
            print(
                f"[{i + 1:4d}/{n_frames}] "
                f"ground_dz={delta_z_ground:+.4f} m, "
                f"Lerr={left_rel_after - target_left_rel:+.5f} m, "
                f"Rerr={right_rel_after - target_right_rel:+.5f} m, "
                f"contact_after={min_contact_after_ik:+.5f} m"
            )

    # ------------------------------------------------------------------
    # Save PKL
    # ------------------------------------------------------------------
    output = dict(motion)
    output["root_pos"] = out_root_pos
    output["root_rot"] = out_root_rot
    output["dof_pos"] = out_dof_pos

    metadata = dict(output.get("metadata", {}))
    metadata["modify_z"] = {
        "enabled": True,
        "method": "contact_ground_shift_plus_world_pelvis_foot_relative_z_ik",
        "meva_fixed_columns": {
            "pelvis_z": "LY",
            "left_foot_z": "BF",
            "right_foot_z": "NK",
            "header_row": 8,
            "data_start_row": 9,
        },
        "scale_fit": {
            "method": "least_squares_through_origin_left_right_combined",
            "common": scale,
            "left_diagnostic": scale_left,
            "right_diagnostic": scale_right,
        },
        "relative_z_cost": args.relative_z_cost,
        "posture_cost": args.posture_cost,
        "task_gain": args.task_gain,
        "task_lm_damping": args.task_lm_damping,
        "solver": args.solver,
        "solver_damping": args.solver_damping,
        "max_iterations": args.max_iterations,
        "tolerance_m": args.tolerance_m,
        "final_reground": bool(args.final_reground),
        "contact_geoms": {
            "left_ids": left_contact_ids,
            "right_ids": right_contact_ids,
            "surface_definition": "sphere_center_world_z_minus_radius",
        },
    }
    output["metadata"] = metadata

    save_pickle(args.output_pkl, output)

    # ------------------------------------------------------------------
    # Diagnostics CSV
    # ------------------------------------------------------------------
    args.diagnostics_csv.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = list(diagnostic_rows[0].keys())

    with args.diagnostics_csv.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(diagnostic_rows)

    # ------------------------------------------------------------------
    # Config JSON
    # ------------------------------------------------------------------
    config = {
        "input_pkl": str(args.input_pkl),
        "robot_xml": str(args.robot_xml),
        "meva_csv": str(args.meva_csv),
        "output_pkl": str(args.output_pkl),
        "diagnostics_csv": str(args.diagnostics_csv),

        "meva_columns": {
            "pelvis_z": "LY",
            "left_foot_z": "BF",
            "right_foot_z": "NK",
        },

        "scale_common": scale,
        "scale_left_diagnostic": scale_left,
        "scale_right_diagnostic": scale_right,

        "relative_z_cost": args.relative_z_cost,
        "posture_cost": args.posture_cost,
        "task_gain": args.task_gain,
        "task_lm_damping": args.task_lm_damping,
        "solver": args.solver,
        "solver_damping": args.solver_damping,
        "dt": args.dt,
        "max_iterations": args.max_iterations,
        "tolerance_m": args.tolerance_m,
        "final_reground": bool(args.final_reground),
    }

    args.config_out.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    args.config_out.write_text(
        json.dumps(config, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("")
    print(f"Saved PKL        : {args.output_pkl}")
    print(f"Saved diagnostics: {args.diagnostics_csv}")
    print(f"Saved config     : {args.config_out}")


# ============================================================================
# CLI
# ============================================================================

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()

    p.add_argument(
        "--input-pkl",
        type=Path,
        required=True,
    )
    p.add_argument(
        "--robot-xml",
        type=Path,
        required=True,
    )
    p.add_argument(
        "--meva-csv",
        type=Path,
        required=True,
    )
    p.add_argument(
        "--output-pkl",
        type=Path,
        required=True,
    )
    p.add_argument(
        "--diagnostics-csv",
        type=Path,
        required=True,
    )
    p.add_argument(
        "--config-out",
        type=Path,
        required=True,
    )

    p.add_argument(
        "--relative-z-cost",
        type=float,
        default=0.8,
    )
    p.add_argument(
        "--posture-cost",
        type=float,
        default=0.02,
        help=(
            "Weak joint-posture reference to primary. "
            "Set 0 to disable."
        ),
    )
    p.add_argument(
        "--task-gain",
        type=float,
        default=1.0,
    )
    p.add_argument(
        "--task-lm-damping",
        type=float,
        default=1e-6,
    )
    p.add_argument(
        "--solver",
        type=str,
        default="daqp",
    )
    p.add_argument(
        "--solver-damping",
        type=float,
        default=1e-6,
    )
    p.add_argument(
        "--dt",
        type=float,
        default=0.01,
    )
    p.add_argument(
        "--max-iterations",
        type=int,
        default=20,
    )
    p.add_argument(
        "--tolerance-m",
        type=float,
        default=1e-4,
    )
    p.add_argument(
        "--final-reground",
        action="store_true",
        help=(
            "After IK, apply one more pure global-Z shift so the final "
            "lowest contact sphere surface is exactly z=0."
        ),
    )

    return p


def main() -> None:
    args = build_parser().parse_args()
    process(args)


if __name__ == "__main__":
    main()
