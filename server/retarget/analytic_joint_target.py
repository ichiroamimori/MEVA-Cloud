"""Model-derived analytic targets for serial three-hinge orientation clusters."""
from __future__ import annotations

from dataclasses import dataclass, replace
import itertools
import math
from typing import Any

import mujoco
import numpy as np


RANK_RATIO_MIN = 0.1
AXIAL_MAX_ANGLE_DEG = 30.0
AXIAL_MAX_SENSITIVITY = 0.5
AXIAL_SENSITIVITY_MARGIN = 0.25
FK_TOLERANCE_RAD = 1e-5
POE_VALIDATION_TOLERANCE_RAD = 1e-6


def _name(model: mujoco.MjModel, kind: mujoco.mjtObj, index: int) -> str:
    return mujoco.mj_id2name(model, kind, index) or f"unnamed_{index}"


def _rotation(axis: np.ndarray, angle: float) -> np.ndarray:
    axis = np.asarray(axis, dtype=float)
    axis = axis / np.linalg.norm(axis)
    x, y, z = axis
    c, s = math.cos(angle), math.sin(angle)
    C = 1.0 - c
    return np.asarray([
        [c + x*x*C, x*y*C - z*s, x*z*C + y*s],
        [y*x*C + z*s, c + y*y*C, y*z*C - x*s],
        [z*x*C - y*s, z*y*C + x*s, c + z*z*C],
    ])


def _quat_matrix(quaternion_wxyz: np.ndarray) -> np.ndarray:
    matrix = np.empty(9, dtype=float)
    mujoco.mju_quat2Mat(matrix, np.asarray(quaternion_wxyz, dtype=float))
    return matrix.reshape(3, 3)


def _rotation_error(a: np.ndarray, b: np.ndarray) -> float:
    value = float(np.clip((np.trace(a.T @ b) - 1.0) * 0.5, -1.0, 1.0))
    return float(math.acos(value))


def _angle_about_axis(rotation: np.ndarray, axis: np.ndarray) -> float:
    skew_vector = np.asarray([
        rotation[2, 1] - rotation[1, 2],
        rotation[0, 2] - rotation[2, 0],
        rotation[1, 0] - rotation[0, 1],
    ])
    sine = 0.5 * float(np.dot(axis, skew_vector))
    cosine = 0.5 * float(np.trace(rotation) - 1.0)
    return float(math.atan2(sine, cosine))


def _axis_angle_from_vectors(axis: np.ndarray, source: np.ndarray, target: np.ndarray) -> float | None:
    source_perp = source - axis * float(np.dot(axis, source))
    target_perp = target - axis * float(np.dot(axis, target))
    source_norm = float(np.linalg.norm(source_perp))
    target_norm = float(np.linalg.norm(target_perp))
    if source_norm < 1e-10 or target_norm < 1e-10:
        return None
    source_perp /= source_norm
    target_perp /= target_norm
    return float(math.atan2(
        float(np.dot(axis, np.cross(source_perp, target_perp))),
        float(np.dot(source_perp, target_perp)),
    ))


def _lift_angle(
    angle: float, previous: float, limited: bool, joint_range: tuple[float, float]
) -> list[float]:
    two_pi = 2.0 * math.pi
    if not limited:
        return [angle + two_pi * round((previous - angle) / two_pi)]
    lower, upper = joint_range
    minimum = math.ceil((lower - angle - 1e-10) / two_pi)
    maximum = math.floor((upper - angle + 1e-10) / two_pi)
    return [angle + two_pi * k for k in range(minimum, maximum + 1)]


