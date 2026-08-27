# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import mujoco
import numpy as np

try:
    from .meva_canonical_geometry import (
        CANONICAL_GEOMETRY_VERSION,
        canonical_direction,
        canonical_geometry_hash,
    )
except ImportError:
    from meva_canonical_geometry import (
        CANONICAL_GEOMETRY_VERSION,
        canonical_direction,
        canonical_geometry_hash,
    )


# ============================================================
# Coordinate convention
# ============================================================
# MEVA world:
#   +X forward, +Y left, +Z up
#
# Paired MEVA CSV/BVH verification:
#   BVH +X -> MEVA +X
#   BVH +Y -> MEVA +Z
#   BVH +Z -> MEVA -Y
#
# Therefore the BVH zero-rotation frame -> MEVA world is Rx(+90 deg).
#
# Non-terminal segments:
#   Source geometry comes from versioned MEVA canonical directions.
#
# Terminal segments (Hand / Foot):
#   BVH End Site is NOT used to define orientation.
#   Instead, explicit semantic local frames are used.
#
# A mapping offset is cached as a derived User asset and regenerated when
# canonical geometry, MJCF, mappings, or algorithm version changes.
#
# Runtime-only IK settings such as temporal_regularization are deliberately
# excluded from the offset fingerprint. Changing temporal_regularization.cost
# must therefore NOT trigger geometric offset recalibration.
# ============================================================

ALGORITHM_VERSION = "geometry-v3.0-meva-canonical"

SQRT_HALF = float(np.sqrt(0.5))

Q_BVH_TO_MEVA_WXYZ = np.array(
    [SQRT_HALF, SQRT_HALF, 0.0, 0.0],
    dtype=np.float64,
)


# ============================================================
# MEVA non-terminal geometry
# ============================================================

BVH_DISTAL_JOINT = {
    "Pelvis": "PelvisLumbarSpine",
    "Thoracic2": "Thoracic2Head",

    # The only supported composite source.  Its runtime orientation is the
    # 50:50 SLERP of Thoracic2 and LumbarSpine.  For geometric offset
    # construction, use the real LumbarSpine -> Thoracic2 inter-joint BVH
    # direction.  The UI label intentionally follows the requested spelling
    # "LumberSpine"; the actual CSV/BVH segment remains "LumbarSpine".
    "Thoracic2+LumberSpine": "LumbarSpineThoracic2",

    "LeftUpperArm": "LeftUpperArmLeftForearm",
    "LeftForearm": "LeftForearmLeftHand",

    "RightUpperArm": "RightUpperArmRightForearm",
    "RightForearm": "RightForearmRightHand",

    "LeftUpperLeg": "LeftUpperLegLeftLowerLeg",
    "LeftLowerLeg": "LeftLowerLegLeftFoot",

    "RightUpperLeg": "RightUpperLegRightLowerLeg",
    "RightLowerLeg": "RightLowerLegRightFoot",
}


# ============================================================
# Terminal semantic frames
# ============================================================
#
# IMPORTANT:
# Hand / Foot DO NOT use BVH End Site.
#
# Each semantic frame is defined by:
#
#   primary
#       longitudinal direction
#
#   secondary
#       anatomically meaningful second axis
#
# Hand:
#   secondary = palm normal
#
# Foot:
#   secondary = upward sole normal
#
# All vectors below are LOCAL coordinates.
# ============================================================

MEVA_TERMINAL_SEMANTICS = {
    "LeftHand": {
        "primary": [0.0, -1.0, 0.0],
        "secondary": [0.0, 0.0, 1.0],
        "secondary_name": "palm_normal",
    },

    "RightHand": {
        "primary": [0.0, -1.0, 0.0],
        "secondary": [0.0, 0.0, -1.0],
        "secondary_name": "palm_normal",
    },

    "LeftFoot": {
        "primary": [1.0, 0.0, 0.0],
        "secondary": [0.0, 1.0, 0.0],
        "secondary_name": "sole_up_normal",
    },

    "RightFoot": {
        "primary": [1.0, 0.0, 0.0],
        "secondary": [0.0, 1.0, 0.0],
        "secondary_name": "sole_up_normal",
    },
}


# ============================================================
# Basic math
# ============================================================

def normalize(v):
    v = np.asarray(v, dtype=np.float64)

    n = float(np.linalg.norm(v))

    if not np.isfinite(n) or n <= 1e-12:
        raise ValueError(
            f"Cannot normalize vector: {v}"
        )

    return v / n


