# -*- coding: utf-8 -*-
"""Robot-model-derived metadata shared by Retargeting settings and validation."""
from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import mujoco


def object_name(model, kind, index: int, fallback: str) -> str:
    return mujoco.mj_id2name(model, kind, index) or fallback


def joint_descriptors(model: mujoco.MjModel) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for jid in range(model.njnt):
        jtype = int(model.jnt_type[jid])
        name = object_name(model, mujoco.mjtObj.mjOBJ_JOINT, jid, f"joint_{jid}")
        dof_count = {
            int(mujoco.mjtJoint.mjJNT_FREE): 6,
            int(mujoco.mjtJoint.mjJNT_BALL): 3,
            int(mujoco.mjtJoint.mjJNT_SLIDE): 1,
            int(mujoco.mjtJoint.mjJNT_HINGE): 1,
        }.get(jtype, 0)
        type_name = {
            int(mujoco.mjtJoint.mjJNT_FREE): "free",
            int(mujoco.mjtJoint.mjJNT_BALL): "ball",
            int(mujoco.mjtJoint.mjJNT_SLIDE): "slide",
            int(mujoco.mjtJoint.mjJNT_HINGE): "revolute",
        }.get(jtype, "unknown")
        rows.append({
            "id": jid,
            "name": name,
            "body": object_name(
                model, mujoco.mjtObj.mjOBJ_BODY, int(model.jnt_bodyid[jid]),
                f"body_{int(model.jnt_bodyid[jid])}",
            ),
            "dof_count": dof_count,
            "type_name": type_name,
            "axis": [float(x) for x in model.jnt_axis[jid]],
            "controllable": type_name != "free" and dof_count > 0,
            "qpos_address": int(model.jnt_qposadr[jid]),
            "dof_address": int(model.jnt_dofadr[jid]),
            "limited": bool(model.jnt_limited[jid]),
            "range": [float(x) for x in model.jnt_range[jid]],
            "type": jtype,
        })
    return rows


