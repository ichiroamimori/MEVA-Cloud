# -*- coding: utf-8 -*-
"""Common MEVA-to-robot orientation Mapping tasks for every IK stage."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import mujoco
import mink
import numpy as np

try:
    from .ik_solver import IKDiagnosticTarget
except ImportError:
    from ik_solver import IKDiagnosticTarget


VIRTUAL_SOURCE_SEGMENTS = {
    "Thoracic2+LumberSpine": ("Thoracic2", "LumbarSpine", 0.5),
}


def normq(q):
    q = np.asarray(q, dtype=float).reshape(4)
    n = np.linalg.norm(q)
    if not np.isfinite(n) or n < 1e-12:
        raise ValueError(f"bad quaternion {q}")
    return q / n


def qmul(a, b):
    out = np.empty(4, dtype=float)
    mujoco.mju_mulQuat(out, normq(a), normq(b))
    return normq(out)


def qinv(q):
    q = normq(q)
    return np.array([q[0], -q[1], -q[2], -q[3]], dtype=float)


def quat_angle_deg(a, b):
    dq = qmul(qinv(a), b)
    w = float(np.clip(abs(dq[0]), -1.0, 1.0))
    return float(np.degrees(2.0 * np.arccos(w)))


def normalize_vec(v):
    v = np.asarray(v, dtype=float)
    n = float(np.linalg.norm(v))
    if n < 1e-12:
        raise ValueError("zero-length direction vector")
    return v / n


def _skew(v):
    x, y, z = np.asarray(v, dtype=float).reshape(3)
    return np.asarray([
        [0.0, -z, y],
        [z, 0.0, -x],
        [-y, x, 0.0],
    ])


def quat_rotate_vec(q, v):
    q = normq(q)
    v = np.asarray(v, dtype=float)
    qv = q[1:4]
    t = 2.0 * np.cross(qv, v)
    return v + q[0] * t + np.cross(qv, t)


def axis_angle_rad(a, b):
    a = normalize_vec(a)
    b = normalize_vec(b)
    dot = float(np.clip(np.dot(a, b), -1.0, 1.0))
    return float(np.arccos(dot))


def axis_angle_deg(a, b):
    return float(np.degrees(axis_angle_rad(a, b)))


def quat_slerp(a, b, t: float):
    a = normq(a)
    b = normq(b)
    t = float(t)
    dot = float(np.dot(a, b))
    if dot < 0.0:
        b = -b
        dot = -dot
    dot = float(np.clip(dot, -1.0, 1.0))
    if dot > 0.9995:
        return normq((1.0 - t) * a + t * b)
    theta = float(np.arccos(dot))
    sin_theta = float(np.sin(theta))
    wa = float(np.sin((1.0 - t) * theta) / sin_theta)
    wb = float(np.sin(t * theta) / sin_theta)
    return normq(wa * a + wb * b)


def source_segments_for_columns(segment: str):
    virtual = VIRTUAL_SOURCE_SEGMENTS.get(segment)
    return (segment,) if virtual is None else (virtual[0], virtual[1])


def read_meva(path: Path, header_row: int):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        for _ in range(header_row - 1):
            next(f, None)
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def _segq_physical(row, pattern: str, segment: str):
    keys = [pattern.format(segment=segment, component=c) for c in "wxyz"]
    return normq([float(row[k]) for k in keys])


def segq(row, pattern: str, segment: str):
    virtual = VIRTUAL_SOURCE_SEGMENTS.get(segment)
    if virtual is None:
        return _segq_physical(row, pattern, segment)
    segment_a, segment_b, weight_b = virtual
    return quat_slerp(
        _segq_physical(row, pattern, segment_a),
        _segq_physical(row, pattern, segment_b),
        weight_b,
    )


def required_quaternion_columns(cfg: dict) -> set[str]:
    pattern = cfg["source"]["quaternion_columns"]
    return {
        pattern.format(segment=physical_segment, component=component)
        for mapping in cfg.get("mappings", [])
        for physical_segment in source_segments_for_columns(mapping["source_segment"])
        for component in "wxyz"
    }


@dataclass
class PreparedMappingTasks:
    tasks: list[Any]
    diagnostics: list[IKDiagnosticTarget]


class RelativeDirectionTask(mink.Task):
    """Keep the world direction between two Body-fixed Robot points."""

    k = 3

    def __init__(
        self,
        from_frame,
        to_frame,
        cost,
        gain=1.0,
        lm_damping=0.0,
        from_local_position=None,
        to_local_position=None,
    ):
        cost = float(cost)
        if not np.isfinite(cost) or cost < 0.0:
            raise ValueError("RelativeDirectionTask cost must be non-negative")
        super().__init__(
            cost=np.full(self.k, cost, dtype=float),
            gain=gain,
            lm_damping=lm_damping,
        )
        self.from_frame = from_frame
        self.to_frame = to_frame
        self.from_local_position = np.asarray(
            [0.0, 0.0, 0.0]
            if from_local_position is None else from_local_position,
            dtype=float,
        )
        self.to_local_position = np.asarray(
            [0.0, 0.0, 0.0]
            if to_local_position is None else to_local_position,
            dtype=float,
        )
        if (
            self.from_local_position.shape != (3,)
            or self.to_local_position.shape != (3,)
            or not np.all(np.isfinite(self.from_local_position))
            or not np.all(np.isfinite(self.to_local_position))
        ):
            raise ValueError("RelativeDirectionTask local positions must be finite XYZ")
        self.target_direction = None

    def set_target(self, direction_world):
        self.target_direction = normalize_vec(direction_world).copy()

    def _error_and_jacobian(self, configuration):
        if self.target_direction is None:
            raise RuntimeError("RelativeDirectionTask target is not set")
        tf_from = configuration.get_transform_frame_to_world(self.from_frame, "body")
        tf_to = configuration.get_transform_frame_to_world(self.to_frame, "body")
        rot_from = tf_from.rotation().as_matrix()
        rot_to = tf_to.rotation().as_matrix()
        offset_from_world = rot_from @ self.from_local_position
        offset_to_world = rot_to @ self.to_local_position
        point_from = tf_from.translation() + offset_from_world
        point_to = tf_to.translation() + offset_to_world
        relative = point_to - point_from
        distance = float(np.linalg.norm(relative))
        if not np.isfinite(distance) or distance < 1e-9:
            raise ValueError(
                f"RelativeDirectionTask degenerate frames: "
                f"{self.from_frame} -> {self.to_frame}"
            )
        direction = relative / distance
        jac_from_local = configuration.get_frame_jacobian(self.from_frame, "body")
        jac_to_local = configuration.get_frame_jacobian(self.to_frame, "body")
        jac_from_linear = rot_from @ jac_from_local[:3]
        jac_to_linear = rot_to @ jac_to_local[:3]
        jac_from_angular = rot_from @ jac_from_local[3:]
        jac_to_angular = rot_to @ jac_to_local[3:]
        jac_from_point = (
            jac_from_linear - _skew(offset_from_world) @ jac_from_angular
        )
        jac_to_point = (
            jac_to_linear - _skew(offset_to_world) @ jac_to_angular
        )
        jac_relative = jac_to_point - jac_from_point
        projector = np.eye(3) - np.outer(direction, direction)
        return direction - self.target_direction, (projector @ jac_relative) / distance

    def compute_error(self, configuration):
        return self._error_and_jacobian(configuration)[0]

    def compute_jacobian(self, configuration):
        return self._error_and_jacobian(configuration)[1]


class MappingTaskSet:
    """Build and update the same Mapping semantics for Primary and Main.

    A stage supplies only the position targets that exist for that stage.  All
    configured Mapping orientation targets are always generated.
    """

    def __init__(
        self,
        *,
        model,
        cfg: dict,
        mapping_offsets: dict[str, Any],
        offset_details: dict[str, Any],
        position_cost_by_link: dict[str, float] | None = None,
    ):
        self.model = model
        self.mappings = list(cfg.get("mappings", []))
        self.mapping_offsets = mapping_offsets
        self.pattern = str(cfg["source"]["quaternion_columns"])
        self.world_alignment = normq(cfg.get("world_alignment", {}).get(
            "offset_quaternion_wxyz", [1.0, 0.0, 0.0, 0.0]
        ))
        self.position_cost_by_link = dict(position_cost_by_link or {})
        lm_damping = float(cfg["solver"]["task_lm_damping"])
        self.robot_axis_by_link: dict[str, np.ndarray] = {}
        self.tasks_by_link: dict[str, list[Any]] = {}

        for mapping in self.mappings:
            link = str(mapping["target_link"])
            mode = str(mapping.get("orientation_mode", "full"))
            if mode not in {"full", "axis"}:
                raise ValueError(f"Unsupported orientation_mode={mode!r}")
            if mujoco.mj_name2id(
                model, mujoco.mjtObj.mjOBJ_BODY, link
            ) < 0:
                raise KeyError("Missing body " + link)
            if link not in mapping_offsets:
                raise KeyError(f"Missing mapping offset for {link}")

            position_cost = float(self.position_cost_by_link.get(link, 0.0))
            orientation_cost = float(mapping["orientation_weight"])
            link_tasks: list[Any] = []
            if mode == "full":
                link_tasks.append(mink.FrameTask(
                    link,
                    "body",
                    position_cost=position_cost,
                    orientation_cost=orientation_cost,
                    gain=1.0,
                    lm_damping=lm_damping,
                ))
            else:
                axis = offset_details.get(link, {}).get(
                    "robot_long_axis_link_local"
                )
                if axis is None:
                    raise KeyError(
                        "Axis mode requires robot_long_axis_link_local in the "
                        f"mapping offset asset for {link}."
                    )
                self.robot_axis_by_link[link] = normalize_vec(axis)
                link_tasks.append(mink.AxisAlignTask(
                    frame_name=link,
                    frame_type="body",
                    axis=self.robot_axis_by_link[link],
                    cost=orientation_cost,
                ))
                if position_cost > 0.0:
                    link_tasks.append(mink.FrameTask(
                        link,
                        "body",
                        position_cost=position_cost,
                        orientation_cost=0.0,
                        gain=1.0,
                        lm_damping=lm_damping,
                    ))
            self.tasks_by_link[link] = link_tasks

    def prepare(
        self,
        *,
        row: dict,
        configuration,
        source_frame: int,
        position_targets_by_link: dict[str, Any] | None = None,
    ) -> PreparedMappingTasks:
        position_targets_by_link = dict(position_targets_by_link or {})
        active: list[Any] = []
        target_quats: dict[str, np.ndarray] = {}
        target_dirs: dict[str, np.ndarray] = {}

        for mapping in self.mappings:
            link = str(mapping["target_link"])
            mode = str(mapping.get("orientation_mode", "full"))
            q_meva = segq(row, self.pattern, mapping["source_segment"])
            q_target = qmul(
                self.world_alignment,
                qmul(q_meva, self.mapping_offsets[link]),
            )
            target_quats[link] = q_target.copy()
            rotation = mink.SO3(wxyz=q_target)
            translation = position_targets_by_link.get(link)
            if translation is None:
                translation = configuration.get_transform_frame_to_world(
                    link, "body"
                ).translation()

            link_tasks = self.tasks_by_link[link]
            if mode == "full":
                link_tasks[0].set_target(
                    mink.SE3.from_rotation_and_translation(rotation, translation)
                )
            else:
                target_direction = normalize_vec(
                    quat_rotate_vec(q_target, self.robot_axis_by_link[link])
                )
                target_dirs[link] = target_direction
                link_tasks[0].set_target(target_direction)
                if len(link_tasks) > 1:
                    link_tasks[1].set_target(
                        mink.SE3.from_rotation_and_translation(rotation, translation)
                    )
            active.extend(link_tasks)

        diagnostics: list[IKDiagnosticTarget] = []
        for mapping in self.mappings:
            link = str(mapping["target_link"])
            mode = str(mapping.get("orientation_mode", "full"))

            def measure(current, link=link, mode=mode):
                actual_tf = current.get_transform_frame_to_world(link, "body")
                q_actual = normq(actual_tf.rotation().wxyz)
                if mode == "axis":
                    actual_direction = quat_rotate_vec(
                        q_actual, self.robot_axis_by_link[link]
                    )
                    return axis_angle_deg(target_dirs[link], actual_direction)
                return quat_angle_deg(target_quats[link], q_actual)

            diagnostics.append(IKDiagnosticTarget(
                key=link,
                metadata={
                    "source_frame": int(source_frame),
                    "source_segment": mapping["source_segment"],
                    "target_link": link,
                    "orientation_weight": float(mapping["orientation_weight"]),
                    "orientation_mode": mode,
                },
                measure=measure,
            ))
        return PreparedMappingTasks(tasks=active, diagnostics=diagnostics)
