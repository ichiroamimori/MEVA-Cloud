# -*- coding: utf-8 -*-
from __future__ import annotations

import csv
import io
import json
import struct
from pathlib import Path
from typing import Any

import mujoco
import numpy as np

try:
    from .main_calibration import foot_contact_geom_ids
    from .motion_io import load_motion
except ImportError:
    from main_calibration import foot_contact_geom_ids
    from motion_io import load_motion

LEGACY_MAGIC = b"MEVAVW01"
MAGIC = b"MEVAVW02"
FORMAT_VERSION = 5

MEVA_SEGMENTS = [
    "Pelvis", "LumbarSpine", "Thoracic2", "Head",
    "LeftScapula", "LeftUpperArm", "LeftForearm", "LeftHand",
    "RightScapula", "RightUpperArm", "RightForearm", "RightHand",
    "LeftUpperLeg", "LeftLowerLeg", "LeftFoot",
    "RightUpperLeg", "RightLowerLeg", "RightFoot",
]

# Anatomical joint centers already solved by MEVA and stored in the CSV as
# <Joint>_g_x/y/z.  These are intentionally kept separate from segment
# origins (<Segment>_g_x/y/z): the two are not generally coincident.
MEVA_JOINTS = [
    "Neck",
    "LeftSCJoint", "LeftShoulder", "LeftElbow", "LeftWrist",
    "RightSCJoint", "RightShoulder", "RightElbow", "RightWrist",
    "LumbosacralJoint", "ThoracolumbarJoint",
    "LeftHip", "LeftKnee", "LeftAnkle",
    "RightHip", "RightKnee", "RightAnkle",
]


def _read_header(path: Path) -> dict[str, Any] | None:
    try:
        with path.open("rb") as f:
            magic = f.read(8)
            if magic == MAGIC:
                struct.unpack("<I", f.read(4))[0]  # fixed-header format version
            elif magic != LEGACY_MAGIC:
                return None
            header_len = struct.unpack("<I", f.read(4))[0]
            return json.loads(f.read(header_len).decode("utf-8"))
    except Exception:
        return None


def _is_current(path: Path, kind: str) -> bool:
    if not path.exists():
        return False
    h = _read_header(path)
    minimum_version = 4 if kind == "meva" else FORMAT_VERSION
    if not (
        h
        and int(h.get("format_version", 0)) >= minimum_version
        and h.get("kind") == kind
    ):
        return False
    if kind == "meva":
        block_names = {b.get("name") for b in h.get("blocks", [])}
        if "joint_pos" not in block_names or not h.get("joint_names"):
            return False
    return True


def _serialize_bin(metadata: dict[str, Any], arrays: dict[str, np.ndarray]) -> bytes:
    """Serialize the viewer container to bytes without creating a file."""
    blocks = []
    offset = 0
    payloads = []
    for name, arr0 in arrays.items():
        arr = np.ascontiguousarray(arr0)
        if arr.dtype == np.uint8:
            arr = arr.astype("u1", copy=False)
            dtype = "uint8"
        elif arr.dtype.kind in "iu":
            arr = arr.astype("<i4", copy=False)
            dtype = "int32"
        else:
            arr = arr.astype("<f4", copy=False)
            dtype = "float32"
        raw = arr.tobytes(order="C")
        descriptor = {
            "name": name,
            "dtype": dtype,
            "shape": list(arr.shape),
            "offset": offset,
            "nbytes": len(raw),
        }
        descriptor.update(dict(metadata.get("array_metadata", {}).get(name, {})))
        blocks.append(descriptor)
        payloads.append(raw)
        offset += len(raw)

    header = {
        **metadata,
        "format": "MEVA Viewer Binary",
        "format_version": FORMAT_VERSION,
        "schema_version": str(metadata.get("schema_version", "1.0")),
        "endianness": "little",
        "array_offset_basis": "payload_start",
        "blocks": blocks,
    }
    header_raw = json.dumps(
        header, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")

    out = io.BytesIO()
    out.write(MAGIC)
    out.write(struct.pack("<I", FORMAT_VERSION))
    out.write(struct.pack("<I", len(header_raw)))
    out.write(header_raw)
    for raw in payloads:
        out.write(raw)
    return out.getvalue()


def _write_bin(path: Path, metadata: dict[str, Any], arrays: dict[str, np.ndarray]) -> None:
    """Write a cached viewer container. Used only for the capsule-level MEVA cache."""
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = _serialize_bin(metadata, arrays)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(raw)
    tmp.replace(path)


def write_viewer_bin(
    path: Path, metadata: dict[str, Any], arrays: dict[str, np.ndarray]
) -> Path:
    """Persist one self-describing viewer binary atomically."""
    _write_bin(path, metadata, arrays)
    return path


def _hinge_info(model: mujoco.MjModel):
    out = []
    for j in range(model.njnt):
        if model.jnt_type[j] != mujoco.mjtJoint.mjJNT_HINGE:
            continue
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, j)
        out.append((name or f"joint_{j}", int(model.jnt_qposadr[j])))
    return out


