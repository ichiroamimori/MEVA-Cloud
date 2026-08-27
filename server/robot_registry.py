from __future__ import annotations

import json
import math
import re
import xml.etree.ElementTree as ET
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SUPPORTED_SCHEMA_VERSIONS = {"1.0"}
SAFE_ID_RE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.-]*$")


class RobotRegistryError(ValueError):
    pass


@dataclass(frozen=True)
class RobotVariant:
    manufacturer_id: str
    manufacturer_name: str
    robot_id: str
    robot_name: str
    manifest_relative_path: str
    manifest_path: Path
    robot_directory: Path
    robot_enabled: bool
    variant: dict[str, Any]

    @property
    def variant_id(self) -> str:
        return str(self.variant["id"])

    @property
    def enabled(self) -> bool:
        return self.robot_enabled and bool(self.variant["enabled"])

    @property
    def model_path(self) -> Path:
        return _child_path(
            self.robot_directory,
            str(self.variant["model"]["file"]),
            "model file",
        )

    def runtime_robot(self, repository_root: Path) -> dict[str, Any]:
        model = self.variant["model"]
        value: dict[str, Any] = {
            "manufacturer": self.manufacturer_id,
            "model": self.robot_id,
            "variant": self.variant_id,
            "model_format": str(model["format"]),
            "model_file": _repository_relative(self.model_path, repository_root),
            # Compatibility key used by the existing MuJoCo Retargeting code.
            "mjcf": _repository_relative(self.model_path, repository_root),
            "manifest": _repository_relative(self.manifest_path, repository_root),
            "initial_pose": deepcopy(
                self.variant.get("initial_pose", {"type": "model_default"})
            ),
            "root_body": str(self.variant.get("root_body") or ""),
            "floating_base": bool(self.variant.get("floating_base", False)),
            "output_joint_order": deepcopy(
                self.variant.get("output_joint_order", "model_hinge_order")
            ),
        }
        initial_pose = value["initial_pose"]
        if isinstance(initial_pose, dict) and initial_pose.get("type") == "keyframe":
            value["initial_keyframe"] = str(initial_pose["name"])
        retargeting = variant_retargeting_metadata(self)
        if "foot_contacts" in retargeting:
            value["foot_contacts"] = deepcopy(retargeting["foot_contacts"])
        return value

    def public_dict(self) -> dict[str, Any]:
        return {
            "id": self.variant_id,
            "name": str(self.variant["name"]),
            "short_name": str(self.variant.get("short_name") or self.variant["name"]),
            "dof": int(self.variant["dof"]),
            "enabled": bool(self.variant["enabled"]),
            "model": deepcopy(self.variant["model"]),
            "source": deepcopy(self.variant.get("source", {})),
            "initial_pose": deepcopy(
                self.variant.get("initial_pose", {"type": "model_default"})
            ),
            "root_body": str(self.variant.get("root_body") or ""),
            "floating_base": bool(self.variant.get("floating_base", False)),
            "output_joint_order": deepcopy(
                self.variant.get("output_joint_order", "model_hinge_order")
            ),
            "retargeting": deepcopy(self.variant.get("retargeting", {})),
        }


def repository_root() -> Path:
    return Path(__file__).resolve().parents[1]


def robots_root(root: Path | None = None) -> Path:
    base = (root or repository_root()).resolve()
    return base / "server" / "robots"


def _read_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RobotRegistryError(f"{label} not found: {path}") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise RobotRegistryError(f"Could not read {label}: {path}") from exc
    if not isinstance(value, dict):
        raise RobotRegistryError(f"{label} must be a JSON object: {path}")
    version = str(value.get("schema_version") or "")
    if version not in SUPPORTED_SCHEMA_VERSIONS:
        raise RobotRegistryError(
            f"Unsupported {label} schema_version {version!r}: {path}"
        )
    return value


def _required_id(value: Any, label: str) -> str:
    result = str(value or "").strip()
    if not SAFE_ID_RE.fullmatch(result) or result in {".", ".."}:
        raise RobotRegistryError(f"Invalid {label}: {result!r}")
    return result


def _required_name(value: Any, label: str) -> str:
    result = str(value or "").strip()
    if not result or len(result) > 200 or any(ord(char) < 32 for char in result):
        raise RobotRegistryError(f"Invalid {label}")
    return result