def body_descriptors(
    model: mujoco.MjModel, joints: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    joints_by_body: dict[int, list[int]] = {}
    for joint in joints:
        joints_by_body.setdefault(int(model.jnt_bodyid[int(joint["id"])]), []).append(
            int(joint["id"])
        )
    depths = [0] * model.nbody
    for body_id in range(1, model.nbody):
        parent_id = int(model.body_parentid[body_id])
        depths[body_id] = depths[parent_id] + 1
    rows: list[dict[str, Any]] = []
    for body_id in range(1, model.nbody):
        parent_id = int(model.body_parentid[body_id])
        rows.append({
            "id": body_id,
            "name": object_name(
                model, mujoco.mjtObj.mjOBJ_BODY, body_id, f"body_{body_id}"
            ),
            "parent_id": parent_id,
            "parent_name": (
                object_name(
                    model, mujoco.mjtObj.mjOBJ_BODY, parent_id, f"body_{parent_id}"
                ) if parent_id else "world"
            ),
            "depth": depths[body_id] - 1,
            "joint_ids": joints_by_body.get(body_id, []),
        })
    return rows


def _pair_map(
    raw_pairs: Any, available: set[str], *, label: str
) -> dict[str, str]:
    result: dict[str, str] = {}
    if raw_pairs is None:
        return result
    if not isinstance(raw_pairs, list):
        raise ValueError(f"Robot UI {label} must be an array")
    for raw in raw_pairs:
        if not isinstance(raw, list) or len(raw) != 2:
            raise ValueError(f"Robot UI {label} entries must contain two names")
        left, right = (str(raw[0]), str(raw[1]))
        if left not in available or right not in available:
            raise ValueError(
                f"Robot UI {label} references an unknown name: {left}, {right}"
            )
        if left == right or left in result or right in result:
            raise ValueError(f"Robot UI {label} contains a duplicate pair")
        result[left] = right
        result[right] = left
    return result


def ui_metadata(
    model: mujoco.MjModel,
    bodies: list[dict[str, Any]],
    joints: list[dict[str, Any]],
    raw_ui: dict[str, Any] | None,
) -> dict[str, Any]:
    """Validate optional manifest presentation metadata against the Runtime Model."""
    raw_ui = raw_ui or {}
    if not isinstance(raw_ui, dict):
        raise ValueError("Robot UI metadata must be an object")
    body_by_name = {str(body["name"]): body for body in bodies}
    children: dict[str, list[str]] = {}
    for body in bodies:
        children.setdefault(str(body["parent_name"]), []).append(str(body["name"]))

    def subtree(root_name: str) -> list[str]:
        if root_name not in body_by_name:
            raise ValueError(f"Robot UI group root_body not found: {root_name}")
        result: list[str] = []
        stack = [root_name]
        while stack:
            current = stack.pop()
            result.append(current)
            stack.extend(reversed(children.get(current, [])))
        return result

    groups: list[dict[str, Any]] = []
    assigned: set[str] = set()
    raw_groups = raw_ui.get("groups", [])
    if not isinstance(raw_groups, list):
        raise ValueError("Robot UI groups must be an array")
    group_ids: set[str] = set()
    for index, raw in enumerate(raw_groups):
        if not isinstance(raw, dict):
            raise ValueError("Robot UI group must be an object")
        group_id = str(raw.get("id") or f"group_{index + 1}")
        if group_id in group_ids:
            raise ValueError(f"Duplicate Robot UI group id: {group_id}")
        group_ids.add(group_id)
        if "bodies" in raw:
            if not isinstance(raw["bodies"], list) or not raw["bodies"]:
                raise ValueError(f"Robot UI group bodies must be non-empty: {group_id}")
            names = [str(name) for name in raw["bodies"]]
            missing = [name for name in names if name not in body_by_name]
            if missing:
                raise ValueError(
                    f"Robot UI group {group_id} references unknown bodies: {missing}"
                )
        else:
            names = subtree(str(raw.get("root_body") or ""))
        duplicate = assigned.intersection(names)
        if duplicate:
            raise ValueError(
                f"Robot UI body belongs to multiple groups: {sorted(duplicate)}"
            )
        assigned.update(names)
        groups.append({
            "id": group_id,
            "name": str(raw.get("name") or group_id),
            "body_names": names,
            "collapsed": bool(raw.get("collapsed", False)),
        })
    if not raw_groups:
        roots = [body for body in bodies if int(body["parent_id"]) == 0]
        for root in roots:
            names = subtree(str(root["name"]))
            groups.append({
                "id": str(root["name"]), "name": str(root["name"]),
                "body_names": names, "collapsed": False,
            })
            group_ids.add(str(root["name"]))
            assigned.update(names)
    else:
        unassigned = [
            str(body["name"]) for body in bodies if body["name"] not in assigned
        ]
        if unassigned:
            groups.append({
                "id": "other", "name": "OTHER", "body_names": unassigned,
                "collapsed": False,
            })
            group_ids.add("other")

    symmetry = raw_ui.get("symmetry", {})
    if symmetry is not None and not isinstance(symmetry, dict):
        raise ValueError("Robot UI symmetry must be an object")
    symmetry = symmetry or {}
    explicit_body = _pair_map(
        symmetry.get("body_pairs"), set(body_by_name), label="body_pairs"
    )
    explicit_joint = _pair_map(
        symmetry.get("joint_pairs"), {str(joint["name"]) for joint in joints},
        label="joint_pairs",
    )
    group_pairs = _pair_map(
        symmetry.get("group_pairs"), group_ids, label="group_pairs"
    )
    inferred_body = symmetry_map(list(body_by_name))
    inferred_joint = symmetry_map([str(joint["name"]) for joint in joints])
    inferred_body.update(explicit_body)
    inferred_joint.update(explicit_joint)
    for group in groups:
        partner = group_pairs.get(str(group["id"]))
        if partner:
            group["symmetry_partner"] = partner
            raw_pair = next(
                pair for pair in symmetry.get("group_pairs", [])
                if str(group["id"]) in (str(pair[0]), str(pair[1]))
            )
            group["symmetry_primary"] = str(raw_pair[0]) == str(group["id"])
    return {
        "groups": groups,
        "body_symmetry": inferred_body,
        "joint_symmetry": inferred_joint,
    }


def _counterpart(name: str) -> str | None:
    """Infer a model-provided left/right counterpart without robot-specific names."""
    replacements = (
        ("Left", "Right"), ("Right", "Left"),
        ("left", "right"), ("right", "left"),
        ("LEFT", "RIGHT"), ("RIGHT", "LEFT"),
        ("_l_", "_r_"), ("_r_", "_l_"),
        ("_L_", "_R_"), ("_R_", "_L_"),
    )
    for source, target in replacements:
        if source in name:
            return name.replace(source, target, 1)
    return None


def symmetry_map(names: list[str]) -> dict[str, str]:
    available = set(names)
    return {
        name: other for name in names
        if (other := _counterpart(name)) is not None and other in available
    }


def _xml_excluded_body_pairs(xml_path: Path, model: mujoco.MjModel) -> set[tuple[int, int]]:
    excluded: set[tuple[int, int]] = set()
    # Compiled signatures also cover excludes originating from included MJCFs.
    compiled = {int(x) for x in getattr(model, "exclude_signature", [])}
    for body1 in range(model.nbody):
        for body2 in range(body1 + 1, model.nbody):
            if ((body1 << 16) + body2) in compiled or ((body2 << 16) + body1) in compiled:
                excluded.add((body1, body2))
    try:
        root = ET.parse(xml_path).getroot()
    except (OSError, ET.ParseError):
        return excluded
    for node in root.findall(".//contact/exclude"):
        body1, body2 = node.get("body1"), node.get("body2")
        if not body1 or not body2:
            continue
        id1 = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, body1)
        id2 = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, body2)
        if id1 >= 0 and id2 >= 0:
            excluded.add(tuple(sorted((int(id1), int(id2)))))
    return excluded