def _body_names(model: mujoco.MjModel) -> list[str]:
    names = []
    for i in range(1, model.nbody):  # skip world
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, i)
        names.append(name or f"body_{i}")
    return names


def build_retarget_viewer_bytes(
    repo_root: Path,
    capsule_id: str,
    robot_variant: str,
    run_id: str,
    user_id: str = "local_user",
    stage: str = "primary",
    main_id: str = "legacy",
) -> bytes:
    """Build legacy/Main viewer bytes from canonical NPZ or legacy PKL."""
    stage = str(stage).strip().lower()
    if stage not in {"primary", "main"}:
        raise ValueError(f"Unsupported retarget viewer stage: {stage}")

    run_dir = (
        repo_root / "workspace" / "users" / user_id / "capsules"
        / capsule_id / "retarget" / robot_variant / run_id
    )
    primary_run_dir = run_dir
    file_id = run_id
    if stage == "main" and main_id != "legacy":
        preferred = run_dir / main_id
        legacy = run_dir / "main" / main_id
        run_dir = preferred if preferred.exists() or not legacy.exists() else legacy
        file_id = main_id
    motion_path = run_dir / f"{file_id}_{stage}.npz"
    if not motion_path.exists():
        legacy_candidates = [run_dir / f"{file_id}_{stage}.pkl"]
        if stage == "primary":
            legacy_candidates.append(run_dir / "primary.pkl")
        legacy = next((path for path in legacy_candidates if path.exists()), None)
        if legacy is not None:
            motion_path = legacy
    if not motion_path.exists():
        raise FileNotFoundError(
            f"Retarget motion not found for stage '{stage}': {motion_path}"
        )

    config_path = (
        run_dir / f"{main_id}_main_config.json"
        if stage == "main" and main_id != "legacy"
        else run_dir / f"{run_id}_primary_config.json"
    )
    if not config_path.exists():
        legacy_candidates = (
            (run_dir / "main.json", run_dir / f"{main_id}_main.json")
            if stage == "main" and main_id != "legacy"
            else (run_dir / f"{run_id}_config.json", run_dir / "config.json")
        )
        config_path = next((path for path in legacy_candidates if path.exists()), config_path)
        if not config_path.exists():
            raise FileNotFoundError(
                f"Run config not found: {config_path}"
            )

    with config_path.open("r", encoding="utf-8") as f:
        cfg = json.load(f)
    pkl = load_motion(motion_path)

    root_pos = np.asarray(pkl["root_pos"], dtype=np.float32)
    root_rot = np.asarray(pkl["root_rot"], dtype=np.float32)
    dof_pos = np.asarray(pkl["dof_pos"], dtype=np.float32)
    n = int(root_pos.shape[0])

    source_frames = pkl.get("source_frame_indices")
    if source_frames is None:
        fr = cfg.get("frame_range", {})
        start = int(fr.get("start", 0))
        step = int(fr.get("step", 1))
        source_frames = start + np.arange(n, dtype=np.int32) * step
    source_frames = np.asarray(source_frames, dtype=np.int32)
    local_frames = np.arange(n, dtype=np.int32)
    source_frame_float = np.asarray(
        pkl.get("source_frame_float", source_frames), dtype=np.float64
    )
    if source_frame_float.shape != (n,):
        source_frame_float = source_frames.astype(np.float64)
    fps = float(pkl.get("fps", cfg["source"]["sampling_rate_hz"]))
    time_s = np.asarray(
        pkl.get("time_s", np.arange(n, dtype=np.float64) / fps),
        dtype=np.float64,
    )
    if time_s.shape != (n,):
        time_s = np.arange(n, dtype=np.float64) / fps

    xml_path = (repo_root / cfg["robot"]["mjcf"]).resolve()
    model = mujoco.MjModel.from_xml_path(str(xml_path))
    data = mujoco.MjData(model)

    bodies = _body_names(model)
    body_ids = np.arange(1, model.nbody, dtype=np.int32)
    link_pos = np.empty((n, len(body_ids), 3), dtype=np.float32)
    link_quat = np.empty((n, len(body_ids), 4), dtype=np.float32)

    mapped_links = {
        str(item.get("source_segment")): str(item.get("target_link"))
        for item in cfg.get("mappings", [])
        if item.get("source_segment") and item.get("target_link")
    }
    sole_geom_ids: dict[str, list[int]] = {}
    geom_names: list[str] = []
    for side, source_segment, fallback in (
        ("left", "LeftFoot", "left_ankle_roll_link"),
        ("right", "RightFoot", "right_ankle_roll_link"),
    ):
        ids = list(foot_contact_geom_ids(
            model, mapped_links.get(source_segment, fallback)
        ).values())
        sole_geom_ids[side] = ids
        geom_names.extend([f"{side}_sole_{index}" for index in range(1, 5)])
        geom_names.append(f"{side}_sole_min")
    geom_pos = np.empty((n, len(geom_names), 3), dtype=np.float32)

    hinges = _hinge_info(model)
    if len(hinges) != dof_pos.shape[1]:
        raise ValueError(
            f"Motion dof count {dof_pos.shape[1]} does not match "
            f"MJCF hinge count {len(hinges)}"
        )

    # Find the single free joint.
    free_joints = [
        j for j in range(model.njnt)
        if model.jnt_type[j] == mujoco.mjtJoint.mjJNT_FREE
    ]
    if len(free_joints) != 1:
        raise ValueError(f"Expected one free joint, got {len(free_joints)}")
    free_qadr = int(model.jnt_qposadr[free_joints[0]])

    root_order = (
        pkl.get("metadata", {}).get("root_rot_order")
        or cfg.get("output", {}).get("root_rot_order", "xyzw")
    )

    for i in range(n):
        data.qpos[:] = model.qpos0
        data.qpos[free_qadr:free_qadr + 3] = root_pos[i]
        r = root_rot[i]
        if root_order == "xyzw":
            wxyz = np.array([r[3], r[0], r[1], r[2]], dtype=float)
        else:
            wxyz = np.asarray(r, dtype=float)
        wxyz /= max(np.linalg.norm(wxyz), 1e-12)
        data.qpos[free_qadr + 3:free_qadr + 7] = wxyz

        for k, (_, qadr) in enumerate(hinges):
            data.qpos[qadr] = dof_pos[i, k]

        mujoco.mj_forward(model, data)
        link_pos[i] = data.xpos[body_ids]
        link_quat[i] = data.xquat[body_ids]
        geom_index = 0
        for side in ("left", "right"):
            ids = sole_geom_ids[side]
            positions = np.asarray(data.geom_xpos[ids], dtype=np.float32)
            geom_pos[i, geom_index:geom_index + 4] = positions
            geom_pos[i, geom_index + 4] = positions[int(np.argmin(positions[:, 2]))]
            geom_index += 5

    # Viewer orientation comparison needs the same MEVA->robot frame
    # conversion used by Primary.  Persist the run's offset snapshot in
    # metadata so browser-side Roll/Pitch/Yaw compares like with like.
    mapping_offsets = {}
    try:
        from .check_offsets import compute_offsets
        _, offsets_path, _ = compute_offsets(config_path)
        with offsets_path.open("r", encoding="utf-8") as f:
            offset_asset = json.load(f)
        mapping_offsets = offset_asset.get("offsets_wxyz_by_link", {})
    except Exception:
        mapping_offsets = {}

    world_alignment = (
        cfg.get("world_alignment", {})
        .get("offset_quaternion_wxyz", [1.0, 0.0, 0.0, 0.0])
    )

    return _serialize_bin(
        {
            "kind": "retarget",
            "stage": stage,
            "capsule_id": capsule_id,
            "retargeted_data_id": run_id,
            "robot_variant": robot_variant,
            "fps": fps,
            # New trajectories are indexed by their local Primary/Main frame.
            # The authoritative link back to MEVA remains in the arrays below.
            "source_frame_start": 0,
            "source_frame_stop": n,
            "source_frame_step": 1,
            "frame_count": n,
            "root_rot_order": root_order,
            "joint_names": [name for name, _ in hinges],
            "link_names": bodies,
            "geom_names": geom_names,
            "geom_position_note": (
                "Four sole contact GEOM centers per Foot plus the full XYZ of "
                "the GEOM having minimum world Z in each frame."
            ),
            "mappings": cfg.get("mappings", []),
            "mapping_offsets_wxyz_by_link": mapping_offsets,
            "world_alignment_wxyz": world_alignment,
            "body_parent_index_note": "Indices refer to link_names; -1 means world.",
            "mjcf": cfg["robot"]["mjcf"],
            "rendering": {
                "preferred": "mujoco_wasm",
                "plot_pose_available": True,
            },
        },
        {
            "source_frame": local_frames,
            "source_frame_nearest": source_frames,
            "source_frame_float": source_frame_float,
            "time_s": time_s,
            "root_pos": root_pos,
            "root_rot": root_rot,
            "dof_pos": dof_pos,
            "link_pos": link_pos,
            "link_quat": link_quat,
            "geom_pos": geom_pos,
            "body_parent_index": np.asarray([
                int(model.body_parentid[bid] - 1) if int(model.body_parentid[bid]) > 0 else -1
                for bid in body_ids
            ], dtype=np.int32),
        },
    )


