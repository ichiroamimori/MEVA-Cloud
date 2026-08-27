"""Robot-independent Foot support point definitions and kinematics."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Any

import mujoco
import numpy as np

try:
    from server.robot_registry import (
        RobotRegistryError,
        resolve_variant,
        variant_retargeting_metadata,
    )
except ImportError:  # pragma: no cover - direct script execution
    application_root = Path(__file__).resolve().parents[2]
    if str(application_root) not in sys.path:
        sys.path.insert(0, str(application_root))
    from server.robot_registry import (  # type: ignore
        RobotRegistryError,
        resolve_variant,
        variant_retargeting_metadata,
    )


SIDES = ("left", "right")


@dataclass(frozen=True)
class FootSupportSide:
    side: str
    body_name: str
    body_id: int
    names: tuple[str, ...]
    local_positions: np.ndarray
    generation_method: str
    source_geom: str | None

    @property
    def display_names(self) -> list[str]:
        return [f"{self.side}_{name}" for name in self.names]


@dataclass(frozen=True)
class FootSupportDefinition:
    robot_foot_to_ground_offset_m: float
    sides: dict[str, FootSupportSide]


def _manifest_contacts(config: dict[str, Any]) -> dict[str, Any]:
    robot = config.get("robot", {})
    contacts = robot.get("foot_contacts") if isinstance(robot, dict) else None
    if isinstance(contacts, dict):
        return contacts
    try:
        record = resolve_variant(
            str(robot.get("variant") or ""),
            manufacturer_id=str(robot.get("manufacturer") or "") or None,
            robot_id=str(robot.get("model") or "") or None,
        )
    except RobotRegistryError as exc:
        raise ValueError(f"Robot Foot contact metadata is unavailable: {exc}") from exc
    contacts = variant_retargeting_metadata(record).get("foot_contacts")
    if not isinstance(contacts, dict):
        raise ValueError(
            f"Robot Variant {record.variant_id} has no Foot contact metadata"
        )
    return contacts


def load_foot_support_definition(
    model: mujoco.MjModel,
    config: dict[str, Any],
) -> FootSupportDefinition:
    contacts = _manifest_contacts(config)
    try:
        offset = float(contacts["robot_foot_to_ground_offset_m"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Robot Foot-to-ground offset is unavailable") from exc
    if not np.isfinite(offset) or offset < 0.0:
        raise ValueError("Robot Foot-to-ground offset must be finite and non-negative")

    sides: dict[str, FootSupportSide] = {}
    for side in SIDES:
        raw = contacts.get(side)
        if not isinstance(raw, dict):
            raise ValueError(f"Robot Foot contact metadata is missing {side}")
        body_name = str(raw.get("body") or "")
        body_id = int(mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, body_name))
        if body_id < 0:
            raise ValueError(f"Robot Foot body not found: side={side}, body={body_name}")
        points = raw.get("support_points")
        if not isinstance(points, list) or len(points) != 4:
            raise ValueError(f"Robot {side} Foot must define four support points")
        names = tuple(str(point.get("name") or "") for point in points)
        local = np.asarray(
            [point.get("local_position") for point in points], dtype=np.float64
        )
        if len(set(names)) != 4 or any(not name for name in names):
            raise ValueError(f"Robot {side} Foot support point names must be unique")
        if local.shape != (4, 3) or not np.all(np.isfinite(local)):
            raise ValueError(f"Robot {side} Foot support points must be finite (4, 3)")
        sides[side] = FootSupportSide(
            side=side,
            body_name=body_name,
            body_id=body_id,
            names=names,
            local_positions=local,
            generation_method=str(raw.get("generation_method") or "explicit"),
            source_geom=(str(raw["source_geom"]) if raw.get("source_geom") else None),
        )
    return FootSupportDefinition(offset, sides)


def support_point_world_positions(
    data: mujoco.MjData,
    definition: FootSupportSide,
) -> np.ndarray:
    rotation = np.asarray(data.xmat[definition.body_id], dtype=np.float64).reshape(3, 3)
    origin = np.asarray(data.xpos[definition.body_id], dtype=np.float64)
    return origin[None, :] + definition.local_positions @ rotation.T


def support_point_world_position(
    data: mujoco.MjData,
    definition: FootSupportSide,
    point_index: int,
) -> np.ndarray:
    rotation = np.asarray(data.xmat[definition.body_id], dtype=np.float64).reshape(3, 3)
    return (
        np.asarray(data.xpos[definition.body_id], dtype=np.float64)
        + rotation @ definition.local_positions[int(point_index)]
    )


def support_point_jacobian(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    definition: FootSupportSide,
    point_index: int,
) -> np.ndarray:
    jacobian = np.zeros((3, model.nv), dtype=np.float64)
    rotational = np.zeros((3, model.nv), dtype=np.float64)
    point = support_point_world_position(data, definition, point_index)
    mujoco.mj_jac(
        model,
        data,
        jacobian,
        rotational,
        point,
        definition.body_id,
    )
    return jacobian


def support_point_metadata(definition: FootSupportDefinition) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for side in SIDES:
        item = definition.sides[side]
        for index, name in enumerate(item.names):
            result.append({
                "name": f"{side}_{name}",
                "side": side,
                "body": item.body_name,
                "local_position_m": item.local_positions[index].tolist(),
                "generation_method": item.generation_method,
                "source_geom": item.source_geom,
            })
    return result
