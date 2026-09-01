from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

from server.robot_registry import (
    RobotRegistryError,
    RobotVariant,
    apply_variant_to_runtime_config,
    public_catalog,
    resolve_variant,
    validate_retarget_config,
    variant_retargeting_metadata,
)


router = APIRouter()


def repo_root() -> Path:
    # server/api/retarget_api.py -> repo root
    return Path(__file__).resolve().parents[2]

def _registered_variant(
    robot_variant: str,
    *,
    manufacturer: str | None = None,
    robot_id: str | None = None,
) -> RobotVariant:
    try:
        return resolve_variant(
            robot_variant,
            manufacturer_id=manufacturer,
            robot_id=robot_id,
            root=repo_root(),
        )
    except RobotRegistryError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

def _runtime_robot_config(config: dict[str, Any], record: RobotVariant) -> dict[str, Any]:
    return apply_variant_to_runtime_config(config, record, root=repo_root())

def _assert_config_robot(config: dict[str, Any], record: RobotVariant) -> None:
    robot = config.get("robot")
    if not isinstance(robot, dict):
        raise HTTPException(status_code=400, detail="Config robot identity is required")
    actual = (
        str(robot.get("manufacturer") or ""),
        str(robot.get("model") or ""),
        str(robot.get("variant") or ""),
    )
    expected = (record.manufacturer_id, record.robot_id, record.variant_id)
    if actual != expected:
        raise HTTPException(
            status_code=400,
            detail=(
                "Config Robot identity mismatch: "
                f"expected {expected[0]}/{expected[1]}/{expected[2]}, "
                f"found {actual[0]}/{actual[1]}/{actual[2]}"
            ),
        )

def _validate_retarget_config_or_http(
    record: RobotVariant, config: dict[str, Any]
) -> dict[str, Any]:
    try:
        return validate_retarget_config(record, config)
    except RobotRegistryError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

def _sole_geom_descriptors(config: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Expose the manifest-defined Foot support points to the existing UI."""
    robot = config.get("robot", {})
    contacts = robot.get("foot_contacts") if isinstance(robot, dict) else None
    if not isinstance(contacts, dict):
        contacts = None
    if contacts is None:
        try:
            variant = resolve_variant(
                str(robot.get("variant") or ""),
                manufacturer_id=str(robot.get("manufacturer") or "") or None,
                robot_id=str(robot.get("model") or "") or None,
                root=repo_root(),
            )
            value = variant_retargeting_metadata(variant).get("foot_contacts")
            contacts = value if isinstance(value, dict) else None
        except RobotRegistryError:
            contacts = None
    result: dict[str, list[dict[str, Any]]] = {"left": [], "right": []}
    if contacts is None:
        return result
    for side in ("left", "right"):
        definition = contacts.get(side)
        if not isinstance(definition, dict):
            continue
        points = definition.get("support_points")
        if not isinstance(points, list):
            continue
        for index, point in enumerate(points):
            if not isinstance(point, dict):
                continue
            position = point.get("local_position")
            if not isinstance(position, list) or len(position) != 3:
                continue
            name = str(point.get("name") or f"support_{index + 1}")
            result[side].append({
                "index": index,
                "name": name,
                "display": f"{side}_{name}",
                "pos": " ".join(f"{float(value):g}" for value in position),
                "size": "",
                "body": str(definition.get("body") or ""),
                "source_geom": str(definition.get("source_geom") or ""),
                "generation_method": str(
                    definition.get("generation_method") or "explicit"
                ),
            })
    return result

def _manifest_robot_foot_to_ground_offset(config: dict[str, Any]) -> float | None:
    """Read the installer-confirmed Robot Foot offset from manifest metadata."""
    robot = config.get("robot", {})
    contacts = robot.get("foot_contacts") if isinstance(robot, dict) else None
    if not isinstance(contacts, dict):
        try:
            variant = resolve_variant(
                str(robot.get("variant") or ""),
                manufacturer_id=str(robot.get("manufacturer") or "") or None,
                robot_id=str(robot.get("model") or "") or None,
                root=repo_root(),
            )
            value = variant_retargeting_metadata(variant).get("foot_contacts")
            contacts = value if isinstance(value, dict) else None
        except RobotRegistryError:
            contacts = None
    if not isinstance(contacts, dict):
        return None
    try:
        value = float(contacts["robot_foot_to_ground_offset_m"])
    except (KeyError, TypeError, ValueError):
        return None
    return value if math.isfinite(value) and value >= 0.0 else None

@router.get("/robots")
def get_robot_catalog():
    try:
        return public_catalog(repo_root())
    except RobotRegistryError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
