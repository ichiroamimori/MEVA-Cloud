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
        rows.append({
            "id": jid,
            "name": name,
            "body": object_name(
                model, mujoco.mjtObj.mjOBJ_BODY, int(model.jnt_bodyid[jid]),
                f"body_{int(model.jnt_bodyid[jid])}",
            ),
            "dof_count": dof_count,
            "qpos_address": int(model.jnt_qposadr[jid]),
            "dof_address": int(model.jnt_dofadr[jid]),
            "limited": bool(model.jnt_limited[jid]),
            "range": [float(x) for x in model.jnt_range[jid]],
            "type": jtype,
        })
    return rows


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
    body_names = [
        object_name(model, mujoco.mjtObj.mjOBJ_BODY, i, f"body_{i}")
        for i in range(1, model.nbody)
    ]
    return {
        "joints": joints,
        "joint_symmetry": symmetry_map([x["name"] for x in joints]),
        "body_symmetry": symmetry_map(body_names),
        "collision_pairs": collision_pair_descriptors(model, xml_path),
    }