def collision_pair_descriptors(
    model: mujoco.MjModel, xml_path: Path
) -> list[dict[str, Any]]:
    """Generate eligible self-collision geom pairs using MJCF collision metadata."""
    excluded = _xml_excluded_body_pairs(xml_path, model)
    pairs: list[dict[str, Any]] = []
    for a in range(model.ngeom):
        body_a = int(model.geom_bodyid[a])
        contype_a = int(model.geom_contype[a])
        affinity_a = int(model.geom_conaffinity[a])
        if body_a == 0 or (contype_a == 0 and affinity_a == 0):
            continue
        for b in range(a + 1, model.ngeom):
            body_b = int(model.geom_bodyid[b])
            if body_b == 0 or int(model.body_weldid[body_a]) == int(model.body_weldid[body_b]):
                continue
            # MuJoCo's default parent filter and explicit MJCF excludes.
            if int(model.body_parentid[body_a]) == body_b or int(model.body_parentid[body_b]) == body_a:
                continue
            if tuple(sorted((body_a, body_b))) in excluded:
                continue
            contype_b = int(model.geom_contype[b])
            affinity_b = int(model.geom_conaffinity[b])
            if not ((contype_a & affinity_b) or (contype_b & affinity_a)):
                continue
            geom_a = object_name(model, mujoco.mjtObj.mjOBJ_GEOM, a, f"geom_{a}")
            geom_b = object_name(model, mujoco.mjtObj.mjOBJ_GEOM, b, f"geom_{b}")
            body_name_a = object_name(model, mujoco.mjtObj.mjOBJ_BODY, body_a, f"body_{body_a}")
            body_name_b = object_name(model, mujoco.mjtObj.mjOBJ_BODY, body_b, f"body_{body_b}")
            pairs.append({
                "key": f"{a}:{b}", "geom_a_id": a, "geom_b_id": b,
                "geom_a": geom_a, "geom_b": geom_b,
                "body_a": body_name_a, "body_b": body_name_b,
                "label": f"{body_name_a} / {geom_a} ↔ {body_name_b} / {geom_b}",
            })
    return pairs


def robot_model_metadata(repo_root: Path, config: dict[str, Any]) -> dict[str, Any]:
    xml_path = (repo_root / str(config["robot"]["mjcf"])).resolve()
    model = mujoco.MjModel.from_xml_path(str(xml_path))
    joints = joint_descriptors(model)
    bodies = body_descriptors(model, joints)
    raw_mapping_targets = config["robot"].get("mapping_target_links", [])
    if not isinstance(raw_mapping_targets, list):
        raise ValueError("Robot mapping_target_links must be an array")
    mapping_target_links = [str(name) for name in raw_mapping_targets]
    body_names = {str(body["name"]) for body in bodies}
    unknown_mapping_targets = sorted(set(mapping_target_links) - body_names)
    if unknown_mapping_targets:
        raise ValueError(
            "Robot mapping_target_links reference unknown bodies: "
            f"{unknown_mapping_targets}"
        )
    mapping_target_set = set(mapping_target_links)
    for body in bodies:
        body["mapping_target"] = str(body["name"]) in mapping_target_set
    presentation = ui_metadata(model, bodies, joints, config["robot"].get("ui", {}))
    return {
        "joints": joints,
        "bodies": bodies,
        "actuated_dof_count": sum(
            int(joint["dof_count"]) for joint in joints if joint["controllable"]
        ),
        "groups": presentation["groups"],
        "joint_symmetry": presentation["joint_symmetry"],
        "body_symmetry": presentation["body_symmetry"],
        "mapping_target_links": mapping_target_links,
        "collision_pairs": collision_pair_descriptors(model, xml_path),
    }