def normalize_quat(q):
    return normalize(
        np.asarray(
            q,
            dtype=np.float64,
        ).reshape(4)
    )


def quat_mul(a, b):
    out = np.empty(
        4,
        dtype=np.float64,
    )

    mujoco.mju_mulQuat(
        out,
        normalize_quat(a),
        normalize_quat(b),
    )

    return normalize_quat(out)


def quat_inv(q):
    q = normalize_quat(q)

    return np.array(
        [
            q[0],
            -q[1],
            -q[2],
            -q[3],
        ],
        dtype=np.float64,
    )


def quat_rotate(q, v):
    out = np.empty(
        3,
        dtype=np.float64,
    )

    mujoco.mju_rotVecQuat(
        out,
        np.asarray(
            v,
            dtype=np.float64,
        ),
        normalize_quat(q),
    )

    return out


def mat_to_quat(mat):
    out = np.empty(
        4,
        dtype=np.float64,
    )

    mujoco.mju_mat2Quat(
        out,
        np.asarray(
            mat,
            dtype=np.float64,
        ).reshape(9),
    )

    return normalize_quat(out)


# ============================================================
# Semantic frame construction
# ============================================================

def frame_from_primary(
    primary,
    reference,
):
    """
    Build a right-handed semantic frame.

    Column 0:
        primary axis

    Column 1:
        reference/secondary axis projected perpendicular
        to the primary axis

    Column 2:
        right-handed completion

    The same semantic columns must be used for source and robot.
    """

    e0 = normalize(primary)

    ref = np.asarray(
        reference,
        dtype=np.float64,
    )

    e1 = ref - np.dot(
        ref,
        e0,
    ) * e0

    if np.linalg.norm(e1) < 1e-8:
        for fallback in (
            np.array(
                [1.0, 0.0, 0.0],
                dtype=np.float64,
            ),
            np.array(
                [0.0, 0.0, 1.0],
                dtype=np.float64,
            ),
            np.array(
                [0.0, 1.0, 0.0],
                dtype=np.float64,
            ),
        ):
            e1 = (
                fallback
                - np.dot(
                    fallback,
                    e0,
                ) * e0
            )

            if np.linalg.norm(e1) >= 1e-8:
                break

    e1 = normalize(e1)

    e2 = normalize(
        np.cross(
            e0,
            e1,
        )
    )

    e1 = normalize(
        np.cross(
            e2,
            e0,
        )
    )

    return np.column_stack(
        [
            e0,
            e1,
            e2,
        ]
    )


def preferred_world_reference(
    long_axis_world,
):
    """
    Zero-twist reference for non-terminal segments.

    Mostly X-oriented segment:
        use world +Z

    Otherwise:
        use world +X
    """

    d = normalize(
        long_axis_world
    )

    forward = np.array(
        [1.0, 0.0, 0.0],
        dtype=np.float64,
    )

    up = np.array(
        [0.0, 0.0, 1.0],
        dtype=np.float64,
    )

    if abs(
        float(
            np.dot(
                d,
                forward,
            )
        )
    ) > 0.85:
        return up

    return forward


# ============================================================
# Repository helpers
# ============================================================

def find_repo_root(
    start: Path,
) -> Path:

    p = start.resolve()

    for candidate in [
        p,
        *p.parents,
    ]:
        if (
            (candidate / "server").exists()
            and
            (candidate / "workspace").exists()
        ):
            return candidate

    raise FileNotFoundError(
        "repo root not found"
    )


def sha256(
    path: Path,
) -> str:

    h = hashlib.sha256()

    with path.open(
        "rb"
    ) as f:

        while True:
            chunk = f.read(
                1024 * 1024
            )

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()


# ============================================================
# BVH hierarchy parser
# ============================================================

TOKEN_RE = re.compile(
    r"\{|\}|[^\s{}]+"
)