@dataclass(frozen=True)
class AnalyticJointCluster:
    cluster_id: str
    proximal_link: str
    distal_link: str
    proximal_segment: str
    distal_segment: str
    mapping_mode: str
    body_ids: tuple[int, ...]
    joint_ids: tuple[int, int, int]
    joint_names: tuple[str, str, str]
    qpos_addresses: tuple[int, int, int]
    dof_addresses: tuple[int, int, int]
    joint_limited: tuple[bool, bool, bool]
    joint_ranges: tuple[tuple[float, float], tuple[float, float], tuple[float, float]]
    axes_proximal_zero: np.ndarray
    home_rotation: np.ndarray
    fixed_body_positions: tuple[tuple[float, float, float], ...]
    fixed_body_quaternions: tuple[tuple[float, float, float, float], ...]
    rank_ratio_max: float
    fk_reconstruction_error_rad: float
    supported: bool
    detection_reason: str
    primary_axis_local: np.ndarray | None = None
    axial_joint_index: int | None = None
    axial_alignment_deg: float | None = None
    axial_sensitivity: float | None = None
    axial_runner_up_sensitivity: float | None = None
    low_confidence: bool = False

    def metadata(self) -> dict[str, Any]:
        return {
            "cluster_id": self.cluster_id,
            "proximal_link": self.proximal_link,
            "distal_link": self.distal_link,
            "proximal_segment": self.proximal_segment,
            "distal_segment": self.distal_segment,
            "mapping_mode": self.mapping_mode,
            "joint_names": list(self.joint_names),
            "joint_ids": list(self.joint_ids),
            "axes_proximal_zero": self.axes_proximal_zero.tolist(),
            "home_rotation": self.home_rotation.tolist(),
            "fixed_body_positions": [list(value) for value in self.fixed_body_positions],
            "fixed_body_quaternions": [list(value) for value in self.fixed_body_quaternions],
            "rank_ratio_max": float(self.rank_ratio_max),
            "fk_reconstruction_error_rad": float(self.fk_reconstruction_error_rad),
            "supported": bool(self.supported),
            "detection_reason": self.detection_reason,
            "primary_axis_local": (
                None if self.primary_axis_local is None else self.primary_axis_local.tolist()
            ),
            "axial_joint_index": self.axial_joint_index,
            "axial_joint_name": (
                None if self.axial_joint_index is None
                else self.joint_names[self.axial_joint_index]
            ),
            "axial_alignment_deg": self.axial_alignment_deg,
            "axial_sensitivity": self.axial_sensitivity,
            "axial_runner_up_sensitivity": self.axial_runner_up_sensitivity,
            "low_confidence": bool(self.low_confidence),
        }


@dataclass(frozen=True)
class AnalyticJointTargetProfile:
    joint_names: tuple[str, ...]
    target_rad: np.ndarray
    target_enabled: np.ndarray
    cluster_ids: tuple[str, ...]
    selected_branch: np.ndarray
    singularity_flag: np.ndarray
    clusters: tuple[AnalyticJointCluster, ...]


def _path_bodies(model: mujoco.MjModel, ancestor: int, distal: int) -> list[int]:
    path: list[int] = []
    current = distal
    while current != ancestor and current > 0:
        path.append(current)
        current = int(model.body_parentid[current])
    return list(reversed(path)) if current == ancestor else []


def _sample_values(model: mujoco.MjModel, initial_q: np.ndarray, joints: list[int]) -> list[list[float]]:
    values: list[list[float]] = []
    for joint_id in joints:
        q0 = float(initial_q[int(model.jnt_qposadr[joint_id])])
        raw = [q0 - 0.6, q0, q0 + 0.6]
        if bool(model.jnt_limited[joint_id]):
            lower, upper = (float(x) for x in model.jnt_range[joint_id])
            margin = 0.05 * (upper - lower)
            raw = [min(upper - margin, max(lower + margin, value)) for value in raw]
        values.append(list(dict.fromkeys(round(value, 12) for value in raw)))
    return values


def _angular_axes_proximal(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    proximal_id: int,
    distal_id: int,
    joints: list[int],
) -> list[np.ndarray]:
    """Read actual instantaneous hinge axes from the distal Body Jacobian."""
    jacobian_position = np.zeros((3, model.nv), dtype=float)
    jacobian_rotation = np.zeros((3, model.nv), dtype=float)
    mujoco.mj_jacBody(
        model, data, jacobian_position, jacobian_rotation, distal_id
    )
    proximal_rotation = np.asarray(data.xmat[proximal_id]).reshape(3, 3)
    return [
        proximal_rotation.T @ jacobian_rotation[:, int(model.jnt_dofadr[joint_id])]
        for joint_id in joints
    ]


