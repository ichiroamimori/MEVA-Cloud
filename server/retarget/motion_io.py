"""Canonical MEVA Cloud motion NPZ I/O and GMR export helpers."""
from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any

import numpy as np


MOTION_SCHEMA_VERSION = "1.0"


def trajectory_derivatives(values: np.ndarray, fps: float) -> tuple[np.ndarray, np.ndarray]:
    """Offline first/second derivatives with explicit finite endpoints."""
    values = np.asarray(values, dtype=np.float64)
    if values.ndim < 1:
        raise ValueError("Trajectory must have a frame axis")
    if not np.isfinite(fps) or fps <= 0.0:
        raise ValueError("fps must be positive")
    n = len(values)
    velocity = np.zeros_like(values)
    acceleration = np.zeros_like(values)
    if n == 0:
        return velocity, acceleration
    dt = 1.0 / float(fps)
    if n == 2:
        velocity[:] = (values[1] - values[0]) / dt
        return velocity, acceleration
    if n >= 3:
        velocity[1:-1] = (values[2:] - values[:-2]) / (2.0 * dt)
        velocity[0] = (-3.0 * values[0] + 4.0 * values[1] - values[2]) / (2.0 * dt)
        velocity[-1] = (3.0 * values[-1] - 4.0 * values[-2] + values[-3]) / (2.0 * dt)
        acceleration[1:-1] = (
            values[2:] - 2.0 * values[1:-1] + values[:-2]
        ) / (dt * dt)
        if n == 3:
            acceleration[0] = acceleration[1]
            acceleration[-1] = acceleration[1]
        else:
            acceleration[0] = (
                2.0 * values[0] - 5.0 * values[1]
                + 4.0 * values[2] - values[3]
            ) / (dt * dt)
            acceleration[-1] = (
                2.0 * values[-1] - 5.0 * values[-2]
                + 4.0 * values[-3] - values[-4]
            ) / (dt * dt)
    return velocity, acceleration


def _wxyz(quaternions: np.ndarray, order: str) -> np.ndarray:
    q = np.asarray(quaternions, dtype=np.float64)
    if q.ndim != 2 or q.shape[1] != 4:
        raise ValueError("root_rot must have shape (N,4)")
    if order == "xyzw":
        q = q[:, [3, 0, 1, 2]]
    elif order != "wxyz":
        raise ValueError(f"Unsupported quaternion order: {order}")
    norms = np.linalg.norm(q, axis=1, keepdims=True)
    if np.any(norms <= 1e-12):
        raise ValueError("root_rot contains a zero quaternion")
    return q / norms


def _qmul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    aw, ax, ay, az = np.moveaxis(a, -1, 0)
    bw, bx, by, bz = np.moveaxis(b, -1, 0)
    return np.stack((
        aw*bw - ax*bx - ay*by - az*bz,
        aw*bx + ax*bw + ay*bz - az*by,
        aw*by - ax*bz + ay*bw + az*bx,
        aw*bz + ax*by - ay*bx + az*bw,
    ), axis=-1)