def parse_bvh_offsets(
    path: Path,
):
    """
    Parse HIERARCHY/OFFSET data.

    Returns:

        offsets[joint_name]
            normal ROOT / JOINT OFFSET

        endsites[parent_joint_name]
            End Site OFFSET

    End Site is still parsed for inspection/debugging,
    but Hand / Foot orientation generation does NOT use it.
    """

    text = path.read_text(
        encoding="utf-8",
        errors="replace",
    )

    hierarchy = text.split(
        "MOTION",
        1,
    )[0]

    tokens = TOKEN_RE.findall(
        hierarchy
    )

    offsets = {}
    endsites = {}

    joint_stack = []

    context_stack = []

    pending_context = None

    i = 0

    while i < len(tokens):

        tok = tokens[i]

        if tok in (
            "ROOT",
            "JOINT",
        ):

            if i + 1 >= len(tokens):
                raise ValueError(
                    f"Malformed BVH near token {i}: {tok}"
                )

            name = tokens[
                i + 1
            ]

            pending_context = (
                "joint",
                name,
            )

            i += 2
            continue

        if tok == "End":

            if (
                i + 1 >= len(tokens)
                or
                tokens[i + 1] != "Site"
            ):
                raise ValueError(
                    f"Malformed BVH End Site near token {i}"
                )

            if not joint_stack:
                raise ValueError(
                    "BVH End Site found without parent joint"
                )

            pending_context = (
                "end",
                joint_stack[-1],
            )

            i += 2
            continue

        if tok == "{":

            if pending_context is None:

                context_stack.append(
                    (
                        "other",
                        None,
                    )
                )

            else:

                kind, name = pending_context

                context_stack.append(
                    (
                        kind,
                        name,
                    )
                )

                if kind == "joint":
                    joint_stack.append(
                        name
                    )

                pending_context = None

            i += 1
            continue

        if tok == "}":

            if not context_stack:
                raise ValueError(
                    f"Unbalanced BVH closing brace near token {i}"
                )

            kind, name = (
                context_stack.pop()
            )

            if kind == "joint":

                if (
                    not joint_stack
                    or
                    joint_stack[-1] != name
                ):
                    raise ValueError(
                        f"BVH joint stack mismatch while closing {name}"
                    )

                joint_stack.pop()

            # End Site does NOT pop joint_stack.

            i += 1
            continue

        if tok == "OFFSET":

            if i + 3 >= len(tokens):
                raise ValueError(
                    f"Malformed BVH OFFSET near token {i}"
                )

            vec = np.array(
                [
                    float(
                        tokens[i + 1]
                    ),
                    float(
                        tokens[i + 2]
                    ),
                    float(
                        tokens[i + 3]
                    ),
                ],
                dtype=np.float64,
            )

            if not context_stack:
                raise ValueError(
                    "BVH OFFSET found outside hierarchy block"
                )

            kind, name = (
                context_stack[-1]
            )

            if kind == "joint":
                offsets[name] = vec

            elif kind == "end":
                endsites[name] = vec

            i += 4
            continue

        i += 1

    return (
        offsets,
        endsites,
    )


def source_long_axis_canonical(segment: str):
    """Return the Capsule-independent canonical MEVA segment direction."""
    return canonical_direction(segment)


# ============================================================
# Robot geometry from MJCF
# ============================================================

def body_world_pose_qpos0(
    model,
    body_name,
):

    bid = mujoco.mj_name2id(
        model,
        mujoco.mjtObj.mjOBJ_BODY,
        body_name,
    )

    if bid < 0:
        raise KeyError(
            f"Robot body not found: {body_name}"
        )

    data = mujoco.MjData(
        model
    )

    mujoco.mj_resetData(
        model,
        data,
    )

    mujoco.mj_forward(
        model,
        data,
    )

    pos = np.asarray(
        data.xpos[bid],
        dtype=np.float64,
    ).copy()

    mat = np.asarray(
        data.xmat[bid],
        dtype=np.float64,
    ).reshape(
        3,
        3,
    ).copy()

    quat = mat_to_quat(
        mat
    )

    return (
        pos,
        mat,
        quat,
    )


def robot_long_axis_local(
    model,
    target_link,
    target_geometry,
):

    if target_link not in target_geometry:

        raise KeyError(
            f"No robot geometry rule for target link: {target_link}. "
            "Add it to the Variant manifest retargeting.target_geometry."
        )

    rule = target_geometry[target_link]
    if not isinstance(rule, dict):
        raise ValueError(f"Invalid robot geometry rule for {target_link}")
    kind = str(rule.get("type") or "")

    if kind == "local_vector":

        return normalize(
            rule.get("vector")
        )

    if kind == "body_to_body":

        p0, R0, _ = (
            body_world_pose_qpos0(
                model,
                target_link,
            )
        )

        p1, _, _ = (
            body_world_pose_qpos0(
                model,
                str(rule.get("distal_body") or ""),
            )
        )

        return normalize(
            R0.T @ (
                p1 - p0
            )
        )

    raise ValueError(
        kind
    )