def _sample_metrics(
    runtime: Any, proximal_id: int, distal_id: int, joints: list[int], primary: np.ndarray | None
) -> tuple[float, list[float], list[float]]:
    model = runtime.model
    ratios: list[float] = []
    sensitivities: list[list[float]] = [[], [], []]
    angles: list[list[float]] = [[], [], []]
    for values in itertools.product(*_sample_values(model, runtime.initial_qpos, joints)):
        data = mujoco.MjData(model)
        data.qpos[:] = runtime.initial_qpos
        for joint_id, value in zip(joints, values):
            data.qpos[int(model.jnt_qposadr[joint_id])] = value
        mujoco.mj_forward(model, data)
        proximal_rotation = np.asarray(data.xmat[proximal_id]).reshape(3, 3)
        axes = _angular_axes_proximal(
            model, data, proximal_id, distal_id, joints
        )
        singular_values = np.linalg.svd(np.column_stack(axes), compute_uv=False)
        ratios.append(float(singular_values[-1] / singular_values[0]))
        if primary is not None:
            direction_world = (
                np.asarray(data.xmat[distal_id]).reshape(3, 3) @ primary
            )
            for index, axis in enumerate(axes):
                alignment = abs(float(np.dot(axis, proximal_rotation.T @ direction_world)))
                alignment = float(np.clip(alignment, -1.0, 1.0))
                angles[index].append(math.degrees(math.acos(alignment)))
                sensitivities[index].append(math.sqrt(max(0.0, 1.0 - alignment * alignment)))
    return (
        max(ratios, default=0.0),
        [float(np.median(value)) for value in angles] if primary is not None else [],
        [float(np.median(value)) for value in sensitivities] if primary is not None else [],
    )


def _poe_reconstruction_error(
    runtime: Any,
    proximal_id: int,
    distal_id: int,
    joints: list[int],
    axes: np.ndarray,
    home_rotation: np.ndarray,
) -> float:
    """Validate that detected axes and fixed transforms reproduce MuJoCo FK."""
    errors: list[float] = []
    for values in itertools.product(*_sample_values(
        runtime.model, runtime.initial_qpos, joints
    )):
        data = mujoco.MjData(runtime.model)
        data.qpos[:] = runtime.initial_qpos
        for joint_id, value in zip(joints, values):
            data.qpos[int(runtime.model.jnt_qposadr[joint_id])] = value
        mujoco.mj_forward(runtime.model, data)
        proximal_rotation = np.asarray(data.xmat[proximal_id]).reshape(3, 3)
        distal_rotation = np.asarray(data.xmat[distal_id]).reshape(3, 3)
        expected = proximal_rotation.T @ distal_rotation
        reconstructed = home_rotation.copy()
        for axis, value in reversed(list(zip(axes, values))):
            reconstructed = _rotation(axis, value) @ reconstructed
        errors.append(_rotation_error(reconstructed, expected))
    return max(errors, default=math.inf)