def _required_bool(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise RobotRegistryError(f"{label} must be boolean")
    return value


def _child_path(directory: Path, relative: str, label: str) -> Path:
    raw = Path(relative.replace("\\", "/"))
    if raw.is_absolute() or ".." in raw.parts:
        raise RobotRegistryError(f"Unsafe {label}: {relative}")
    base = directory.resolve()
    result = (base / raw).resolve()
    if result != base and base not in result.parents:
        raise RobotRegistryError(f"Unsafe {label}: {relative}")
    return result


def _repository_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise RobotRegistryError(f"Robot asset is outside the repository: {path}") from exc


def _validate_manifest(
    manifest: dict[str, Any],
    *,
    manifest_path: Path,
    catalog_entry: dict[str, Any],
) -> list[dict[str, Any]]:
    manufacturer = manifest.get("manufacturer")
    robot = manifest.get("robot")
    if not isinstance(manufacturer, dict) or not isinstance(robot, dict):
        raise RobotRegistryError(
            f"manifest manufacturer/robot must be objects: {manifest_path}"
        )
    manufacturer_id = _required_id(manufacturer.get("id"), "manifest manufacturer id")
    robot_id = _required_id(robot.get("id"), "manifest robot id")
    expected_manufacturer = str(catalog_entry["manufacturer_id"])
    expected_robot = str(catalog_entry["robot_id"])
    if manufacturer_id != expected_manufacturer or robot_id != expected_robot:
        raise RobotRegistryError(
            "Robot manifest identity mismatch: "
            f"expected {expected_manufacturer}/{expected_robot}, "
            f"found {manufacturer_id}/{robot_id}, manifest={manifest_path}"
        )

    raw_variants = manifest.get("variants")
    if not isinstance(raw_variants, list) or not raw_variants:
        raise RobotRegistryError(f"manifest variants must be a non-empty array: {manifest_path}")
    variants: list[dict[str, Any]] = []
    ids: set[str] = set()
    for raw in raw_variants:
        if not isinstance(raw, dict):
            raise RobotRegistryError(f"Variant must be an object: {manifest_path}")
        variant = deepcopy(raw)
        variant_id = _required_id(variant.get("id"), "Variant ID")
        if variant_id in ids:
            raise RobotRegistryError(
                f"Duplicate Variant ID {variant_id!r}: {manifest_path}"
            )
        ids.add(variant_id)
        variant["name"] = _required_name(variant.get("name"), "Variant name")
        dof = variant.get("dof")
        if isinstance(dof, bool) or not isinstance(dof, int) or dof <= 0:
            raise RobotRegistryError(
                f"Variant DOF must be a positive integer: "
                f"{manufacturer_id}/{robot_id}/{variant_id}"
            )
        variant["enabled"] = _required_bool(
            variant.get("enabled"),
            f"Variant enabled ({manufacturer_id}/{robot_id}/{variant_id})",
        )
        model = variant.get("model")
        if not isinstance(model, dict):
            raise RobotRegistryError(
                f"Variant model must be an object: {manufacturer_id}/{robot_id}/{variant_id}"
            )
        model_format = str(model.get("format") or "").lower()
        if model_format not in {"mjcf", "urdf"}:
            raise RobotRegistryError(
                f"Unsupported model format {model_format!r}: "
                f"{manufacturer_id}/{robot_id}/{variant_id}"
            )
        model["format"] = model_format
        model_file = str(model.get("file") or "")
        model_path = _child_path(manifest_path.parent, model_file, "model file")
        if not model_path.is_file():
            raise RobotRegistryError(
                "Robot model file not found: "
                f"manufacturer={manufacturer_id}, robot={robot_id}, "
                f"variant={variant_id}, expected={model_path}"
            )
        source = variant.get("source", {})
        if source is not None and not isinstance(source, dict):
            raise RobotRegistryError(
                f"Variant source must be an object: {manufacturer_id}/{robot_id}/{variant_id}"
            )
        source = source or {}
        if source.get("urdf"):
            urdf_path = _child_path(manifest_path.parent, str(source["urdf"]), "source URDF")
            if not urdf_path.is_file():
                raise RobotRegistryError(
                    "Robot source URDF not found: "
                    f"manufacturer={manufacturer_id}, robot={robot_id}, "
                    f"variant={variant_id}, expected={urdf_path}"
                )
        initial_pose = variant.get("initial_pose", {"type": "model_default"})
        if not isinstance(initial_pose, dict) or initial_pose.get("type") not in {
            "model_default", "keyframe"
        }:
            raise RobotRegistryError(
                f"Invalid initial_pose: {manufacturer_id}/{robot_id}/{variant_id}"
            )
        if initial_pose.get("type") == "keyframe" and not str(initial_pose.get("name") or ""):
            raise RobotRegistryError(
                f"initial_pose keyframe name is required: "
                f"{manufacturer_id}/{robot_id}/{variant_id}"
            )
        root_body = _required_id(variant.get("root_body"), "Variant root_body")
        floating_base = _required_bool(
            variant.get("floating_base"),
            f"Variant floating_base ({manufacturer_id}/{robot_id}/{variant_id})",
        )
        output_joint_order = variant.get("output_joint_order", "model_hinge_order")
        if output_joint_order != "model_hinge_order" and not (
            isinstance(output_joint_order, list)
            and output_joint_order
            and all(isinstance(name, str) and name for name in output_joint_order)
        ):
            raise RobotRegistryError(
                f"Invalid output_joint_order: {manufacturer_id}/{robot_id}/{variant_id}"
            )
        variant["model"] = model
        variant["source"] = source
        variant["initial_pose"] = initial_pose
        variant["root_body"] = root_body
        variant["floating_base"] = floating_base
        variant["output_joint_order"] = output_joint_order
        variants.append(variant)
    return variants


def load_registry(root: Path | None = None) -> list[RobotVariant]:
    repository = (root or repository_root()).resolve()
    directory = robots_root(repository)
    catalog_path = directory / "robots.json"
    catalog = _read_object(catalog_path, "robots.json")
    raw_robots = catalog.get("robots")
    if not isinstance(raw_robots, list):
        raise RobotRegistryError(f"robots must be an array: {catalog_path}")

    robot_keys: set[tuple[str, str]] = set()
    variant_ids: dict[str, str] = {}
    records: list[RobotVariant] = []
    for raw in raw_robots:
        if not isinstance(raw, dict):
            raise RobotRegistryError(f"Robot entry must be an object: {catalog_path}")
        manufacturer_id = _required_id(raw.get("manufacturer_id"), "manufacturer_id")
        robot_id = _required_id(raw.get("robot_id"), "robot_id")
        key = (manufacturer_id, robot_id)
        if key in robot_keys:
            raise RobotRegistryError(
                f"Duplicate Robot identity {manufacturer_id}/{robot_id}: {catalog_path}"
            )
        robot_keys.add(key)
        manufacturer_name = _required_name(
            raw.get("manufacturer_name"), "manufacturer_name"
        )
        robot_name = _required_name(raw.get("robot_name"), "robot_name")
        enabled = _required_bool(
            raw.get("enabled"), f"Robot enabled ({manufacturer_id}/{robot_id})"
        )
        manifest_relative = str(raw.get("manifest") or "")
        manifest_path = _child_path(directory, manifest_relative, "manifest path")
        manifest = _read_object(manifest_path, "manifest.json")
        variants = _validate_manifest(
            manifest, manifest_path=manifest_path, catalog_entry={
                "manufacturer_id": manufacturer_id, "robot_id": robot_id,
            }
        )
        for variant in variants:
            variant_id = str(variant["id"])
            owner = f"{manufacturer_id}/{robot_id}"
            if variant_id in variant_ids:
                raise RobotRegistryError(
                    f"Duplicate global Variant ID {variant_id!r}: "
                    f"{variant_ids[variant_id]} and {owner}"
                )
            variant_ids[variant_id] = owner
            records.append(RobotVariant(
                manufacturer_id=manufacturer_id,
                manufacturer_name=manufacturer_name,
                robot_id=robot_id,
                robot_name=robot_name,
                manifest_relative_path=manifest_relative.replace("\\", "/"),
                manifest_path=manifest_path,
                robot_directory=manifest_path.parent,
                robot_enabled=enabled,
                variant=variant,
            ))
    return records


def resolve_variant(
    variant_id: str,
    *,
    manufacturer_id: str | None = None,
    robot_id: str | None = None,
    root: Path | None = None,
    require_enabled: bool = True,
) -> RobotVariant:
    variant_id = _required_id(variant_id, "variant_id")
    records = [item for item in load_registry(root) if item.variant_id == variant_id]
    if manufacturer_id is not None:
        records = [item for item in records if item.manufacturer_id == manufacturer_id]
    if robot_id is not None:
        records = [item for item in records if item.robot_id == robot_id]
    if not records:
        identity = "/".join(x for x in (manufacturer_id, robot_id, variant_id) if x)
        raise RobotRegistryError(f"Robot Variant is not registered: {identity}")
    record = records[0]
    if require_enabled and not record.enabled:
        raise RobotRegistryError(
            f"Robot Variant is disabled: "
            f"{record.manufacturer_id}/{record.robot_id}/{record.variant_id}"
        )
    return record


def public_catalog(root: Path | None = None) -> dict[str, Any]:
    records = load_registry(root)
    grouped: dict[tuple[str, str], dict[str, Any]] = {}
    for item in records:
        key = (item.manufacturer_id, item.robot_id)
        group = grouped.setdefault(key, {
            "manufacturer_id": item.manufacturer_id,
            "manufacturer_name": item.manufacturer_name,
            "robot_id": item.robot_id,
            "robot_name": item.robot_name,
            "manifest": item.manifest_relative_path,
            "enabled": item.robot_enabled,
            "variants": [],
        })
        group["variants"].append(item.public_dict())
    return {
        "schema_version": "1.0",
        "robots": list(grouped.values()),
    }


def apply_variant_to_runtime_config(
    config: dict[str, Any], record: RobotVariant, *, root: Path | None = None
) -> dict[str, Any]:
    repository = (root or repository_root()).resolve()
    result = deepcopy(config)
    result["robot"] = record.runtime_robot(repository)
    return result


def variant_retargeting_metadata(record: RobotVariant) -> dict[str, Any]:
    value = record.variant.get("retargeting", {})
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise RobotRegistryError(
            f"retargeting metadata must be an object: "
            f"{record.manufacturer_id}/{record.robot_id}/{record.variant_id}"
        )
    return deepcopy(value)


def validate_retarget_config(
    record: RobotVariant, config: dict[str, Any]
) -> dict[str, Any]:
    identity = f"{record.manufacturer_id}/{record.robot_id}/{record.variant_id}"
    robot = config.get("robot")
    if not isinstance(robot, dict):
        raise RobotRegistryError(f"Config robot identity is missing: {identity}")
    actual = (
        str(robot.get("manufacturer") or ""),
        str(robot.get("model") or ""),
        str(robot.get("variant") or ""),
    )
    expected = (record.manufacturer_id, record.robot_id, record.variant_id)
    if actual != expected:
        raise RobotRegistryError(
            f"Config Robot identity mismatch: expected {'/'.join(expected)}, "
            f"found {'/'.join(actual)}"
        )
    if str(record.variant["model"]["format"]) != "mjcf":
        raise RobotRegistryError(
            f"Retargeting Runtime Model must be MJCF: {identity}, "
            f"model={record.model_path}"
        )
    try:
        xml = ET.parse(record.model_path).getroot()
    except (OSError, ET.ParseError) as exc:
        raise RobotRegistryError(
            f"Could not parse Runtime Model: {identity}, path={record.model_path}"
        ) from exc

    bodies = {
        str(node.get("name")) for node in xml.findall(".//body") if node.get("name")
    }
    joints = {
        str(node.get("name")) for node in xml.findall(".//joint") if node.get("name")
    }
    actuator_joints = {
        str(node.get("joint"))
        for node in xml.findall(".//actuator/*")
        if node.get("joint")
    }
    root_body = str(record.variant.get("root_body") or "")
    if root_body not in bodies:
        raise RobotRegistryError(
            f"Root body not found in model: {identity}, body={root_body}, "
            f"path={record.model_path}"
        )
    initial_pose = record.variant.get("initial_pose", {})
    if isinstance(initial_pose, dict) and initial_pose.get("type") == "keyframe":
        keyframe_name = str(initial_pose.get("name") or "")
        keyframes = {
            str(node.get("name")) for node in xml.findall(".//keyframe/key")
            if node.get("name")
        }
        if keyframe_name not in keyframes:
            raise RobotRegistryError(
                f"Initial keyframe not found in model: {identity}, "
                f"keyframe={keyframe_name}, path={record.model_path}"
            )
    output_joint_order = record.variant.get("output_joint_order")
    if isinstance(output_joint_order, list):
        missing_output_joints = sorted(set(output_joint_order) - joints)
        if missing_output_joints:
            raise RobotRegistryError(
                f"Output Joint not found in model: {identity}, "
                f"joints={', '.join(missing_output_joints)}, path={record.model_path}"
            )
    if actuator_joints and len(actuator_joints) != int(record.variant["dof"]):
        raise RobotRegistryError(
            f"Variant DOF mismatch: manufacturer={record.manufacturer_id}, "
            f"robot={record.robot_id}, variant={record.variant_id}, "
            f"manifest={record.variant['dof']}, model_actuators={len(actuator_joints)}, "
            f"path={record.model_path}"
        )

    mappings = config.get("mappings")
    if not isinstance(mappings, list):
        raise RobotRegistryError(f"Config mappings must be an array: {identity}")
    missing_links = sorted({
        str(item.get("target_link"))
        for item in mappings
        if isinstance(item, dict)
        and item.get("target_link")
        and str(item["target_link"]) not in bodies
    })
    if missing_links:
        raise RobotRegistryError(
            f"Config target_link not found in model: {identity}, "
            f"links={', '.join(missing_links)}, path={record.model_path}"
        )

    missing_joints: set[str] = set()
    for section in (
        "joint_limit_avoidance",
        "interframe_joint_velocity_limit",
        "interframe_joint_acceleration_limit",
    ):
        settings = config.get(section)
        overrides = settings.get("overrides") if isinstance(settings, dict) else None
        if isinstance(overrides, dict):
            missing_joints.update(str(name) for name in overrides if str(name) not in joints)
    if missing_joints:
        raise RobotRegistryError(
            f"Config Joint override not found in model: {identity}, "
            f"joints={', '.join(sorted(missing_joints))}, path={record.model_path}"
        )

    metadata = variant_retargeting_metadata(record)
    foot_contacts = metadata.get("foot_contacts", {})
    if isinstance(foot_contacts, dict):
        offset = foot_contacts.get("robot_foot_to_ground_offset_m")
        if (
            isinstance(offset, bool)
            or not isinstance(offset, (int, float))
            or not math.isfinite(float(offset))
            or float(offset) < 0.0
        ):
            raise RobotRegistryError(
                f"Invalid robot Foot-to-ground offset: {identity}"
            )
        for side, definition in foot_contacts.items():
            if side == "robot_foot_to_ground_offset_m":
                continue
            if not isinstance(definition, dict):
                raise RobotRegistryError(f"Invalid {side} foot contact definition: {identity}")
            if side not in {"left", "right"}:
                raise RobotRegistryError(
                    f"Unknown Foot contact side {side!r}: {identity}"
                )
            body_name = str(definition.get("body") or "")
            if body_name not in bodies:
                raise RobotRegistryError(
                    f"Foot body not found in model: {identity}, side={side}, "
                    f"body={body_name}, path={record.model_path}"
                )
            points = definition.get("support_points")
            if not isinstance(points, list) or len(points) != 4:
                raise RobotRegistryError(
                    f"Foot contact requires four support points: {identity}, side={side}"
                )
            point_names: set[str] = set()
            for point in points:
                if not isinstance(point, dict):
                    raise RobotRegistryError(
                        f"Invalid Foot support point: {identity}, side={side}"
                    )
                point_name = _required_id(point.get("name"), "Foot support point name")
                if point_name in point_names:
                    raise RobotRegistryError(
                        f"Duplicate Foot support point {point_name!r}: {identity}, side={side}"
                    )
                point_names.add(point_name)
                position = point.get("local_position")
                if not (
                    isinstance(position, list)
                    and len(position) == 3
                    and all(
                        not isinstance(value, bool)
                        and isinstance(value, (int, float))
                        and math.isfinite(float(value))
                        for value in position
                    )
                ):
                    raise RobotRegistryError(
                        f"Invalid Foot support point position: {identity}, "
                        f"side={side}, point={point_name}"
                    )
        if set(foot_contacts) - {"robot_foot_to_ground_offset_m"} != {"left", "right"}:
            raise RobotRegistryError(
                f"Foot contacts must define left and right sides: {identity}"
            )
    return {
        "manufacturer_id": record.manufacturer_id,
        "robot_id": record.robot_id,
        "variant_id": record.variant_id,
        "model_path": str(record.model_path),
        "dof": int(record.variant["dof"]),
        "body_count": len(bodies),
        "joint_count": len(joints),
        "mapping_count": len(mappings),
    }