# ============================================================
# Terminal mapping
# ============================================================

def build_terminal_semantic_offset(
    source_segment,
    target_link,
    terminal_semantics,
):
    """
    Build Hand / Foot full-orientation offset
    from explicit semantic frames.

    BVH End Site is NOT used.
    """

    if (
        source_segment
        not in
        MEVA_TERMINAL_SEMANTICS
    ):
        raise KeyError(
            source_segment
        )

    if (
        target_link
        not in
        terminal_semantics
    ):
        raise KeyError(
            f"No terminal semantic rule for target link: {target_link}"
        )

    src = (
        MEVA_TERMINAL_SEMANTICS[
            source_segment
        ]
    )

    robot = (
        terminal_semantics[
            target_link
        ]
    )

    if (
        src["secondary_name"]
        !=
        robot["secondary_name"]
    ):
        raise ValueError(
            f"Semantic mismatch: "
            f"{source_segment} uses "
            f"{src['secondary_name']} "
            f"but {target_link} uses "
            f"{robot['secondary_name']}"
        )

    src_axis_local = normalize(
        src["primary"]
    )

    src_secondary_local = normalize(
        src["secondary"]
    )

    robot_axis_local = normalize(
        robot["primary"]
    )

    robot_secondary_local = normalize(
        robot["secondary"]
    )

    F_meva = frame_from_primary(
        src_axis_local,
        src_secondary_local,
    )

    F_robot = frame_from_primary(
        robot_axis_local,
        robot_secondary_local,
    )

    # Want:
    #
    # q_meva * q_offset * F_robot
    #     =
    # q_meva * F_meva
    #
    # therefore:
    #
    # q_offset
    #     =
    # F_meva * inv(F_robot)

    R_offset = (
        F_meva
        @
        F_robot.T
    )

    q_offset = mat_to_quat(
        R_offset
    )

    detail = {
        "source_geometry_mode":
            "semantic_frame",

        "source_primary_axis_local":
            [
                float(x)
                for x
                in src_axis_local
            ],

        "robot_long_axis_link_local":
            [
                float(x)
                for x
                in robot_axis_local
            ],

        "source_secondary_axis_local":
            [
                float(x)
                for x
                in src_secondary_local
            ],

        "robot_secondary_axis_link_local":
            [
                float(x)
                for x
                in robot_secondary_local
            ],

        "secondary_axis_semantics":
            src["secondary_name"],

        "uses_bvh_end_site":
            False,
    }

    return (
        q_offset,
        detail,
    )


# ============================================================
# Mapping offset
# ============================================================

def build_mapping_offset(
    model,
    source_segment,
    target_link,
    target_geometry,
    terminal_semantics,
    bvh_offsets=None,
    bvh_endsites=None,
):
    """
    Build:

        q_target
            =
        q_meva
            *
        q_mapping_offset

    Terminal Hand / Foot:
        semantic-frame method

    Other segments:
        MEVA canonical geometry method
    """

    # --------------------------------------------------------
    # Terminal segments
    # --------------------------------------------------------

    if (
        source_segment
        in
        MEVA_TERMINAL_SEMANTICS
    ):

        return (
            build_terminal_semantic_offset(
                source_segment,
                target_link,
                terminal_semantics,
            )
        )

    # --------------------------------------------------------
    # Non-terminal segments
    # --------------------------------------------------------

    src_axis_local = (
        source_long_axis_canonical(source_segment)
    )

    # Source long axis in MEVA world
    # at BVH zero rotation.

    src_axis_world0 = quat_rotate(
        Q_BVH_TO_MEVA_WXYZ,
        src_axis_local,
    )

    ref_world = (
        preferred_world_reference(
            src_axis_world0
        )
    )

    # Same world reference represented
    # in source local coordinates.

    src_ref_local = quat_rotate(
        quat_inv(
            Q_BVH_TO_MEVA_WXYZ
        ),
        ref_world,
    )

    F_meva = frame_from_primary(
        src_axis_local,
        src_ref_local,
    )

    # Robot long axis in target-link local coordinates.

    robot_axis_local = (
        robot_long_axis_local(
            model,
            target_link,
            target_geometry,
        )
    )

    # Same world reference represented
    # in robot-link local coordinates at qpos0.

    _, _, q_robot0 = (
        body_world_pose_qpos0(
            model,
            target_link,
        )
    )

    robot_ref_local = quat_rotate(
        quat_inv(
            q_robot0
        ),
        ref_world,
    )

    F_robot = frame_from_primary(
        robot_axis_local,
        robot_ref_local,
    )

    R_offset = (
        F_meva
        @
        F_robot.T
    )

    q_offset = mat_to_quat(
        R_offset
    )

    detail = {
        "source_geometry_mode":
            "meva_canonical_direction",

        "source_long_axis_canonical_local":
            [
                float(x)
                for x
                in src_axis_local
            ],

        "robot_long_axis_link_local":
            [
                float(x)
                for x
                in robot_axis_local
            ],

        "uses_bvh_end_site":
            False,
    }

    return (
        q_offset,
        detail,
    )