def detect_analytic_joint_clusters(runtime: Any, config: dict[str, Any]) -> list[AnalyticJointCluster]:
    """Detect nearest-mapped-link three-hinge clusters without Robot/name rules."""
    model = runtime.model
    mappings = {
        str(item.get("target_link")): item
        for item in config.get("mappings", []) if isinstance(item, dict)
    }
    body_ids = {
        _name(model, mujoco.mjtObj.mjOBJ_BODY, body_id): body_id
        for body_id in range(1, model.nbody)
    }
    candidates: list[AnalyticJointCluster] = []
    for distal_link, distal_mapping in mappings.items():
        distal_id = body_ids.get(distal_link)
        if distal_id is None:
            continue
        current = int(model.body_parentid[distal_id])
        proximal_link = None
        proximal_id = -1
        while current > 0:
            current_name = _name(model, mujoco.mjtObj.mjOBJ_BODY, current)
            if current_name in mappings:
                proximal_link, proximal_id = current_name, current
                break
            current = int(model.body_parentid[current])
        if proximal_link is None:
            continue
        bodies = _path_bodies(model, proximal_id, distal_id)
        joints: list[int] = []
        for body_id in bodies:
            address = int(model.body_jntadr[body_id])
            joints.extend(range(address, address + int(model.body_jntnum[body_id])))
        if len(joints) != 3 or any(
            int(model.jnt_type[joint_id]) != int(mujoco.mjtJoint.mjJNT_HINGE)
            for joint_id in joints
        ):
            continue

        zero_data = mujoco.MjData(model)
        zero_data.qpos[:] = runtime.initial_qpos
        for joint_id in joints:
            zero_data.qpos[int(model.jnt_qposadr[joint_id])] = 0.0
        mujoco.mj_forward(model, zero_data)
        proximal_rotation = np.asarray(zero_data.xmat[proximal_id]).reshape(3, 3)
        distal_rotation = np.asarray(zero_data.xmat[distal_id]).reshape(3, 3)
        axes = _angular_axes_proximal(
            model, zero_data, proximal_id, distal_id, joints
        )
        axes_array = np.asarray(axes)
        home_rotation = proximal_rotation.T @ distal_rotation
        reconstruction_error = _poe_reconstruction_error(
            runtime, proximal_id, distal_id, joints, axes_array, home_rotation
        )
        primary_definition = runtime.orientation(distal_link).primary_axis
        primary = (
            None if primary_definition is None
            else np.asarray(primary_definition, dtype=float)
        )
        rank_ratio, alignment_angles, sensitivities = _sample_metrics(
            runtime, proximal_id, distal_id, joints, primary
        )
        mode = str(distal_mapping.get("orientation_mode") or "full")
        proximal_mode = str(mappings[proximal_link].get("orientation_mode") or "full")
        supported = rank_ratio >= RANK_RATIO_MIN
        reason = "supported" if supported else "orientation_rank_below_threshold"
        if supported and reconstruction_error > POE_VALIDATION_TOLERANCE_RAD:
            supported = False
            reason = "kinematic_factorization_validation_failed"
        axial_index = None
        axial_angle = None
        axial_sensitivity = None
        runner_up = None
        low_confidence = False
        if supported and proximal_mode != "full":
            supported = False
            reason = "proximal_mapping_does_not_define_full_orientation"
        if supported and mode == "axis":
            if primary is None or not sensitivities:
                supported = False
                reason = "distal_primary_axis_missing"
            else:
                best = int(np.argmin(sensitivities))
                ordered = sorted(float(value) for value in sensitivities)
                runner_up = ordered[1]
                axial_index = best
                axial_angle = float(alignment_angles[best])
                axial_sensitivity = float(sensitivities[best])
                # Ignore-axial semantics must correspond to the revolute axis
                # immediately preceding the mapped distal Link.  If another axis
                # looks more axial, the model/mapping is ambiguous and we fall back.
                if best != 2:
                    supported = False
                    reason = "distal_preceding_joint_is_not_unique_axial_axis"
                elif (
                    axial_angle > AXIAL_MAX_ANGLE_DEG
                    or axial_sensitivity > AXIAL_MAX_SENSITIVITY
                    or runner_up - axial_sensitivity < AXIAL_SENSITIVITY_MARGIN
                ):
                    supported = False
                    reason = "distal_preceding_axial_axis_is_ambiguous"
                else:
                    low_confidence = axial_angle > 15.0
        elif supported and mode != "full":
            supported = False
            reason = "unsupported_mapping_mode"

        candidates.append(AnalyticJointCluster(
            cluster_id=f"{proximal_link}->{distal_link}",
            proximal_link=proximal_link,
            distal_link=distal_link,
            proximal_segment=str(mappings[proximal_link].get("source_segment") or ""),
            distal_segment=str(distal_mapping.get("source_segment") or ""),
            mapping_mode=mode,
            body_ids=tuple(bodies),
            joint_ids=tuple(joints),  # type: ignore[arg-type]
            joint_names=tuple(
                _name(model, mujoco.mjtObj.mjOBJ_JOINT, joint_id) for joint_id in joints
            ),  # type: ignore[arg-type]
            qpos_addresses=tuple(int(model.jnt_qposadr[j]) for j in joints),  # type: ignore[arg-type]
            dof_addresses=tuple(int(model.jnt_dofadr[j]) for j in joints),  # type: ignore[arg-type]
            joint_limited=tuple(bool(model.jnt_limited[j]) for j in joints),  # type: ignore[arg-type]
            joint_ranges=tuple(
                tuple(float(x) for x in model.jnt_range[j]) for j in joints
            ),  # type: ignore[arg-type]
            axes_proximal_zero=axes_array,
            home_rotation=home_rotation,
            fixed_body_positions=tuple(
                tuple(float(x) for x in model.body_pos[body_id]) for body_id in bodies
            ),
            fixed_body_quaternions=tuple(
                tuple(float(x) for x in model.body_quat[body_id]) for body_id in bodies
            ),
            rank_ratio_max=rank_ratio,
            fk_reconstruction_error_rad=reconstruction_error,
            supported=supported,
            detection_reason=reason,
            primary_axis_local=primary,
            axial_joint_index=axial_index,
            axial_alignment_deg=axial_angle,
            axial_sensitivity=axial_sensitivity,
            axial_runner_up_sensitivity=runner_up,
            low_confidence=low_confidence,
        ))

    joint_owners: dict[int, list[int]] = {}
    for cluster_index, cluster in enumerate(candidates):
        for joint_id in cluster.joint_ids:
            joint_owners.setdefault(joint_id, []).append(cluster_index)
    conflicted = {
        cluster_index for owners in joint_owners.values() if len(owners) > 1
        for cluster_index in owners
    }
    return [
        replace(cluster, supported=False, detection_reason="overlapping_cluster")
        if index in conflicted else cluster
        for index, cluster in enumerate(candidates)
    ]


