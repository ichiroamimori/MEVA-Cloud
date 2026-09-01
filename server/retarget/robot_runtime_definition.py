"""Validated Robot definition shared by Retargeting components.

Manufacturer URDF/MJCF files describe mechanical facts.  The Robot manifest
adds MEVA Cloud semantics which cannot be inferred safely from those files.
This module compiles both inputs into one validated Runtime definition so that
Primary, Main, the Mapping UI, and diagnostics do not interpret manufacturer
XML independently.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
from typing import Any

import mujoco
import numpy as np


class RobotRuntimeDefinitionError(ValueError):
    """Raised when the compiled model and manifest semantics disagree."""


@dataclass(frozen=True)
class BodyOrientationDefinition:
    primary_axis: tuple[float, float, float] | None = None
    primary_source: str | None = None
    secondary_axis: tuple[float, float, float] | None = None
    secondary_name: str | None = None

    @property
    def axis_alignment_supported(self) -> bool:
        return self.primary_axis is not None


@dataclass(frozen=True)
class BodyPointDefinition:
    """A Robot-semantic point fixed in one compiled MuJoCo Body frame."""

    body_name: str
    local_position: tuple[float, float, float]

    def world_position(self, model: mujoco.MjModel, data: mujoco.MjData) -> np.ndarray:
        body_id = mujoco.mj_name2id(
            model, mujoco.mjtObj.mjOBJ_BODY, self.body_name
        )
        if body_id < 0:
            raise RobotRuntimeDefinitionError(
                f"Landmark body not found in compiled model: {self.body_name}"
            )
        rotation = np.asarray(data.xmat[body_id], dtype=np.float64).reshape(3, 3)
        return (
            np.asarray(data.xpos[body_id], dtype=np.float64)
            + rotation @ np.asarray(self.local_position, dtype=np.float64)
        )


@dataclass(frozen=True)
class RobotRuntimeDefinition:
    identity: str
    model_path: Path
    model_format: str
    model: mujoco.MjModel
    initial_qpos: np.ndarray
    body_names: tuple[str, ...]
    joint_names: tuple[str, ...]
    output_joint_names: tuple[str, ...]
    root_body: str
    floating_base: bool
    pelvis_reference: BodyPointDefinition
    orientations: dict[str, BodyOrientationDefinition]
    foot_contacts: dict[str, Any] | None
    retargeting: dict[str, Any]

    def orientation(self, body_name: str) -> BodyOrientationDefinition:
        if body_name not in self.orientations:
            raise RobotRuntimeDefinitionError(
                f"Robot body not found: {self.identity}, body={body_name}"
            )
        return self.orientations[body_name]

    def validate_config(self, config: dict[str, Any]) -> None:
        mappings = config.get("mappings")
        if not isinstance(mappings, list):
            raise RobotRuntimeDefinitionError(
                f"Config mappings must be an array: {self.identity}"
            )
        body_names = set(self.body_names)
        for mapping in mappings:
            if not isinstance(mapping, dict):
                raise RobotRuntimeDefinitionError(
                    f"Invalid Config mapping: {self.identity}"
                )
            target_link = str(mapping.get("target_link") or "")
            if target_link not in body_names:
                raise RobotRuntimeDefinitionError(
                    "Config target_link not found in compiled model: "
                    f"{self.identity}, body={target_link}, model={self.model_path}"
                )
            mode = str(mapping.get("orientation_mode") or "full")
            if mode not in {"full", "axis"}:
                raise RobotRuntimeDefinitionError(
                    f"Unknown orientation_mode {mode!r}: "
                    f"{self.identity}, body={target_link}"
                )
            orientation = self.orientation(target_link)
            if mode == "axis" and not orientation.axis_alignment_supported:
                raise RobotRuntimeDefinitionError(
                    "Ignore Axis Rotation requires a Primary axis: "
                    f"{self.identity}, body={target_link}"
                )
            if (
                mode == "full"
                and str(mapping.get("source_segment") or "")
                in {"LeftHand", "RightHand", "LeftFoot", "RightFoot"}
                and orientation.secondary_axis is None
            ):
                raise RobotRuntimeDefinitionError(
                    "Terminal Full Quaternion mapping requires Primary and "
                    f"Secondary axes: {self.identity}, body={target_link}"
                )

        joint_names = set(self.joint_names)
        missing_joints: set[str] = set()
        for section in (
            "joint_limit_avoidance",
            "interframe_joint_velocity_limit",
            "interframe_joint_acceleration_limit",
        ):
            settings = config.get(section)
            overrides = settings.get("overrides") if isinstance(settings, dict) else None
            if isinstance(overrides, dict):
                missing_joints.update(
                    str(name) for name in overrides if str(name) not in joint_names
                )
        if missing_joints:
            raise RobotRuntimeDefinitionError(
                f"Config Joint override not found in compiled model: {self.identity}, "
                f"joints={', '.join(sorted(missing_joints))}, model={self.model_path}"
            )


def _name(model: mujoco.MjModel, object_type: mujoco.mjtObj, index: int) -> str:
    return mujoco.mj_id2name(model, object_type, index) or f"unnamed_{index}"


def _unit_vector(value: Any, *, identity: str, field: str) -> np.ndarray:
    if not (
        isinstance(value, (list, tuple, np.ndarray))
        and len(value) == 3
        and all(
            not isinstance(component, (bool, np.bool_))
            and isinstance(component, (int, float, np.integer, np.floating))
            and math.isfinite(float(component))
            for component in value
        )
    ):
        raise RobotRuntimeDefinitionError(f"Invalid {field} vector: {identity}")
    vector = np.asarray(value, dtype=np.float64)
    length = float(np.linalg.norm(vector))
    if length <= 1e-12:
        raise RobotRuntimeDefinitionError(f"Zero-length {field} vector: {identity}")
    return vector / length


def _tuple3(vector: np.ndarray) -> tuple[float, float, float]:
    return tuple(float(component) for component in vector)  # type: ignore[return-value]


def _initial_data(
    model: mujoco.MjModel, initial_pose: dict[str, Any], *, identity: str
) -> mujoco.MjData:
    data = mujoco.MjData(model)
    pose_type = str(initial_pose.get("type") or "model_default")
    if pose_type == "model_default":
        mujoco.mj_resetData(model, data)
    elif pose_type == "keyframe":
        key_name = str(initial_pose.get("name") or "")
        key_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_KEY, key_name)
        if key_id < 0:
            raise RobotRuntimeDefinitionError(
                f"Initial keyframe not found in compiled model: {identity}, "
                f"keyframe={key_name}"
            )
        mujoco.mj_resetDataKeyframe(model, data, key_id)
    else:
        raise RobotRuntimeDefinitionError(
            f"Unknown initial_pose type {pose_type!r}: {identity}"
        )
    mujoco.mj_forward(model, data)
    return data


def _orientation_definitions(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    retargeting: dict[str, Any],
    *,
    identity: str,
) -> dict[str, BodyOrientationDefinition]:
    body_names = {
        _name(model, mujoco.mjtObj.mjOBJ_BODY, body_id): body_id
        for body_id in range(1, model.nbody)
    }
    values = {name: BodyOrientationDefinition() for name in body_names}
    target_geometry = retargeting.get("target_geometry") or {}
    terminal_semantics = retargeting.get("terminal_semantics") or {}
    if not isinstance(target_geometry, dict) or not isinstance(terminal_semantics, dict):
        raise RobotRuntimeDefinitionError(
            f"Robot orientation metadata must be objects: {identity}"
        )

    for body_name, raw_rule in target_geometry.items():
        body_name = str(body_name)
        if body_name not in body_names or not isinstance(raw_rule, dict):
            raise RobotRuntimeDefinitionError(
                f"Invalid orientation geometry body: {identity}, body={body_name}"
            )
        rule_type = str(raw_rule.get("type") or "")
        if rule_type == "local_vector":
            primary = _unit_vector(
                raw_rule.get("vector"), identity=identity,
                field=f"target_geometry.{body_name}.vector",
            )
        elif rule_type == "body_to_body":
            distal_name = str(raw_rule.get("distal_body") or "")
            if distal_name not in body_names or distal_name == body_name:
                raise RobotRuntimeDefinitionError(
                    f"Invalid distal body: {identity}, body={body_name}, "
                    f"distal={distal_name}"
                )
            body_id = body_names[body_name]
            distal_id = body_names[distal_name]
            direction_world = np.asarray(data.xpos[distal_id]) - np.asarray(data.xpos[body_id])
            body_rotation = np.asarray(data.xmat[body_id]).reshape(3, 3)
            primary = _unit_vector(
                body_rotation.T @ direction_world,
                identity=identity,
                field=f"target_geometry.{body_name}.body_to_body",
            )
        else:
            raise RobotRuntimeDefinitionError(
                f"Unknown orientation geometry type {rule_type!r}: "
                f"{identity}, body={body_name}"
            )
        values[body_name] = BodyOrientationDefinition(
            primary_axis=_tuple3(primary), primary_source=f"target_geometry:{rule_type}"
        )

    for body_name, raw_semantic in terminal_semantics.items():
        body_name = str(body_name)
        if body_name not in body_names or not isinstance(raw_semantic, dict):
            raise RobotRuntimeDefinitionError(
                f"Invalid terminal semantic body: {identity}, body={body_name}"
            )
        primary = _unit_vector(
            raw_semantic.get("primary"), identity=identity,
            field=f"terminal_semantics.{body_name}.primary",
        )
        secondary = None
        secondary_name = None
        if "secondary" in raw_semantic:
            secondary = _unit_vector(
                raw_semantic.get("secondary"), identity=identity,
                field=f"terminal_semantics.{body_name}.secondary",
            )
            if float(np.linalg.norm(np.cross(primary, secondary))) <= 1e-12:
                raise RobotRuntimeDefinitionError(
                    f"Parallel terminal semantic axes: {identity}, body={body_name}"
                )
            secondary_name = str(raw_semantic.get("secondary_name") or "")
            if not secondary_name:
                raise RobotRuntimeDefinitionError(
                    f"Terminal secondary_name is missing: {identity}, body={body_name}"
                )
        values[body_name] = BodyOrientationDefinition(
            primary_axis=_tuple3(primary),
            primary_source="terminal_semantics",
            secondary_axis=_tuple3(secondary) if secondary is not None else None,
            secondary_name=secondary_name,
        )
    return values


def _validate_foot_contacts(
    foot_contacts: dict[str, Any] | None,
    body_names: set[str],
    *,
    identity: str,
) -> None:
    if foot_contacts is None:
        return
    offset = foot_contacts.get("robot_foot_to_ground_offset_m")
    if (
        isinstance(offset, bool)
        or not isinstance(offset, (int, float))
        or not math.isfinite(float(offset))
        or float(offset) < 0.0
    ):
        raise RobotRuntimeDefinitionError(
            f"Invalid Robot Foot-to-ground offset: {identity}"
        )
    sides = set(foot_contacts) - {"robot_foot_to_ground_offset_m"}
    if sides != {"left", "right"}:
        raise RobotRuntimeDefinitionError(
            f"Foot contacts must define left and right sides: {identity}"
        )
    for side in ("left", "right"):
        definition = foot_contacts.get(side)
        if not isinstance(definition, dict):
            raise RobotRuntimeDefinitionError(
                f"Invalid {side} Foot contact definition: {identity}"
            )
        body_name = str(definition.get("body") or "")
        if body_name not in body_names:
            raise RobotRuntimeDefinitionError(
                f"Foot body not found in compiled model: {identity}, "
                f"side={side}, body={body_name}"
            )
        points = definition.get("support_points")
        if not isinstance(points, list) or len(points) != 4:
            raise RobotRuntimeDefinitionError(
                f"Foot contact requires four support points: {identity}, side={side}"
            )
        point_names: set[str] = set()
        for point in points:
            if not isinstance(point, dict):
                raise RobotRuntimeDefinitionError(
                    f"Invalid Foot support point: {identity}, side={side}"
                )
            point_name = str(point.get("name") or "")
            if not point_name or point_name in point_names:
                raise RobotRuntimeDefinitionError(
                    f"Invalid or duplicate Foot support point name: "
                    f"{identity}, side={side}"
                )
            point_names.add(point_name)
            _unit_vector_like_position(
                point.get("local_position"), identity=identity,
                field=f"foot_contacts.{side}.{point_name}.local_position",
            )


def _unit_vector_like_position(value: Any, *, identity: str, field: str) -> None:
    """Validate a finite XYZ position without requiring non-zero length."""
    if not (
        isinstance(value, (list, tuple, np.ndarray))
        and len(value) == 3
        and all(
            not isinstance(component, (bool, np.bool_))
            and isinstance(component, (int, float, np.integer, np.floating))
            and math.isfinite(float(component))
            for component in value
        )
    ):
        raise RobotRuntimeDefinitionError(f"Invalid {field}: {identity}")


def _pelvis_reference_definition(
    retargeting: dict[str, Any],
    body_names: set[str],
    *,
    root_body: str,
    identity: str,
) -> BodyPointDefinition:
    """Resolve the Robot point corresponding to the MEVA Pelvis landmark.

    Existing manifests predate ``retargeting.landmarks``.  Their established
    behavior was the Model Root Body origin, which remains the read-only
    fallback.  New Robot manifests should always define this point explicitly.
    """
    landmarks = retargeting.get("landmarks")
    if landmarks is None:
        return BodyPointDefinition(root_body, (0.0, 0.0, 0.0))
    if not isinstance(landmarks, dict):
        raise RobotRuntimeDefinitionError(
            f"retargeting.landmarks must be an object: {identity}"
        )
    raw = landmarks.get("pelvis_reference")
    if not isinstance(raw, dict):
        raise RobotRuntimeDefinitionError(
            f"retargeting.landmarks.pelvis_reference is required: {identity}"
        )
    body_name = str(raw.get("body") or "")
    if body_name not in body_names:
        raise RobotRuntimeDefinitionError(
            f"Pelvis reference body not found in compiled model: {identity}, "
            f"body={body_name}"
        )
    local_position = raw.get("local_position", [0.0, 0.0, 0.0])
    _unit_vector_like_position(
        local_position,
        identity=identity,
        field="landmarks.pelvis_reference.local_position",
    )
    return BodyPointDefinition(
        body_name=body_name,
        local_position=tuple(float(value) for value in local_position),
    )


def load_robot_runtime_definition(
    repository_root: Path, robot: dict[str, Any]
) -> RobotRuntimeDefinition:
    """Compile a runtime Robot config and validate its manifest semantics."""
    identity = "/".join(
        str(robot.get(key) or "unknown") for key in ("manufacturer", "model", "variant")
    )
    relative_model = Path(str(robot.get("model_file") or robot.get("mjcf") or ""))
    root = repository_root.resolve()
    application_root = Path(__file__).resolve().parents[2]
    if relative_model.is_absolute():
        model_path = relative_model.resolve()
    else:
        if ".." in relative_model.parts:
            raise RobotRuntimeDefinitionError(f"Unsafe Runtime Model path: {identity}")
        model_path = (root / relative_model).resolve()
    allowed_roots = {root, application_root}
    if not any(
        model_path == allowed or allowed in model_path.parents
        for allowed in allowed_roots
    ):
        raise RobotRuntimeDefinitionError(f"Runtime Model is outside repository: {identity}")
    model_format = str(robot.get("model_format") or "mjcf").lower()
    if model_format not in {"mjcf", "urdf"}:
        raise RobotRuntimeDefinitionError(
            f"Unsupported Runtime Model format {model_format!r}: {identity}"
        )
    try:
        model = mujoco.MjModel.from_xml_path(str(model_path))
    except Exception as exc:
        raise RobotRuntimeDefinitionError(
            f"Could not compile Runtime Model with MuJoCo: {identity}, path={model_path}"
        ) from exc

    body_names = tuple(
        _name(model, mujoco.mjtObj.mjOBJ_BODY, body_id)
        for body_id in range(1, model.nbody)
    )
    joint_names = tuple(
        _name(model, mujoco.mjtObj.mjOBJ_JOINT, joint_id)
        for joint_id in range(model.njnt)
    )
    root_body = str(robot.get("root_body") or "")
    if root_body not in body_names:
        raise RobotRuntimeDefinitionError(
            f"Root body not found in compiled model: {identity}, body={root_body}, "
            f"path={model_path}"
        )
    data = _initial_data(
        model, dict(robot.get("initial_pose") or {"type": "model_default"}),
        identity=identity,
    )
    retargeting = robot.get("retargeting") or {}
    if not isinstance(retargeting, dict):
        raise RobotRuntimeDefinitionError(
            f"Robot retargeting metadata must be an object: {identity}"
        )
    orientations = _orientation_definitions(
        model, data, retargeting, identity=identity
    )
    pelvis_reference = _pelvis_reference_definition(
        retargeting,
        set(body_names),
        root_body=root_body,
        identity=identity,
    )

    raw_output_order = robot.get("output_joint_order", "model_hinge_order")
    if raw_output_order == "model_hinge_order":
        output_joint_names = tuple(
            joint_names[joint_id]
            for joint_id in range(model.njnt)
            if int(model.jnt_type[joint_id]) == int(mujoco.mjtJoint.mjJNT_HINGE)
        )
    elif isinstance(raw_output_order, list) and raw_output_order:
        output_joint_names = tuple(str(name) for name in raw_output_order)
        missing = sorted(set(output_joint_names) - set(joint_names))
        if missing:
            raise RobotRuntimeDefinitionError(
                f"Output Joint not found in compiled model: {identity}, "
                f"joints={', '.join(missing)}"
            )
        if len(set(output_joint_names)) != len(output_joint_names):
            raise RobotRuntimeDefinitionError(
                f"Duplicate Output Joint: {identity}"
            )
    else:
        raise RobotRuntimeDefinitionError(f"Invalid output_joint_order: {identity}")

    expected_dof = robot.get("dof")
    if expected_dof is not None and int(expected_dof) != len(output_joint_names):
        raise RobotRuntimeDefinitionError(
            f"Variant DOF mismatch after MuJoCo compilation: {identity}, "
            f"manifest={expected_dof}, output_joints={len(output_joint_names)}, "
            f"path={model_path}"
        )
    foot_contacts = retargeting.get("foot_contacts")
    if foot_contacts is not None and not isinstance(foot_contacts, dict):
        raise RobotRuntimeDefinitionError(
            f"retargeting.foot_contacts must be an object: {identity}"
        )
    _validate_foot_contacts(foot_contacts, set(body_names), identity=identity)
    return RobotRuntimeDefinition(
        identity=identity,
        model_path=model_path,
        model_format=model_format,
        model=model,
        initial_qpos=np.asarray(data.qpos, dtype=np.float64).copy(),
        body_names=body_names,
        joint_names=joint_names,
        output_joint_names=output_joint_names,
        root_body=root_body,
        floating_base=bool(robot.get("floating_base", False)),
        pelvis_reference=pelvis_reference,
        orientations=orientations,
        foot_contacts=foot_contacts,
        retargeting=retargeting,
    )


def load_robot_runtime_definition_for_config(
    repository_root: Path,
    config: dict[str, Any],
    *,
    validate_config: bool = True,
) -> RobotRuntimeDefinition:
    """Resolve a Config's registered Robot before compiling its definition.

    Legacy Run Configs may contain only the old ``mjcf`` compatibility key.
    The Registry remains authoritative for fixed Robot semantics, so those
    snapshots receive the current backward-compatible manifest definition.
    """
    robot = config.get("robot")
    if not isinstance(robot, dict):
        raise RobotRuntimeDefinitionError("Config Robot identity is missing")
    try:
        from server.robot_registry import resolve_variant
    except ModuleNotFoundError:  # Direct execution from server/retarget.
        from robot_registry import resolve_variant
    requested_root = repository_root.resolve()
    registry_root = (
        requested_root
        if (requested_root / "server" / "robots" / "robots.json").is_file()
        else Path(__file__).resolve().parents[2]
    )
    record = resolve_variant(
        str(robot.get("variant") or ""),
        manufacturer_id=str(robot.get("manufacturer") or "") or None,
        robot_id=str(robot.get("model") or "") or None,
        root=registry_root,
    )
    runtime = load_robot_runtime_definition(
        registry_root, record.runtime_robot(registry_root)
    )
    if validate_config:
        runtime.validate_config(config)
    return runtime