# ============================================================
# Cache / public API
# ============================================================

def _mapping_signature(
    mappings,
):

    return [
        {
            "source_segment":
                m["source_segment"],

            "target_link":
                m["target_link"],
        }

        for m
        in mappings
    ]


def offset_fingerprint(
    cfg: dict,
    mjcf_path: Path,
    *,
    algorithm_version: str = ALGORITHM_VERSION,
    geometry_version: str = CANONICAL_GEOMETRY_VERSION,
    geometry_hash: str | None = None,
    robot_retargeting: dict | None = None,
) -> dict:
    """Return the complete Capsule-independent offset cache identity."""
    return {
        "algorithm_version": algorithm_version,
        "meva_canonical_geometry_version": geometry_version,
        "meva_canonical_geometry_sha256": (
            geometry_hash
            if geometry_hash is not None
            else canonical_geometry_hash(terminal_semantics=MEVA_TERMINAL_SEMANTICS)
        ),
        "mjcf_sha256": sha256(mjcf_path),
        "robot_retargeting_sha256": hashlib.sha256(
            json.dumps(
                robot_retargeting or {}, sort_keys=True, separators=(",", ":")
            ).encode("utf-8")
        ).hexdigest(),
        "mappings": _mapping_signature(cfg["mappings"]),
    }


def resolve_bvh_path(
    repo: Path,
    cfg: dict,
) -> Path:

    source = cfg[
        "source"
    ]

    if source.get(
        "bvh"
    ):
        return (
            repo
            /
            source["bvh"]
        ).resolve()

    csv_path = (
        repo
        /
        source["file"]
    ).resolve()

    candidate = (
        csv_path.with_suffix(
            ".bvh"
        )
    )

    if not candidate.exists():

        raise FileNotFoundError(
            "Paired BVH not found. "
            "Either place it beside the CSV "
            "with the same basename or set "
            "source.bvh in config.json.\n"
            f"Expected: {candidate}"
        )

    return candidate


def offsets_path_for_config(
    config_path: Path,
    cfg: dict,
    fingerprint_hash: str,
) -> Path:
    repo = find_repo_root(config_path)
    manufacturer = str(cfg.get("robot", {}).get("manufacturer") or "")
    variant = str(cfg.get("robot", {}).get("variant") or "")
    safe = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.-]*$")
    if not safe.fullmatch(manufacturer) or not safe.fullmatch(variant):
        raise ValueError("Unsafe Robot identity for offset cache")
    return (
        repo / "workspace" / "users" / "local_user" / "retarget_assets"
        / "offsets" / "meva" / manufacturer / variant
        / f"{fingerprint_hash}.json"
    )