def _three_axis_candidates(
    target: np.ndarray, axes: np.ndarray, previous: np.ndarray,
    limited: tuple[bool, bool, bool], ranges: tuple[tuple[float, float], ...],
) -> list[tuple[np.ndarray, int, bool]]:
    a1, a2, a3 = axes
    constant = float(np.dot(a1, a2) * np.dot(a2, a3))
    cosine_term = float(np.dot(a1, a3) - constant)
    sine_term = float(np.dot(a1, np.cross(a2, a3)))
    radius = math.hypot(cosine_term, sine_term)
    if radius < 1e-10:
        return []
    value = (float(np.dot(a1, target @ a3)) - constant) / radius
    if value < -1.0 - 1e-8 or value > 1.0 + 1e-8:
        return []
    value = float(np.clip(value, -1.0, 1.0))
    phase = math.atan2(sine_term, cosine_term)
    middle_offset = math.acos(value)
    raw_middle = [phase + middle_offset, phase - middle_offset]
    output: list[tuple[np.ndarray, int, bool]] = []
    for branch, q2 in enumerate(raw_middle):
        source = _rotation(a2, q2) @ a3
        destination = target @ a3
        q1 = _axis_angle_from_vectors(a1, source, destination)
        singular = q1 is None
        q1_values = [float(previous[0])] if q1 is None else [q1]
        for q1_value in q1_values:
            remainder = _rotation(a2, -q2) @ _rotation(a1, -q1_value) @ target
            q3 = _angle_about_axis(remainder, a3)
            for lifted in itertools.product(
                _lift_angle(q1_value, previous[0], limited[0], ranges[0]),
                _lift_angle(q2, previous[1], limited[1], ranges[1]),
                _lift_angle(q3, previous[2], limited[2], ranges[2]),
            ):
                candidate = np.asarray(lifted)
                rebuilt = (
                    _rotation(a1, candidate[0])
                    @ _rotation(a2, candidate[1])
                    @ _rotation(a3, candidate[2])
                )
                if _rotation_error(rebuilt, target) <= FK_TOLERANCE_RAD:
                    output.append((candidate, branch, singular))
    return output


def _two_axis_candidates(
    target_direction: np.ndarray, axes: np.ndarray, home_direction: np.ndarray,
    axial_gauge: float, previous: np.ndarray,
    limited: tuple[bool, bool, bool], ranges: tuple[tuple[float, float], ...],
) -> list[tuple[np.ndarray, int, bool]]:
    a1, a2, a3 = axes
    source_home = _rotation(a3, axial_gauge) @ home_direction
    constant = float(np.dot(a1, a2) * np.dot(a2, source_home))
    cosine_term = float(np.dot(a1, source_home) - constant)
    sine_term = float(np.dot(a1, np.cross(a2, source_home)))
    radius = math.hypot(cosine_term, sine_term)
    if radius < 1e-10:
        return []
    value = (float(np.dot(a1, target_direction)) - constant) / radius
    if value < -1.0 - 1e-8 or value > 1.0 + 1e-8:
        return []
    value = float(np.clip(value, -1.0, 1.0))
    phase = math.atan2(sine_term, cosine_term)
    middle_offset = math.acos(value)
    output: list[tuple[np.ndarray, int, bool]] = []
    for branch, q2 in enumerate((phase + middle_offset, phase - middle_offset)):
        source = _rotation(a2, q2) @ source_home
        q1 = _axis_angle_from_vectors(a1, source, target_direction)
        if q1 is None:
            q1 = float(previous[0])
            singular = True
        else:
            singular = False
        for lifted in itertools.product(
            _lift_angle(q1, previous[0], limited[0], ranges[0]),
            _lift_angle(q2, previous[1], limited[1], ranges[1]),
        ):
            candidate = np.asarray([lifted[0], lifted[1], axial_gauge])
            rebuilt = (
                _rotation(a1, candidate[0]) @ _rotation(a2, candidate[1])
                @ _rotation(a3, candidate[2]) @ home_direction
            )
            angle = math.acos(float(np.clip(np.dot(rebuilt, target_direction), -1.0, 1.0)))
            if angle <= FK_TOLERANCE_RAD:
                output.append((candidate, branch, singular))
    return output


