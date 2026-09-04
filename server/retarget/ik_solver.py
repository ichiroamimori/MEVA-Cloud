# -*- coding: utf-8 -*-
"""Stage-agnostic Mink IK sequence solver.

Target generation belongs to the stage prepare modules.  This module only
manages sequence state and solves the supplied Mink tasks in their given order.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

import mujoco
import mink
import numpy as np
from mink.limits.limit import Constraint, Limit
from mink.exceptions import NoSolutionFound

try:
    from .robot_model_info import geoms_are_directly_adjacent
except ImportError:
    from robot_model_info import geoms_are_directly_adjacent


DEFAULT_ACCELERATION_WEIGHT_AT_2X_LIMIT = 0.1


@dataclass(frozen=True)
class IKDiagnosticTarget:
    key: str
    metadata: dict[str, Any]
    measure: Callable[[Any], float]


@dataclass(frozen=True)
class PreparedIKFrame:
    tasks: list[Any]
    diagnostics: list[IKDiagnosticTarget] = field(default_factory=list)


@dataclass(frozen=True)
class IKFrameSpec:
    source_frame: int
    prepare: Callable[[Any], PreparedIKFrame]
    # Optional per-frame starting configuration.  When omitted, the solver keeps
    # its historical warm-start behavior (used by Primary).  Main supplies the
    # corresponding Primary pose after its Pelvis-only initial Z shift.
    initial_q: np.ndarray | None = None


@dataclass(frozen=True)
class SolverSettings:
    solver_name: str
    dt_s: float
    global_damping: float
    max_iterations: int
    convergence_joint_delta_deg: float
    convergence_consecutive_iterations: int
    output_frame_dt_s: float
    enforce_hard_xml_limits: bool
    joint_limit_avoidance: dict[str, Any]
    velocity_limit_enabled: bool
    velocity_limit_default_rad_s: float
    velocity_limit_by_joint: dict[str, float]
    acceleration_limit_enabled: bool
    acceleration_limit_by_joint: dict[str, float]
    acceleration_weight_at_2x_limit: float
    self_collision_avoidance: dict[str, Any]
    temporal_regularization_enabled: bool
    temporal_regularization_cost: float | np.ndarray
    iteration_diagnostics: bool = False


@dataclass
class IKSequenceResult:
    qpos: np.ndarray
    diagnostics: list[tuple]
    diagnostic_rows: list[dict[str, Any]]
    diagnostic_values_by_key: dict[str, list[float]]
    iteration_diagnostic_values: dict[int, dict[str, list[float]]] | None
    iteration_joint_deltas: dict[int, dict[str, list[float]]] | None
    iteration_joint_delta_rows: list[dict[str, Any]] | None
    acceleration_soft_limit_rows: list[dict[str, Any]] | None
    diagnostic_hinges: list[tuple[str, int]] | None
    collision_backtracking_rows: list[dict[str, Any]] = field(default_factory=list)


class IKSequenceFailure(RuntimeError):
    """Fatal per-frame IK failure with the already completed sequence attached."""

    def __init__(
        self, message: str, *, result: IKSequenceResult,
        output_index: int, source_frame: int,
    ) -> None:
        super().__init__(message)
        self.result = result
        self.output_index = int(output_index)
        self.source_frame = int(source_frame)


def build_solver_settings(
    *,
    model,
    cfg: dict,
    output_frame_dt_s: float,
    iteration_diagnostics: bool = False,
) -> SolverSettings:
    """Translate common config keys to identical Primary/Main semantics."""
    solver_cfg = dict(cfg["solver"])
    temporal_cfg = dict(cfg.get("temporal_regularization", {}))
    temporal_cost = float(temporal_cfg.get("cost", 0.0))
    if not np.isfinite(temporal_cost) or temporal_cost < 0.0:
        raise ValueError(
            "temporal_regularization.cost must be a finite non-negative number"
        )
    joint_limit_cfg = dict(cfg.get("joint_limit_avoidance", {}))
    velocity_cfg = dict(cfg.get(
        "interframe_joint_velocity_limit", cfg.get("joint_velocity_limit", {})
    ))
    velocity_enabled, velocity_default, velocity_by_joint = (
        resolve_joint_velocity_limit(model, velocity_cfg)
    )
    acceleration_enabled, acceleration_by_joint = resolve_joint_acceleration_limit(
        model, cfg.get("interframe_joint_acceleration_limit", {})
    )
    acceleration_weight_at_2x = float(
        cfg.get("interframe_joint_acceleration_limit", {}).get(
            "weight_at_2x_limit", DEFAULT_ACCELERATION_WEIGHT_AT_2X_LIMIT
        )
    )
    if not np.isfinite(acceleration_weight_at_2x) or acceleration_weight_at_2x < 0.0:
        raise ValueError(
            "interframe_joint_acceleration_limit.weight_at_2x_limit "
            "must be finite and non-negative"
        )
    print(
        "JOINT ACCELERATION:",
        (
            f"enabled, soft boundary task, weight_at_2x_limit="
            f"{acceleration_weight_at_2x:g}, per-iteration"
            if acceleration_enabled else "disabled"
        ),
    )
    return SolverSettings(
        solver_name=str(solver_cfg["name"]),
        dt_s=float(solver_cfg["dt_s"]),
        global_damping=float(solver_cfg["global_damping"]),
        max_iterations=int(solver_cfg.get(
            "max_iterations_per_frame", solver_cfg.get("iterations_per_frame", 20)
        )),
        convergence_joint_delta_deg=float(
            solver_cfg.get("convergence_joint_delta_deg", 0.01)
        ),
        convergence_consecutive_iterations=int(
            solver_cfg.get("convergence_consecutive_iterations", 2)
        ),
        output_frame_dt_s=float(output_frame_dt_s),
        enforce_hard_xml_limits=bool(
            joint_limit_cfg.get("enforce_hard_xml_limits", True)
        ),
        joint_limit_avoidance=joint_limit_cfg,
        velocity_limit_enabled=velocity_enabled,
        velocity_limit_default_rad_s=velocity_default,
        velocity_limit_by_joint=velocity_by_joint,
        acceleration_limit_enabled=acceleration_enabled,
        acceleration_limit_by_joint=acceleration_by_joint,
        acceleration_weight_at_2x_limit=acceleration_weight_at_2x,
        self_collision_avoidance=dict(cfg.get("self_collision_avoidance", {})),
        temporal_regularization_enabled=bool(temporal_cfg.get("enabled", False)),
        temporal_regularization_cost=temporal_cost,
        iteration_diagnostics=bool(iteration_diagnostics),
    )


def hinge_info(model):
    out = []
    for jid in range(model.njnt):
        if model.jnt_type[jid] != mujoco.mjtJoint.mjJNT_HINGE:
            continue
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, jid)
        out.append((
            jid,
            name,
            int(model.jnt_qposadr[jid]),
            int(model.jnt_dofadr[jid]),
            bool(model.jnt_limited[jid]),
            *map(float, model.jnt_range[jid]),
        ))
    return out


def limit_start_ratio(default_setting, override_setting=None):
    override_setting = dict(override_setting or {})
    if "limit_zone_percent" in override_setting:
        zone_percent = float(override_setting["limit_zone_percent"])
        if not np.isfinite(zone_percent) or not 0.0 <= zone_percent <= 50.0:
            raise ValueError("limit_zone_percent must be between 0 and 50")
        return 1.0 - 2.0 * zone_percent / 100.0
    if "start_ratio" in override_setting:
        start = float(override_setting["start_ratio"])
        if not np.isfinite(start) or not 0.0 <= start <= 1.0:
            raise ValueError("start_ratio must be between 0 and 1")
        return start
    if "limit_zone_percent" in default_setting:
        zone_percent = float(default_setting["limit_zone_percent"])
        if not np.isfinite(zone_percent) or not 0.0 <= zone_percent <= 50.0:
            raise ValueError("limit_zone_percent must be between 0 and 50")
        return 1.0 - 2.0 * zone_percent / 100.0
    start = float(default_setting.get("start_ratio", 0.8))
    if not np.isfinite(start) or not 0.0 <= start <= 1.0:
        raise ValueError("start_ratio must be between 0 and 1")
    return start


def joint_limit_avoidance_target_and_cost(model, q, cfg):
    """Build an edge-only posture target that pushes limited hinges inward.

    The limit-zone cost is positional, not velocity damping. Inside the safe
    interval the task is inactive. Once a hinge enters either edge zone, its
    target is the corresponding safe-zone boundary and its weight rises from
    ``base_cost`` to ``max_cost`` toward the XML limit.
    """
    target = np.asarray(q, dtype=float).copy()
    cost = np.zeros(model.nv, dtype=float)
    state_by_joint: dict[str, dict[str, float | str]] = {}
    if not cfg.get("enabled", False):
        return target, cost, state_by_joint
    default_setting = dict(cfg.get("default", {}))
    for _, name, qadr, dadr, limited, lo, hi in hinge_info(model):
        if not limited or hi <= lo:
            continue
        override = dict(cfg.get("overrides", {}).get(name, {}))
        setting = dict(default_setting)
        setting.update(override)
        start = limit_start_ratio(default_setting, override)
        base_cost = float(setting.get("base_cost", 0.01))
        max_cost = float(setting.get("max_cost", 0.2))
        exponent = float(setting.get("exponent", 2.0))
        if not np.isfinite(base_cost) or base_cost < 0.0:
            raise ValueError(f"base_cost must be non-negative for {name}")
        if not np.isfinite(max_cost) or max_cost < base_cost:
            raise ValueError(f"max_cost must be finite and >= base_cost for {name}")
        if not np.isfinite(exponent) or exponent <= 0.0:
            raise ValueError(f"exponent must be positive for {name}")
        mid = (lo + hi) / 2.0
        half = (hi - lo) / 2.0
        safe_half = start * half
        safe_lo = mid - safe_half
        safe_hi = mid + safe_half
        value = float(q[qadr])
        side = "safe"
        penetration = 0.0
        zone_width = max(1e-9, half - safe_half)
        if value < safe_lo:
            side = "lower"
            target[qadr] = safe_lo
            penetration = safe_lo - value
        elif value > safe_hi:
            side = "upper"
            target[qadr] = safe_hi
            penetration = value - safe_hi
        if side != "safe":
            t = float(np.clip(penetration / zone_width, 0.0, 1.0))
            cost[dadr] = base_cost + (max_cost - base_cost) * (t ** exponent)
        state_by_joint[name] = {
            "side": side,
            "position_rad": value,
            "target_rad": float(target[qadr]),
            "zone_fraction": float(np.clip(penetration / zone_width, 0.0, 1.0)),
            "cost": float(cost[dadr]),
        }
    return target, cost, state_by_joint


class JointLimitAvoidanceTask(mink.PostureTask):
    """Position task active only inside the configured XML joint-limit zones."""

    def __init__(self, model, cfg):
        super().__init__(model, cost=np.zeros(model.nv, dtype=float))
        self.model = model
        self.cfg = cfg
        self.state_by_joint: dict[str, dict[str, float | str]] = {}

    def update_from_configuration(self, configuration) -> bool:
        target, cost, states = joint_limit_avoidance_target_and_cost(
            self.model, configuration.q, self.cfg
        )
        self.set_target(target)
        self.set_cost(cost)
        self.state_by_joint = states
        return bool(np.any(cost > 0.0))


class FrameJointVelocityLimit(Limit):
    """Hard hinge bound relative to the previous output-frame solution."""

    def __init__(self, model, max_velocity_by_joint):
        self.model = model
        self._hinges = []
        for _, name, qadr, dadr, limited, _, _ in hinge_info(model):
            vmax = float(max_velocity_by_joint[name])
            if not np.isfinite(vmax) or vmax <= 0.0:
                raise ValueError(f"joint velocity limit must be positive for {name}")
            self._hinges.append((name, qadr, dadr, bool(limited), vmax))
        self._reference_q = None
        self._frame_dt = None

    def set_reference(self, q_reference, frame_dt):
        self._reference_q = np.asarray(q_reference, dtype=float).copy()
        self._frame_dt = float(frame_dt)
        if not np.isfinite(self._frame_dt) or self._frame_dt <= 0.0:
            raise ValueError("frame_dt must be positive")

    def clear_reference(self):
        self._reference_q = None
        self._frame_dt = None

    def compute_qp_inequalities(self, configuration, dt):
        del dt
        if self._reference_q is None:
            return Constraint(None, None)
        n = len(self._hinges)
        G = np.zeros((2 * n, self.model.nv), dtype=float)
        h = np.zeros(2 * n, dtype=float)
        for i, (_, qadr, dadr, limited, vmax) in enumerate(self._hinges):
            delta = float(configuration.q[qadr] - self._reference_q[qadr])
            # A limited hinge has one authoritative XML interval, so wrapping
            # its difference across +/-pi can move the velocity window to an
            # equivalent angle outside that interval.  Only truly continuous
            # hinges use shortest-path wrapping.
            if not limited:
                delta = float(np.arctan2(np.sin(delta), np.cos(delta)))
            allowance = vmax * self._frame_dt
            G[i, dadr] = 1.0
            h[i] = allowance - delta
            G[n + i, dadr] = -1.0
            h[n + i] = allowance + delta
        return Constraint(G, h)


def acceleration_soft_weight(ratio: float, weight_at_2x_limit: float) -> float:
    """Return the configured linear soft cost above the acceleration limit."""
    ratio = float(ratio)
    weight_at_2x_limit = float(weight_at_2x_limit)
    if not np.isfinite(ratio) or ratio < 0.0:
        raise ValueError("acceleration ratio must be finite and non-negative")
    if not np.isfinite(weight_at_2x_limit) or weight_at_2x_limit < 0.0:
        raise ValueError("acceleration weight must be finite and non-negative")
    return weight_at_2x_limit * max(ratio - 1.0, 0.0)


class FrameJointAccelerationSoftTask(mink.PostureTask):
    """Per-iteration soft pull to the nearest acceleration-limit boundary."""

    def __init__(self, model, max_acceleration_by_joint, weight_at_2x_limit):
        super().__init__(model, cost=np.zeros(model.nv, dtype=float))
        self.model = model
        self.weight_at_2x_limit = float(weight_at_2x_limit)
        self._hinges = [
            (name, qadr, dadr, float(max_acceleration_by_joint[name]))
            for _, name, qadr, dadr, _, _, _ in hinge_info(model)
            if name in max_acceleration_by_joint
        ]
        self.state_by_joint: dict[str, dict[str, float]] = {}
        self.clear_reference()

    def set_reference(self, q_previous, q_before_previous, frame_dt):
        self._previous = np.asarray(q_previous, dtype=float).copy()
        self._before_previous = np.asarray(q_before_previous, dtype=float).copy()
        self._frame_dt = float(frame_dt)
        if not np.isfinite(self._frame_dt) or self._frame_dt <= 0.0:
            raise ValueError("frame_dt must be positive")

    def clear_reference(self):
        self._previous = self._before_previous = None
        self._frame_dt = None
        self.state_by_joint = {}

    def update_from_configuration(self, configuration) -> bool:
        target = np.asarray(configuration.q, dtype=float).copy()
        costs = np.zeros(self.model.nv, dtype=float)
        states: dict[str, dict[str, float]] = {}
        if self._previous is None or self._before_previous is None:
            self.set_target(target)
            self.set_cost(costs)
            self.state_by_joint = states
            return False

        for name, qadr, dadr, acceleration_limit in self._hinges:
            previous_step = float(self._previous[qadr] - self._before_previous[qadr])
            previous_step = float(np.arctan2(np.sin(previous_step), np.cos(previous_step)))
            q_pred = float(self._previous[qadr] + previous_step)
            displacement = float(configuration.q[qadr] - q_pred)
            displacement = float(np.arctan2(np.sin(displacement), np.cos(displacement)))
            delta_limit = float(acceleration_limit * self._frame_dt ** 2)
            ratio = abs(displacement) / delta_limit
            weight = acceleration_soft_weight(ratio, self.weight_at_2x_limit)
            if weight > 0.0:
                target[qadr] = q_pred + np.copysign(delta_limit, displacement)
                costs[dadr] = weight
            states[name] = {
                "acceleration_limit_rad_s2": acceleration_limit,
                "actual_acceleration_rad_s2": abs(displacement) / self._frame_dt ** 2,
                "acceleration_ratio": ratio,
                "soft_weight": weight,
            }

        self.set_target(target)
        self.set_cost(costs)
        self.state_by_joint = states
        return bool(np.any(costs > 0.0))


def collision_penalty_and_derivative(
    distance_m,
    *,
    zone_m=0.005,
    penetration_scale_m=0.005,
    penetration_gain=4.0,
):
    """Map signed collision distance to a continuous soft penalty."""
    zone_m = float(zone_m)
    penetration_scale_m = float(penetration_scale_m)
    penetration_gain = float(penetration_gain)
    if not np.isfinite(zone_m) or zone_m <= 0.0:
        raise ValueError("collision penalty zone_m must be positive")
    if not np.isfinite(penetration_scale_m) or penetration_scale_m <= 0.0:
        raise ValueError("collision penetration_scale_m must be positive")
    if not np.isfinite(penetration_gain) or penetration_gain < 0.0:
        raise ValueError("collision penetration_gain must be non-negative")

    distance = np.asarray(distance_m, dtype=float)
    active = distance < zone_m
    penetration = np.maximum(-distance, 0.0)
    penalty = np.where(
        active,
        (zone_m - distance) / zone_m
        + penetration_gain * (penetration / penetration_scale_m) ** 2,
        0.0,
    )
    derivative = np.where(active, -1.0 / zone_m, 0.0)
    derivative = np.where(
        distance < 0.0,
        derivative + 2.0 * penetration_gain * distance / penetration_scale_m ** 2,
        derivative,
    )
    if distance.ndim == 0:
        return float(penalty), float(derivative)
    return penalty, derivative


class SelfCollisionDampingTask(mink.Task):
    """Robot-independent soft self-collision penalty task."""

    def __init__(
        self,
        model,
        geom_pairs,
        zone_m,
        base_cost,
        max_cost,
        gain=1.0,
        penetration_scale_m=0.005,
        penetration_gain=4.0,
    ):
        self.model = model
        self.geom_pairs = list(geom_pairs)
        self.zone_m = float(zone_m)
        self.base_cost = float(base_cost)
        self.max_cost = float(max_cost)
        self.penetration_scale_m = float(penetration_scale_m)
        self.penetration_gain = float(penetration_gain)
        self._distances = np.zeros(len(self.geom_pairs))
        self._penalty_derivatives = np.zeros(len(self.geom_pairs))
        self._fromto = np.zeros((len(self.geom_pairs), 6))
        super().__init__(
            cost=np.full(len(self.geom_pairs), self.base_cost), gain=float(gain)
        )

    def compute_error(self, configuration):
        for index, (geom_a, geom_b) in enumerate(self.geom_pairs):
            self._distances[index] = mujoco.mj_geomDistance(
                self.model, configuration.data, geom_a, geom_b,
                max(self.zone_m * 2.0, self.zone_m + 1e-4), self._fromto[index],
            )
        proximity = np.clip(
            (self.zone_m - self._distances) / max(self.zone_m, 1e-9), 0.0, 1.0
        )
        self.cost = self.base_cost + (self.max_cost - self.base_cost) * proximity ** 2
        penalty, derivative = collision_penalty_and_derivative(
            self._distances,
            zone_m=self.zone_m,
            penetration_scale_m=self.penetration_scale_m,
            penetration_gain=self.penetration_gain,
        )
        # Keep the task residual in metres.  This preserves the pre-contact
        # sensitivity of the former distance residual while retaining the
        # quadratic growth after penetration.
        self._penalty_derivatives[:] = self.zone_m * derivative
        return self.zone_m * penalty

    def compute_jacobian(self, configuration):
        jacobian = np.zeros((len(self.geom_pairs), self.model.nv))
        jac_a = np.zeros((3, self.model.nv))
        jac_b = np.zeros((3, self.model.nv))
        for index, (geom_a, geom_b) in enumerate(self.geom_pairs):
            if self._distances[index] >= self.zone_m:
                continue
            point_a, point_b = self._fromto[index, :3], self._fromto[index, 3:]
            normal = point_b - point_a
            norm = float(np.linalg.norm(normal))
            if norm <= 1e-12:
                continue
            normal /= norm
            mujoco.mj_jac(
                self.model, configuration.data, jac_a, None, point_a,
                int(self.model.geom_bodyid[geom_a]),
            )
            mujoco.mj_jac(
                self.model, configuration.data, jac_b, None, point_b,
                int(self.model.geom_bodyid[geom_b]),
            )
            raw_distance_jacobian = normal @ (jac_b - jac_a)
            # For separated geoms MuJoCo's from-to normal gives +d(distance)/dq.
            # During penetration its witness normal reverses and gives the
            # negative derivative.  The task residual is zone-distance, hence
            # the two regions require opposite signs here.
            distance_violation_jacobian = (
                -raw_distance_jacobian
                if self._distances[index] >= 0.0
                else raw_distance_jacobian
            )
            # Convert d(zone-distance)/dq to d(penalty)/dq.
            jacobian[index] = (
                -self._penalty_derivatives[index]
                * distance_violation_jacobian
            )
        return jacobian


def _activate_broadphase_collision_pairs(
    model,
    data,
    geom_pairs,
    active_indices,
    activation_distance_m,
):
    """Add bounding-sphere-near candidate pairs to a frame-local active set."""
    added = False
    margin = float(activation_distance_m)
    for index, (geom_a, geom_b) in enumerate(geom_pairs):
        if index in active_indices:
            continue
        center_distance = float(np.linalg.norm(
            data.geom_xpos[geom_b] - data.geom_xpos[geom_a]
        ))
        broadphase_distance = center_distance - float(
            model.geom_rbound[geom_a] + model.geom_rbound[geom_b]
        )
        if broadphase_distance <= margin:
            active_indices.add(index)
            added = True
    return added


def resolve_joint_velocity_limit(model, velocity_cfg):
    velocity_cfg = dict(velocity_cfg or {})
    enabled = bool(velocity_cfg.get("enabled", True))
    default_rad_s = float(velocity_cfg.get("default_rad_s", 3.0 * np.pi))
    overrides = dict(velocity_cfg.get("overrides", {}))
    if not np.isfinite(default_rad_s) or default_rad_s <= 0.0:
        raise ValueError("interframe_joint_velocity_limit.default_rad_s must be positive")
    values = {}
    for _, name, _, _, _, _, _ in hinge_info(model):
        raw = overrides.get(name, default_rad_s)
        if isinstance(raw, dict):
            raw = raw.get("max_rad_s", default_rad_s)
        vmax = float(raw)
        if not np.isfinite(vmax) or vmax <= 0.0:
            raise ValueError(f"bad joint velocity limit for {name}: {vmax}")
        values[name] = vmax
    return enabled, default_rad_s, values


def resolve_joint_acceleration_limit(model, acceleration_cfg):
    cfg = dict(acceleration_cfg or {})
    enabled = bool(cfg.get("enabled", False))
    default = float(cfg.get("default_rad_s2", 0.0))
    overrides = dict(cfg.get("overrides", {}))
    values = {}
    for _, name, _, _, _, _, _ in hinge_info(model):
        raw = overrides.get(name, default)
        if isinstance(raw, dict):
            raw = raw.get("max_rad_s2", default)
        value = float(raw)
        if value > 0.0 and np.isfinite(value):
            values[name] = value
        elif enabled and name in overrides:
            raise ValueError(f"bad joint acceleration limit for {name}: {value}")
    return bool(enabled and values), values


def extract_output(model, q, order: str):
    free = [
        j for j in range(model.njnt)
        if model.jnt_type[j] == mujoco.mjtJoint.mjJNT_FREE
    ]
    if len(free) != 1:
        raise ValueError(f"expected 1 free joint, got {len(free)}")
    qadr = int(model.jnt_qposadr[free[0]])
    pos = q[qadr:qadr + 3].copy()
    wxyz = np.asarray(q[qadr + 3:qadr + 7], dtype=float)
    wxyz = wxyz / np.linalg.norm(wxyz)
    rot = wxyz[[1, 2, 3, 0]] if order == "xyzw" else wxyz.copy()
    dof = np.array([q[qa] for _, _, qa, _, _, _, _ in hinge_info(model)])
    return pos, rot, dof


def _validate_settings(settings: SolverSettings):
    if settings.max_iterations < 1:
        raise ValueError("solver.max_iterations_per_frame must be >= 1")
    if (
        not np.isfinite(settings.convergence_joint_delta_deg)
        or settings.convergence_joint_delta_deg < 0.0
    ):
        raise ValueError(
            "solver.convergence_joint_delta_deg must be a finite non-negative number"
        )
    if settings.convergence_consecutive_iterations < 1:
        raise ValueError("solver.convergence_consecutive_iterations must be >= 1")
    if not np.isfinite(settings.dt_s) or settings.dt_s <= 0.0:
        raise ValueError("solver.dt_s must be positive")
    temporal_cost = np.asarray(settings.temporal_regularization_cost, dtype=float)
    if not np.all(np.isfinite(temporal_cost)) or np.any(temporal_cost < 0.0):
        raise ValueError("temporal regularization cost must be finite and non-negative")


def _has_temporal_regularization(settings: SolverSettings) -> bool:
    return bool(
        settings.temporal_regularization_enabled
        and np.any(np.asarray(settings.temporal_regularization_cost, dtype=float) > 0.0)
    )


def solve_ik_sequence(
    *,
    model,
    initial_configuration,
    frame_specs: list[IKFrameSpec],
    solver_settings: SolverSettings,
    diagnostic_keys: list[str],
) -> IKSequenceResult:
    """Solve one ordered output sequence while retaining inter-frame state."""
    _validate_settings(solver_settings)
    conf = initial_configuration
    temporal_posture = None
    if _has_temporal_regularization(solver_settings):
        temporal_posture = mink.PostureTask(
            model, cost=solver_settings.temporal_regularization_cost
        )
    joint_limit_avoidance_task = JointLimitAvoidanceTask(
        model, solver_settings.joint_limit_avoidance
    )

    limits = (
        [mink.ConfigurationLimit(model)]
        if solver_settings.enforce_hard_xml_limits
        else []
    )
    frame_velocity_limit = None
    if solver_settings.velocity_limit_enabled:
        frame_velocity_limit = FrameJointVelocityLimit(
            model, solver_settings.velocity_limit_by_joint
        )
        limits.append(frame_velocity_limit)
    frame_acceleration_task = None
    if solver_settings.acceleration_limit_enabled:
        frame_acceleration_task = FrameJointAccelerationSoftTask(
            model,
            solver_settings.acceleration_limit_by_joint,
            solver_settings.acceleration_weight_at_2x_limit,
        )
    collision_damping_task = None
    collision_candidate_pairs = []
    collision_mode = "manual"
    collision_zone = 0.005
    collision_detection_distance = 0.01
    collision_base_cost = 0.01
    collision_max_cost = 0.2
    collision_penetration_scale = 0.005
    collision_penetration_gain = 4.0
    collision_task_gain = 0.2
    collision_cfg = dict(solver_settings.self_collision_avoidance or {})
    selected_collision_pairs = list(collision_cfg.get("selected_pairs", []))
    if collision_cfg.get("enabled", False) and selected_collision_pairs:
        collision_mode = str(collision_cfg.get("mode", "manual")).strip().lower()
        if collision_mode not in {"manual", "auto"}:
            raise ValueError("self_collision_avoidance.mode must be manual or auto")
        seen_collision_pairs: set[tuple[int, int]] = set()
        ignored_adjacent_pairs: list[str] = []
        for key in selected_collision_pairs:
            try:
                geom_a, geom_b = (int(x) for x in str(key).split(":", 1))
            except (TypeError, ValueError) as exc:
                raise ValueError(f"bad self-collision pair key: {key}") from exc
            if not (0 <= geom_a < model.ngeom and 0 <= geom_b < model.ngeom):
                raise ValueError(f"self-collision geom id out of range: {key}")
            geom_pair = tuple(sorted((geom_a, geom_b)))
            if geoms_are_directly_adjacent(model, *geom_pair):
                ignored_adjacent_pairs.append(f"{geom_pair[0]}:{geom_pair[1]}")
                continue
            if geom_pair in seen_collision_pairs:
                continue
            seen_collision_pairs.add(geom_pair)
            collision_candidate_pairs.append(geom_pair)
        if ignored_adjacent_pairs:
            print(
                "Self-collision: ignored directly adjacent body pairs from config: "
                + ", ".join(ignored_adjacent_pairs),
                flush=True,
            )
        collision_zone = float(collision_cfg.get("damping", {}).get("limit_zone_m", 0.005))
        collision_base_cost = float(collision_cfg.get("damping", {}).get("base_cost", 0.01))
        collision_max_cost = float(collision_cfg.get("damping", {}).get("max_cost", 0.2))
        collision_penetration_scale = float(
            collision_cfg.get("damping", {}).get("penetration_scale_m", 0.005)
        )
        collision_penetration_gain = float(
            collision_cfg.get("damping", {}).get("penetration_gain", 4.0)
        )
        collision_task_gain = float(collision_cfg.get("damping", {}).get(
            "gain",
            collision_cfg.get("backtracking", {}).get("initial_gain", 0.2),
        ))
        collision_detection_distance = max(
            collision_zone * 2.0, collision_zone + 1e-4
        )
        if not np.isfinite(collision_zone) or collision_zone <= 0.0:
            raise ValueError("self_collision_avoidance.damping.limit_zone_m must be positive")
        if not np.isfinite(collision_base_cost) or collision_base_cost < 0.0 or not np.isfinite(collision_max_cost) or collision_max_cost < collision_base_cost:
            raise ValueError("self-collision damping costs must satisfy 0 <= base_cost <= max_cost")
        if not np.isfinite(collision_penetration_scale) or collision_penetration_scale <= 0.0:
            raise ValueError("self_collision_avoidance.damping.penetration_scale_m must be positive")
        if not np.isfinite(collision_penetration_gain) or collision_penetration_gain < 0.0:
            raise ValueError("self_collision_avoidance.damping.penetration_gain must be non-negative")
        if not np.isfinite(collision_task_gain) or not 0.0 < collision_task_gain <= 1.0:
            raise ValueError("self_collision_avoidance.damping.gain must be in (0, 1]")

    qpos = []
    diag = []
    diagnostic_rows = []
    diagnostic_values_by_key = {key: [] for key in diagnostic_keys}
    hinges = [(name, qadr) for _, name, qadr, _, _, _, _ in hinge_info(model)]

    iteration_values = None
    iteration_joint_deltas = None
    iteration_joint_delta_rows = None
    acceleration_soft_limit_rows = None
    collision_backtracking_rows: list[dict[str, Any]] = []
    diagnostic_hinges = None
    if solver_settings.iteration_diagnostics:
        iteration_values = {
            i: {key: [] for key in diagnostic_keys}
            for i in range(solver_settings.max_iterations + 1)
        }
        diagnostic_hinges = list(hinges)
        iteration_joint_deltas = {
            i: {name: [] for name, _ in diagnostic_hinges}
            for i in range(1, solver_settings.max_iterations + 1)
        }
        iteration_joint_delta_rows = []
        acceleration_soft_limit_rows = []

    first_source = frame_specs[0].source_frame if frame_specs else 0
    print(f"[0/{len(frame_specs)}] frame {first_source}")

    q_history: list[np.ndarray] = []

    def current_result() -> IKSequenceResult:
        return IKSequenceResult(
            qpos=np.asarray(qpos),
            diagnostics=diag,
            diagnostic_rows=diagnostic_rows,
            diagnostic_values_by_key=diagnostic_values_by_key,
            iteration_diagnostic_values=iteration_values,
            iteration_joint_deltas=iteration_joint_deltas,
            iteration_joint_delta_rows=iteration_joint_delta_rows,
            acceleration_soft_limit_rows=acceleration_soft_limit_rows,
            diagnostic_hinges=diagnostic_hinges,
            collision_backtracking_rows=collision_backtracking_rows,
        )

    for output_index, frame_spec in enumerate(frame_specs):
        source_frame = int(frame_spec.source_frame)
        q_previous = conf.q.copy() if output_index > 0 else None
        if frame_spec.initial_q is not None:
            initial_q = np.asarray(frame_spec.initial_q, dtype=float)
            if initial_q.shape != (model.nq,):
                raise ValueError(
                    f"frame {source_frame} initial_q must have shape "
                    f"({model.nq},), got {initial_q.shape}"
                )
            conf.update(q=initial_q)
        if q_previous is not None and temporal_posture is not None:
            temporal_posture.set_target(q_previous)

        try:
            prepared = frame_spec.prepare(conf)
        except Exception as exc:
            raise IKSequenceFailure(
                f"IK target preparation failed at output frame {output_index}, "
                f"source frame {source_frame}: {type(exc).__name__}: {exc}",
                result=current_result(), output_index=output_index,
                source_frame=source_frame,
            ) from exc
        solve_tasks_base = list(prepared.tasks)
        frame_active_collision_indices = (
            set(range(len(collision_candidate_pairs)))
            if collision_mode == "manual" else set()
        )
        collision_components_dirty = bool(frame_active_collision_indices)
        collision_damping_task = None

        def activate_auto_collision_pairs():
            nonlocal collision_components_dirty
            if collision_mode != "auto" or not collision_candidate_pairs:
                return False
            added = _activate_broadphase_collision_pairs(
                model, conf.data, collision_candidate_pairs,
                frame_active_collision_indices, collision_detection_distance,
            )
            collision_components_dirty = collision_components_dirty or added
            return added

        def rebuild_collision_components_if_needed():
            nonlocal collision_components_dirty, collision_damping_task
            if not collision_components_dirty:
                return
            active_pairs = [
                collision_candidate_pairs[index]
                for index in sorted(frame_active_collision_indices)
            ]
            if active_pairs:
                collision_damping_task = SelfCollisionDampingTask(
                    model, active_pairs, collision_zone, collision_base_cost,
                    collision_max_cost, gain=collision_task_gain,
                    penetration_scale_m=collision_penetration_scale,
                    penetration_gain=collision_penetration_gain,
                )
            else:
                collision_damping_task = None
            collision_components_dirty = False
        if q_previous is not None and temporal_posture is not None:
            solve_tasks_base.append(temporal_posture)

        if frame_velocity_limit is not None:
            if q_previous is None:
                frame_velocity_limit.clear_reference()
            else:
                frame_velocity_limit.set_reference(
                    q_previous, solver_settings.output_frame_dt_s
                )
        if frame_acceleration_task is not None:
            if len(q_history) < 2:
                frame_acceleration_task.clear_reference()
            else:
                frame_acceleration_task.set_reference(
                    q_history[-1], q_history[-2], solver_settings.output_frame_dt_s
                )

        def collect_iteration(iteration_index):
            if iteration_values is None:
                return
            for target in prepared.diagnostics:
                iteration_values[iteration_index][target.key].append(
                    float(target.measure(conf))
                )

        collect_iteration(0)
        converged = False
        convergence_hits = 0
        final_max_joint_delta_deg = float("inf")
        iterations_used = 0
        max_joint_limit_cost_this_frame = 0.0
        for iteration_index in range(1, solver_settings.max_iterations + 1):
            activate_auto_collision_pairs()
            rebuild_collision_components_if_needed()
            q_before_iteration = conf.q.copy()
            joint_limit_active = joint_limit_avoidance_task.update_from_configuration(conf)
            joint_limit_cost = joint_limit_avoidance_task.cost
            max_joint_limit_cost_this_frame = max(
                max_joint_limit_cost_this_frame,
                float(np.max(joint_limit_cost)) if len(joint_limit_cost) else 0.0,
            )
            solve_tasks = list(solve_tasks_base)
            if collision_damping_task is not None:
                solve_tasks.append(collision_damping_task)
            solve_limits = list(limits)
            if joint_limit_active:
                solve_tasks.append(joint_limit_avoidance_task)
            if (
                frame_acceleration_task is not None
                and frame_acceleration_task.update_from_configuration(conf)
            ):
                solve_tasks.append(frame_acceleration_task)
            try:
                velocity = mink.solve_ik(
                    conf,
                    solve_tasks,
                    dt=solver_settings.dt_s,
                    solver=solver_settings.solver_name,
                    damping=solver_settings.global_damping,
                    limits=solve_limits,
                    safety_break=True,
                )
            except NoSolutionFound as exc:
                variant_results: dict[str, str] = {}
                variants = {
                    "xml_only": limits[:1] if solver_settings.enforce_hard_xml_limits else [],
                    "velocity_only": [frame_velocity_limit] if frame_velocity_limit is not None else [],
                    "no_limits": [],
                }
                for label, diagnostic_limits in variants.items():
                    try:
                        mink.solve_ik(
                            conf, solve_tasks, dt=solver_settings.dt_s,
                            solver=solver_settings.solver_name,
                            damping=solver_settings.global_damping,
                            limits=diagnostic_limits, safety_break=True,
                        )
                        variant_results[label] = "feasible"
                    except Exception as diagnostic_exc:  # diagnostic only
                        variant_results[label] = type(diagnostic_exc).__name__
                message = (
                    "Main/Primary IK QP infeasible at "
                    f"output frame {output_index}, source frame {source_frame}, "
                    f"iteration {iteration_index}; variants={variant_results}"
                )
                raise IKSequenceFailure(
                    message, result=current_result(), output_index=output_index,
                    source_frame=source_frame,
                ) from exc
            except Exception as exc:
                raise IKSequenceFailure(
                    "IK solver failed at "
                    f"output frame {output_index}, source frame {source_frame}, "
                    f"iteration {iteration_index}: {type(exc).__name__}: {exc}",
                    result=current_result(), output_index=output_index,
                    source_frame=source_frame,
                ) from exc
            # Self-collision is a soft task.  Integrate the complete QP update
            # so the optimizer can use other joints to escape penetration.
            conf.integrate_inplace(velocity, solver_settings.dt_s)
            if not np.all(np.isfinite(conf.q)):
                raise IKSequenceFailure(
                    "IK produced NaN/Inf at "
                    f"output frame {output_index}, source frame {source_frame}, "
                    f"iteration {iteration_index}",
                    result=current_result(), output_index=output_index,
                    source_frame=source_frame,
                )
            iterations_used = iteration_index
            activated_after_step = activate_auto_collision_pairs()

            per_joint_delta_deg = {}
            for joint_name, qadr in hinges:
                delta_rad = float(conf.q[qadr] - q_before_iteration[qadr])
                delta_rad = float(np.arctan2(np.sin(delta_rad), np.cos(delta_rad)))
                per_joint_delta_deg[joint_name] = float(np.degrees(delta_rad))
            final_max_joint_delta_deg = (
                max(abs(v) for v in per_joint_delta_deg.values())
                if per_joint_delta_deg else 0.0
            )
            if iteration_joint_deltas is not None:
                for joint_name, delta_deg in per_joint_delta_deg.items():
                    iteration_joint_deltas[iteration_index][joint_name].append(delta_deg)
                    iteration_joint_delta_rows.append({
                        "source_frame": source_frame,
                        "iteration": iteration_index,
                        "joint_name": joint_name,
                        "delta_deg": delta_deg,
                        "abs_delta_deg": abs(delta_deg),
                    })
            collect_iteration(iteration_index)
            if activated_after_step:
                convergence_hits = 0
            elif final_max_joint_delta_deg <= solver_settings.convergence_joint_delta_deg:
                convergence_hits += 1
            else:
                convergence_hits = 0
            if convergence_hits >= solver_settings.convergence_consecutive_iterations:
                converged = True
                break

        frame_values = []
        for target in prepared.diagnostics:
            value = float(target.measure(conf))
            diagnostic_values_by_key[target.key].append(value)
            frame_values.append(value)
            diagnostic_rows.append({**target.metadata, "value": value})

        if frame_acceleration_task is not None:
            frame_acceleration_task.update_from_configuration(conf)
            if acceleration_soft_limit_rows is not None:
                for joint_name, state in frame_acceleration_task.state_by_joint.items():
                    acceleration_soft_limit_rows.append({
                        "source_frame": source_frame,
                        "joint_name": joint_name,
                        **state,
                    })

        qpos.append(conf.q.copy())
        q_history.append(conf.q.copy())
        collision_backtracking_rows.append({
            "output_frame": int(output_index),
            "source_frame": source_frame,
            "was_blocked": False,
            "collision_blocked": False,
            "blocked_iterations": 0,
            "final_step_scale": 1.0,
            "final_gain": float(collision_task_gain),
            "final_max_joint_delta_deg": float(final_max_joint_delta_deg),
            "final_max_target_error": float(
                max(frame_values) if frame_values else 0.0
            ),
            "blocking_pairs": [],
        })
        diag.append((
            source_frame,
            float(max_joint_limit_cost_this_frame),
            float(max(frame_values) if frame_values else 0.0),
            int(iterations_used),
            bool(converged),
            float(final_max_joint_delta_deg),
        ))
        completed = output_index + 1
        if completed % 50 == 0 or completed == len(frame_specs):
            print(f"[{completed}/{len(frame_specs)}] frame {source_frame}")

    return current_result()