def _relative_rotvec(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Rotation vector taking orientation a to b, for wxyz inputs."""
    inv = a.copy()
    inv[..., 1:] *= -1.0
    delta = _qmul(inv, b)
    flip = delta[..., 0] < 0.0
    delta[flip] *= -1.0
    vector = delta[..., 1:]
    norm = np.linalg.norm(vector, axis=-1)
    angle = 2.0 * np.arctan2(norm, np.clip(delta[..., 0], -1.0, 1.0))
    scale = np.divide(angle, norm, out=np.full_like(angle, 2.0), where=norm > 1e-12)
    return vector * scale[..., None]


def quaternion_error_rotvec(result_wxyz: np.ndarray, target_wxyz: np.ndarray) -> np.ndarray:
    """Rotation vector that takes result orientation to target orientation."""
    return _relative_rotvec(
        np.asarray(result_wxyz, dtype=np.float64),
        np.asarray(target_wxyz, dtype=np.float64),
    )


def angular_velocity(root_rot: np.ndarray, fps: float, order: str) -> np.ndarray:
    q = _wxyz(root_rot, order)
    n = len(q)
    result = np.zeros((n, 3), dtype=np.float64)
    if n == 1:
        return result
    dt = 1.0 / float(fps)
    result[0] = _relative_rotvec(q[0:1], q[1:2])[0] / dt
    result[-1] = _relative_rotvec(q[-2:-1], q[-1:])[0] / dt
    if n > 2:
        result[1:-1] = _relative_rotvec(q[:-2], q[2:]) / (2.0 * dt)
    return result


def canonical_motion(
    motion: dict[str, Any], *, joint_names: list[str], root_rot_order: str
) -> dict[str, np.ndarray]:
    root_pos = np.asarray(motion["root_pos"], dtype=np.float64)
    root_rot = np.asarray(motion["root_rot"], dtype=np.float64)
    dof_pos = np.asarray(motion["dof_pos"], dtype=np.float64)
    fps = float(motion["fps"])
    n = len(root_pos)
    if root_pos.shape != (n, 3) or root_rot.shape != (n, 4):
        raise ValueError("Invalid root motion shape")
    if dof_pos.shape != (n, len(joint_names)):
        raise ValueError("dof_pos shape does not match joint_names")
    dof_vel, dof_acc = trajectory_derivatives(dof_pos, fps)
    root_lin_vel, _ = trajectory_derivatives(root_pos, fps)
    source_float = np.asarray(
        motion.get("source_frame_float", motion.get("source_frame_indices", np.arange(n))),
        dtype=np.float64,
    )
    source_nearest = np.asarray(
        motion.get("source_frame_nearest", motion.get("source_frame_indices", np.rint(source_float))),
        dtype=np.int32,
    )
    time_s = np.asarray(motion.get("time_s", np.arange(n) / fps), dtype=np.float64)
    return {
        "schema_version": np.asarray(MOTION_SCHEMA_VERSION),
        "fps": np.asarray(fps, dtype=np.float64),
        "frame": np.arange(n, dtype=np.int32),
        "time_s": time_s,
        "source_frame_float": source_float,
        "source_frame_nearest": source_nearest,
        "root_pos": root_pos,
        "root_rot": root_rot,
        "root_rot_order": np.asarray(root_rot_order),
        "joint_names": np.asarray(joint_names, dtype=np.str_),
        "dof_pos": dof_pos,
        "dof_vel": dof_vel,
        "dof_acc": dof_acc,
        "root_lin_vel": root_lin_vel,
        "root_ang_vel": angular_velocity(root_rot, fps, root_rot_order),
    }


def save_motion_npz(
    path: Path, motion: dict[str, Any], *, joint_names: list[str], root_rot_order: str
) -> dict[str, np.ndarray]:
    arrays = canonical_motion(
        motion, joint_names=joint_names, root_rot_order=root_rot_order
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, **arrays)
    return arrays


def load_motion(path: Path) -> dict[str, Any]:
    """Load canonical NPZ, with read-only PKL support for legacy Runs."""
    if path.suffix.lower() == ".pkl":
        with path.open("rb") as stream:
            value = pickle.load(stream)
        if not isinstance(value, dict):
            raise TypeError(f"Legacy motion must be a dict: {path}")
        return value
    with np.load(path, allow_pickle=False) as archive:
        data = {key: archive[key].copy() for key in archive.files}
    for key in ("fps", "root_rot_order", "schema_version"):
        if key in data and np.asarray(data[key]).shape == ():
            data[key] = np.asarray(data[key]).item()
    data["fps"] = float(data["fps"])
    frame_count = int(np.asarray(data.get("root_pos", [])).shape[0])
    source_nearest = data.get("source_frame_nearest")
    data["source_frame_indices"] = np.asarray(
        source_nearest if source_nearest is not None else np.arange(frame_count),
        dtype=np.int32,
    )
    root_rot_order = str(data.get("root_rot_order") or "xyzw")
    data["root_rot_order"] = root_rot_order
    data["metadata"] = {
        "root_rot_order": root_rot_order,
        "canonical_motion_npz": "schema_version" in data,
        "primary_postprocess": {
            "completed": True,
            "root_pos_shift_applied": True,
        },
    }
    return data


def save_gmr_pickle(path: Path, motion: dict[str, Any]) -> dict[str, Any]:
    """Write the exact key contract consumed by GMR data_loader.py.

    GMR persists root_rot as xyzw and converts it to wxyz while loading.
    """
    order = str(motion.get("metadata", {}).get(
        "root_rot_order", motion.get("root_rot_order", "xyzw")
    ))
    root_rot = np.asarray(motion["root_rot"], dtype=np.float64)
    if order == "wxyz":
        root_rot = root_rot[:, [1, 2, 3, 0]]
    elif order != "xyzw":
        raise ValueError(f"Unsupported quaternion order: {order}")
    value = {
        "fps": float(motion["fps"]),
        "root_pos": np.asarray(motion["root_pos"], dtype=np.float64),
        "root_rot": root_rot,
        "dof_pos": np.asarray(motion["dof_pos"], dtype=np.float64),
        "local_body_pos": None,
        "link_body_list": None,
    }
    with path.open("wb") as stream:
        pickle.dump(value, stream)
    return value