def build_analytic_joint_target_profile(
    runtime: Any,
    config: dict[str, Any],
    target_quaternions_by_link: dict[str, np.ndarray],
    target_directions_by_link: dict[str, np.ndarray],
) -> AnalyticJointTargetProfile:
    """Generate all-frame targets before the Mink frame loop."""
    clusters = tuple(detect_analytic_joint_clusters(runtime, config))
    hinge_ids = [
        joint_id for joint_id in range(runtime.model.njnt)
        if int(runtime.model.jnt_type[joint_id]) == int(mujoco.mjtJoint.mjJNT_HINGE)
    ]
    joint_names = tuple(
        _name(runtime.model, mujoco.mjtObj.mjOBJ_JOINT, joint_id)
        for joint_id in hinge_ids
    )
    joint_columns = {joint_id: index for index, joint_id in enumerate(hinge_ids)}
    frame_count = 0
    if target_quaternions_by_link:
        frame_count = len(next(iter(target_quaternions_by_link.values())))
    target = np.full((frame_count, len(hinge_ids)), np.nan, dtype=np.float64)
    enabled = np.zeros_like(target, dtype=bool)
    branches = np.full((frame_count, len(clusters)), -1, dtype=np.int16)
    singular = np.zeros((frame_count, len(clusters)), dtype=bool)
    initial = np.asarray(runtime.initial_qpos, dtype=float)

    for cluster_index, cluster in enumerate(clusters):
        if not cluster.supported:
            continue
        previous = np.asarray([initial[address] for address in cluster.qpos_addresses])
        axial_gauge = float(previous[2])
        for frame in range(frame_count):
            candidates: list[tuple[np.ndarray, int, bool]] = []
            if cluster.mapping_mode == "full":
                proximal_q = target_quaternions_by_link[cluster.proximal_link][frame]
                distal_q = target_quaternions_by_link[cluster.distal_link][frame]
                relative = _quat_matrix(proximal_q).T @ _quat_matrix(distal_q)
                normalized_target = relative @ cluster.home_rotation.T
                candidates = _three_axis_candidates(
                    normalized_target, cluster.axes_proximal_zero, previous,
                    cluster.joint_limited, cluster.joint_ranges,
                )
            else:
                proximal_q = target_quaternions_by_link[cluster.proximal_link][frame]
                direction_world = target_directions_by_link[cluster.distal_link][frame]
                direction_proximal = _quat_matrix(proximal_q).T @ direction_world
                home_direction = cluster.home_rotation @ cluster.primary_axis_local
                candidates = _two_axis_candidates(
                    direction_proximal, cluster.axes_proximal_zero, home_direction,
                    axial_gauge, previous, cluster.joint_limited, cluster.joint_ranges,
                )
            if not candidates:
                continue
            candidate, branch, is_singular = min(
                candidates, key=lambda item: float(np.sum((item[0] - previous) ** 2))
            )
            branches[frame, cluster_index] = branch
            singular[frame, cluster_index] = is_singular
            target_indices = (0, 1, 2) if cluster.mapping_mode == "full" else (0, 1)
            for local_index in target_indices:
                column = joint_columns[cluster.joint_ids[local_index]]
                target[frame, column] = candidate[local_index]
                enabled[frame, column] = True
            previous = candidate
            axial_gauge = float(candidate[2])
    return AnalyticJointTargetProfile(
        joint_names=joint_names,
        target_rad=target,
        target_enabled=enabled,
        cluster_ids=tuple(cluster.cluster_id for cluster in clusters),
        selected_branch=branches,
        singularity_flag=singular,
        clusters=clusters,
    )