def compute_offsets(
    config_path: Path,
    force=False,
):
    """
    Public API used by primary_retarget.py.

    Returns:
        offsets_by_link,
        output_path,
        generated
    """

    config_path = (
        config_path.resolve()
    )

    cfg = json.loads(
        config_path.read_text(
            encoding="utf-8"
        )
    )

    repo = find_repo_root(
        config_path
    )

    application_root = Path(__file__).resolve().parents[2]
    if str(application_root) not in sys.path:
        sys.path.insert(0, str(application_root))
    from server.robot_registry import resolve_variant, variant_retargeting_metadata

    robot_identity = cfg.get("robot", {})
    variant_record = resolve_variant(
        str(robot_identity.get("variant") or ""),
        manufacturer_id=str(robot_identity.get("manufacturer") or "") or None,
        robot_id=str(robot_identity.get("model") or "") or None,
        root=application_root,
    )
    robot_retargeting = variant_retargeting_metadata(variant_record)
    target_geometry = robot_retargeting.get("target_geometry")
    terminal_semantics = robot_retargeting.get("terminal_semantics")
    if not isinstance(target_geometry, dict) or not isinstance(terminal_semantics, dict):
        raise ValueError(
            "Variant manifest requires retargeting.target_geometry and "
            f"retargeting.terminal_semantics: {variant_record.manufacturer_id}/"
            f"{variant_record.robot_id}/{variant_record.variant_id}"
        )

    mjcf_path = (
        repo
        /
        cfg["robot"]["mjcf"]
    ).resolve()

    if not mjcf_path.exists():
        raise FileNotFoundError(
            mjcf_path
        )

    # Keep this fingerprint strictly geometric. In particular,
    # temporal_regularization is a runtime IK objective and is intentionally
    # NOT included here.
    canonical_hash = canonical_geometry_hash(terminal_semantics=MEVA_TERMINAL_SEMANTICS)
    fingerprint = offset_fingerprint(
        cfg, mjcf_path, geometry_hash=canonical_hash,
        robot_retargeting=robot_retargeting,
    )
    fingerprint_hash = hashlib.sha256(
        json.dumps(fingerprint, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    out_path = offsets_path_for_config(
        config_path, cfg, fingerprint_hash
    ).resolve()

    # --------------------------------------------------------
    # Cache reuse
    # --------------------------------------------------------

    if (
        out_path.exists()
        and
        not force
    ):

        old = json.loads(
            out_path.read_text(
                encoding="utf-8"
            )
        )

        if (
            old.get(
                "fingerprint"
            )
            ==
            fingerprint
        ):

            offsets = {
                k:
                    normalize_quat(v)

                for k, v
                in
                old[
                    "offsets_wxyz_by_link"
                ].items()
            }

            print(
                "OFFSET cache reused:",
                out_path,
            )

            return (
                offsets,
                out_path,
                False,
            )

    # --------------------------------------------------------
    # Generate
    # --------------------------------------------------------

    model = (
        mujoco.MjModel.from_xml_path(
            str(
                mjcf_path
            )
        )
    )

    offsets = {}
    details = {}

    for m in cfg[
        "mappings"
    ]:

        src = m[
            "source_segment"
        ]

        dst = m[
            "target_link"
        ]

        (
            q,
            detail,
        ) = build_mapping_offset(
            model,
            src,
            dst,
            target_geometry,
            terminal_semantics,
        )

        offsets[
            dst
        ] = q

        details[
            dst
        ] = {
            "source_segment":
                src,

            **detail,

            "offset_quaternion_wxyz":
                [
                    float(x)
                    for x
                    in q
                ],
        }

        print(
            f"OFFSET "
            f"{src:16s} "
            f"-> "
            f"{dst:28s} "
            f"{q.tolist()}"
        )

    # --------------------------------------------------------
    # Save cache
    # --------------------------------------------------------

    asset = {
        "schema_version":
            "2.1",

        "algorithm":
            ALGORITHM_VERSION,

        "meva_canonical_geometry_version": CANONICAL_GEOMETRY_VERSION,

        "meva_canonical_geometry_sha256": canonical_hash,

        "robot_mjcf": (
            str(mjcf_path.relative_to(repo)).replace("\\", "/")
            if mjcf_path.is_relative_to(repo)
            else str(mjcf_path).replace("\\", "/")
        ),

        "fingerprint":
            fingerprint,

        "offsets_wxyz_by_link":
            {
                k:
                    [
                        float(x)
                        for x
                        in q
                    ]

                for k, q
                in offsets.items()
            },

        "details":
            details,
    }

    out_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    out_path.write_text(
        json.dumps(
            asset,
            ensure_ascii=False,
            indent=2,
        )
        +
        "\n",
        encoding="utf-8",
    )

    print(
        "OFFSET cache written:",
        out_path,
    )

    return (
        offsets,
        out_path,
        True,
    )


# ============================================================
# CLI
# ============================================================

def main():

    ap = argparse.ArgumentParser(
        description=(
            "Compute/cache "
            "MEVA canonical geometry -> robot(MJCF) "
            "mapping offsets."
        )
    )

    ap.add_argument(
        "config",
        type=Path,
    )

    ap.add_argument(
        "--force",
        action="store_true",
    )

    args = (
        ap.parse_args()
    )

    (
        offsets,
        path,
        generated,
    ) = compute_offsets(
        args.config,
        force=args.force,
    )

    print()

    print(
        "Generated:"
        if generated
        else
        "Reused:",
        path,
    )

    print(
        "Mappings :",
        len(offsets),
    )


if __name__ == "__main__":
    main()