def _read_csv_header_and_rows(
    csv_path: Path,
    header_row_1based: int,
):
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    hi = header_row_1based - 1
    if hi < 0 or hi >= len(rows):
        raise ValueError(f"Bad header_row_1based={header_row_1based}")
    header = [x.strip() for x in rows[hi]]
    data_rows = rows[hi + 1:]
    return header, data_rows


def generate_meva_viewer_bin(
    repo_root: Path,
    capsule_id: str,
    config: dict[str, Any],
    user_id: str = "local_user",
) -> Path:
    meva_dir = (
        repo_root / "workspace" / "users" / user_id
        / "capsules" / capsule_id / "meva"
    )
    out_path = meva_dir / f"{capsule_id}_meva_viewer.bin"
    if _is_current(out_path, "meva"):
        return out_path

    csv_path = (repo_root / config["source"]["file"]).resolve()
    header, rows = _read_csv_header_and_rows(
        csv_path,
        int(config["source"].get("header_row_1based", 1)),
    )
    col = {name: i for i, name in enumerate(header)}

    # MEVA segment origin positions use <Segment>_g_x/y/z.
    # Joint/landmark coordinates use <Name>_x/y/z, so do not use that suffix
    # for segment discovery.
    discovered = []
    for name in header:
        if name.endswith("_g_x"):
            base = name[:-4]
            if (
                f"{base}_g_y" in col and f"{base}_g_z" in col
                and f"{base}_q_gs_w" in col
                and f"{base}_q_gs_x" in col
                and f"{base}_q_gs_y" in col
                and f"{base}_q_gs_z" in col
            ):
                discovered.append(base)
    segments = [s for s in MEVA_SEGMENTS if s in discovered]
    segments += [s for s in discovered if s not in segments]
    if not segments:
        raise ValueError(
            "No MEVA segment position/quaternion columns were discovered."
        )

    joints = [
        j for j in MEVA_JOINTS
        if all(f"{j}_g_{axis}" in col for axis in "xyz")
    ]

    n = len(rows)
    pos = np.empty((n, len(segments), 3), dtype=np.float32)
    quat = np.empty((n, len(segments), 4), dtype=np.float32)
    joint_pos = np.empty((n, len(joints), 3), dtype=np.float32)

    for fi, row in enumerate(rows):
        for si, seg in enumerate(segments):
            pos[fi, si] = [
                float(row[col[f"{seg}_g_x"]]),
                float(row[col[f"{seg}_g_y"]]),
                float(row[col[f"{seg}_g_z"]]),
            ]
            quat[fi, si] = [
                float(row[col[f"{seg}_q_gs_w"]]),
                float(row[col[f"{seg}_q_gs_x"]]),
                float(row[col[f"{seg}_q_gs_y"]]),
                float(row[col[f"{seg}_q_gs_z"]]),
            ]
        for ji, joint in enumerate(joints):
            joint_pos[fi, ji] = [
                float(row[col[f"{joint}_g_x"]]),
                float(row[col[f"{joint}_g_y"]]),
                float(row[col[f"{joint}_g_z"]]),
            ]

    _write_bin(
        out_path,
        {
            "kind": "meva",
            "capsule_id": capsule_id,
            "fps": float(config["source"].get("sampling_rate_hz", 100)),
            "source_frame_start": 0,
            "source_frame_stop": n,
            "source_frame_step": 1,
            "frame_count": n,
            "segment_names": segments,
            "joint_names": joints,
            "quaternion_order": "wxyz",
            "rendering": {
                "type": "joint_skeleton_plus_segment_pose",
                "plot_pose_available": True,
            },
        },
        {
            "source_frame": np.arange(n, dtype=np.int32),
            "segment_pos": pos,
            "segment_quat": quat,
            "joint_pos": joint_pos,
        },
    )
    return out_path
