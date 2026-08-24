# -*- coding: utf-8 -*-
"""
MEVA viewer using:
- BVH HIERARCHY for the full skeleton shape / parent-child structure
- MEVA CSV q_gs quaternions for motion (default)
- Optional BVH MOTION playback for comparison

Usage:
    python server\\retarget\\play_meva.py ^
      workspace\\users\\local_user\\capsules\\2606050001\\meva\\sequence_hanya_nakahara_050626_205421.csv

The script automatically looks for a BVH with the same basename in the same folder.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import mujoco
import mujoco.viewer
import numpy as np


# MEVA's 18 displayed segments.
# BVH helper joints (e.g. Neck, End Site) are used for FK/offsets but not drawn.
MEVA_18 = [
    "Pelvis",
    "LumbarSpine",
    "Thoracic2",
    "Head",
    "LeftScapula",
    "LeftUpperArm",
    "LeftForearm",
    "LeftHand",
    "RightScapula",
    "RightUpperArm",
    "RightForearm",
    "RightHand",
    "LeftUpperLeg",
    "LeftLowerLeg",
    "LeftFoot",
    "RightUpperLeg",
    "RightLowerLeg",
    "RightFoot",
]
MEVA_18_CANON = {re.sub(r"[^a-z0-9]", "", s.lower()): s for s in MEVA_18}


# ============================================================
# Data structures
# ============================================================

@dataclass
class BvhJoint:
    name: str
    parent: Optional[str]
    offset: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=np.float64))
    channels: list[str] = field(default_factory=list)
    channel_start: int = 0
    children: list[str] = field(default_factory=list)
    is_end_site: bool = False


@dataclass
class BvhData:
    joints: dict[str, BvhJoint]
    root_name: str
    joint_order: list[str]
    motion: np.ndarray
    frame_time: float
    offset_scale: float


# ============================================================
# Quaternion helpers (wxyz)
# ============================================================

def normalize_quat(q) -> np.ndarray:
    q = np.asarray(q, dtype=np.float64).reshape(4)
    n = float(np.linalg.norm(q))
    if not np.isfinite(n) or n <= 1e-12:
        raise ValueError(f"Invalid quaternion: {q}")
    return q / n


def quat_mul(a, b) -> np.ndarray:
    out = np.empty(4, dtype=np.float64)
    mujoco.mju_mulQuat(out, normalize_quat(a), normalize_quat(b))
    return normalize_quat(out)


def quat_rotate(q, v) -> np.ndarray:
    out = np.empty(3, dtype=np.float64)
    mujoco.mju_rotVecQuat(out, np.asarray(v, dtype=np.float64), normalize_quat(q))
    return out


def axis_angle_quat(axis: str, angle_deg: float) -> np.ndarray:
    angle = math.radians(angle_deg)
    s = math.sin(angle / 2.0)
    c = math.cos(angle / 2.0)
    if axis == "X":
        return np.array([c, s, 0.0, 0.0], dtype=np.float64)
    if axis == "Y":
        return np.array([c, 0.0, s, 0.0], dtype=np.float64)
    if axis == "Z":
        return np.array([c, 0.0, 0.0, s], dtype=np.float64)
    raise ValueError(axis)


def bvh_rotation_quat(channels: list[str], values: np.ndarray) -> np.ndarray:
    q = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64)
    for ch, val in zip(channels, values):
        if ch.endswith("rotation"):
            axis = ch[0].upper()
            q = quat_mul(q, axis_angle_quat(axis, float(val)))
    return q


# ============================================================
# BVH parser
# ============================================================

TOKEN_RE = re.compile(r"\{|\}|[^\s{}]+")


def parse_bvh(path: Path) -> BvhData:
    text = path.read_text(encoding="utf-8", errors="replace")
    if "HIERARCHY" not in text or "MOTION" not in text:
        raise ValueError("Not a valid BVH file: HIERARCHY/MOTION missing.")

    hierarchy_text, motion_text = text.split("MOTION", 1)
    tokens = TOKEN_RE.findall(hierarchy_text)

    joints: dict[str, BvhJoint] = {}
    joint_order: list[str] = []
    total_channels = 0
    i = 0
    root_name = None
    end_counter = 0

    def parse_joint(parent: Optional[str], kind: str, name: str, idx: int) -> int:
        nonlocal total_channels, end_counter

        is_end = (kind == "End")
        if is_end:
            end_counter += 1
            internal_name = f"{parent}__EndSite{end_counter}"
        else:
            internal_name = name

        joint = BvhJoint(name=internal_name, parent=parent, is_end_site=is_end)
        joints[internal_name] = joint
        joint_order.append(internal_name)
        if parent is not None:
            joints[parent].children.append(internal_name)

        if tokens[idx] != "{":
            raise ValueError(f"Expected '{{' after {kind} {name}")
        idx += 1

        while idx < len(tokens):
            tok = tokens[idx]

            if tok == "}":
                return idx + 1

            if tok == "OFFSET":
                joint.offset = np.array(
                    [float(tokens[idx+1]), float(tokens[idx+2]), float(tokens[idx+3])],
                    dtype=np.float64,
                )
                idx += 4
                continue

            if tok == "CHANNELS":
                n = int(tokens[idx+1])
                joint.channels = tokens[idx+2:idx+2+n]
                joint.channel_start = total_channels
                total_channels += n
                idx += 2 + n
                continue

            if tok == "JOINT":
                child_name = tokens[idx+1]
                idx = parse_joint(internal_name, "JOINT", child_name, idx+2)
                continue

            if tok == "End":
                if tokens[idx+1] != "Site":
                    raise ValueError("Expected 'End Site'")
                idx = parse_joint(internal_name, "End", "Site", idx+2)
                continue

            idx += 1

        raise ValueError(f"Unclosed joint block: {internal_name}")

    while i < len(tokens):
        if tokens[i] == "ROOT":
            root_name = tokens[i+1]
            i = parse_joint(None, "ROOT", root_name, i+2)
            break
        i += 1

    if root_name is None:
        raise ValueError("BVH ROOT not found.")

    lines = [ln.strip() for ln in motion_text.splitlines() if ln.strip()]
    frames = None
    frame_time = None
    data_start = None
    for j, ln in enumerate(lines):
        low = ln.lower()
        if low.startswith("frames:"):
            frames = int(ln.split(":", 1)[1].strip())
        elif low.startswith("frame time:"):
            frame_time = float(ln.split(":", 1)[1].strip())
            data_start = j + 1
            break

    if frames is None or frame_time is None or data_start is None:
        raise ValueError("BVH MOTION header is incomplete.")

    motion_rows = []
    for ln in lines[data_start:data_start + frames]:
        vals = [float(x) for x in ln.split()]
        if len(vals) != total_channels:
            raise ValueError(
                f"BVH frame has {len(vals)} values, expected {total_channels}."
            )
        motion_rows.append(vals)

    motion = np.asarray(motion_rows, dtype=np.float64)

    # Heuristic: BVH skeleton offsets are often cm. If the skeleton is clearly
    # larger than meter-scale, convert to meters.
    max_abs_offset = max(
        float(np.max(np.abs(j.offset))) for j in joints.values()
    )
    offset_scale = 0.01 if max_abs_offset > 5.0 else 1.0

    return BvhData(
        joints=joints,
        root_name=root_name,
        joint_order=joint_order,
        motion=motion,
        frame_time=frame_time,
        offset_scale=offset_scale,
    )


# ============================================================
# CSV helpers
# ============================================================

def read_meva_csv(path: Path, header_row_1based: int):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        for _ in range(header_row_1based - 1):
            next(f, None)
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV header not found.")
        return list(reader.fieldnames), list(reader)


def canonical_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def find_csv_segment_names(fieldnames: list[str]) -> dict[str, str]:
    # Extract all segment names that actually have q_gs_w/x/y/z.
    found = {}
    fields = set(fieldnames)
    suffix = "_q_gs_w"
    for f in fieldnames:
        if f.endswith(suffix):
            seg = f[:-len(suffix)]
            required = [f"{seg}_q_gs_{c}" for c in "wxyz"]
            if all(k in fields for k in required):
                found[canonical_name(seg)] = seg
    return found


def segment_quat(row: dict[str, str], segment: str) -> np.ndarray:
    return normalize_quat([
        float(row[f"{segment}_q_gs_w"]),
        float(row[f"{segment}_q_gs_x"]),
        float(row[f"{segment}_q_gs_y"]),
        float(row[f"{segment}_q_gs_z"]),
    ])


def build_bvh_to_csv_mapping(
    bvh: BvhData,
    csv_segment_names: dict[str, str],
) -> dict[str, Optional[str]]:
    """
    MEVA BVH joint names encode the connection as ParentSegmentChildSegment,
    e.g. PelvisLeftUpperLeg or LeftUpperLegLeftLowerLeg.

    For CSV q_gs playback, such a BVH node is mapped to the CHILD segment:
      PelvisLeftUpperLeg          -> LeftUpperLeg
      LumbarSpineThoracic2       -> Thoracic2
      LeftUpperArmLeftForearm    -> LeftForearm

    ROOT Pelvis maps directly to Pelvis.
    """
    mapping: dict[str, Optional[str]] = {}

    # Prefer longer segment names first so suffix matching is unambiguous.
    csv_candidates = sorted(
        csv_segment_names.items(),
        key=lambda kv: len(kv[0]),
        reverse=True,
    )

    for name in bvh.joint_order:
        joint = bvh.joints[name]
        if joint.is_end_site:
            mapping[name] = None
            continue

        c = canonical_name(name)

        # Exact match, e.g. ROOT Pelvis.
        if c in csv_segment_names:
            mapping[name] = csv_segment_names[c]
            continue

        # MEVA BVH convention: ParentSegmentChildSegment.
        # Therefore the child segment is the suffix.
        matched = None
        for child_canon, child_original in csv_candidates:
            if c.endswith(child_canon):
                matched = child_original
                break

        mapping[name] = matched

    return mapping


# ============================================================
# Forward kinematics
# ============================================================

def csv_fk(
    bvh: BvhData,
    row: dict[str, str],
    mapping: dict[str, Optional[str]],
):
    pos: dict[str, np.ndarray] = {}
    rot: dict[str, np.ndarray] = {}

    root = bvh.root_name
    root_seg = mapping.get(root)
    if root_seg is None:
        raise KeyError(
            f"BVH root '{root}' did not map to a CSV segment. "
            "See the printed mapping table."
        )

    pos[root] = np.array([0.0, 0.0, 1.0], dtype=np.float64)
    rot[root] = segment_quat(row, root_seg)

    for name in bvh.joint_order:
        if name == root:
            continue
        j = bvh.joints[name]
        parent = j.parent
        if parent is None:
            continue

        # BVH OFFSET is expressed in the parent frame.
        pos[name] = pos[parent] + quat_rotate(
            rot[parent],
            j.offset * bvh.offset_scale,
        )

        mapped_seg = mapping.get(name)
        if mapped_seg is not None:
            rot[name] = segment_quat(row, mapped_seg)
        else:
            # End Sites / unmapped helper joints inherit parent orientation.
            rot[name] = rot[parent]

    return pos, rot


def bvh_fk(bvh: BvhData, frame: np.ndarray):
    pos: dict[str, np.ndarray] = {}
    rot: dict[str, np.ndarray] = {}

    for name in bvh.joint_order:
        j = bvh.joints[name]
        local_translation = j.offset * bvh.offset_scale
        local_rotation = np.array([1.0, 0.0, 0.0, 0.0])

        if j.channels:
            vals = frame[j.channel_start:j.channel_start + len(j.channels)]
            t = np.zeros(3, dtype=np.float64)
            for ch, val in zip(j.channels, vals):
                if ch == "Xposition":
                    t[0] = val * bvh.offset_scale
                elif ch == "Yposition":
                    t[1] = val * bvh.offset_scale
                elif ch == "Zposition":
                    t[2] = val * bvh.offset_scale
            local_translation = local_translation + t
            local_rotation = bvh_rotation_quat(j.channels, vals)

        if j.parent is None:
            pos[name] = np.array([0.0, 0.0, 1.0]) + local_translation
            rot[name] = local_rotation
        else:
            pos[name] = pos[j.parent] + quat_rotate(
                rot[j.parent], local_translation
            )
            rot[name] = quat_mul(rot[j.parent], local_rotation)

    return pos, rot


def visible_bvh_nodes(
    bvh: BvhData,
    mapping: dict[str, Optional[str]],
) -> dict[str, str]:
    """Return BVH joint -> MEVA segment for only the 18 MEVA segments."""
    out: dict[str, str] = {}
    for name in bvh.joint_order:
        seg = mapping.get(name)
        if seg is None:
            continue
        canon = canonical_name(seg)
        if canon in MEVA_18_CANON:
            out[name] = MEVA_18_CANON[canon]
    return out


def nearest_visible_ancestor(
    bvh: BvhData,
    name: str,
    visible: set[str],
) -> Optional[str]:
    """Skip helper joints and return the closest visible ancestor."""
    p = bvh.joints[name].parent
    while p is not None:
        if p in visible:
            return p
        p = bvh.joints[p].parent
    return None


# ============================================================
# Viewer
# ============================================================

def build_model():
    return mujoco.MjModel.from_xml_string("""
<mujoco model="meva_bvh_viewer">
  <option gravity="0 0 0"/>
  <visual>
    <headlight diffuse="0.8 0.8 0.8" ambient="0.35 0.35 0.35"/>
  </visual>
  <worldbody>
    <geom name="ground" type="plane" size="4 4 0.1"
          rgba="0.22 0.22 0.22 1"/>
    <geom name="origin" type="sphere" pos="0 0 0.02" size="0.025"
          rgba="1 1 0 1"/>
  </worldbody>
</mujoco>
""")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", type=Path)
    ap.add_argument("--bvh", type=Path, default=None)
    ap.add_argument("--mode", choices=["csv", "bvh"], default="csv")
    ap.add_argument("--header-row", type=int, default=8)
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--stop", type=int, default=300)
    ap.add_argument("--speed", type=float, default=0.5)
    ap.add_argument("--no-loop", action="store_true")
    args = ap.parse_args()

    csv_path = args.csv.resolve()
    bvh_path = (
        args.bvh.resolve()
        if args.bvh is not None
        else csv_path.with_suffix(".bvh")
    )

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")
    if not bvh_path.exists():
        raise FileNotFoundError(
            f"Same-name BVH not found: {bvh_path}\n"
            "Use --bvh <path> if the BVH has a different name."
        )

    bvh = parse_bvh(bvh_path)
    fieldnames, csv_rows = read_meva_csv(csv_path, args.header_row)
    csv_segments = find_csv_segment_names(fieldnames)
    mapping = build_bvh_to_csv_mapping(bvh, csv_segments)

    print("CSV :", csv_path)
    print("BVH :", bvh_path)
    print("Mode:", args.mode)
    print()
    print("BVH skeleton:")
    print(f"  joints incl. End Sites: {len(bvh.joint_order)}")
    print(f"  motion frames         : {len(bvh.motion)}")
    print(f"  frame time            : {bvh.frame_time:.6f} s")
    print(f"  offset scale          : {bvh.offset_scale}")
    print()
    print("BVH -> CSV mapping:")
    mapped_count = 0
    for name in bvh.joint_order:
        if bvh.joints[name].is_end_site:
            continue
        dst = mapping[name]
        if dst is not None:
            mapped_count += 1
        print(f"  {name:28s} -> {dst or '[unmapped]'}")
    print()
    print(f"Mapped BVH joints: {mapped_count}")
    print(f"CSV q_gs segments found: {len(csv_segments)}")

    visible_map = visible_bvh_nodes(bvh, mapping)
    visible_names = set(visible_map.keys())
    print(f"Displayed MEVA segments: {len(visible_map)} / 18")
    for bvh_name, meva_name in visible_map.items():
        print(f"  DISPLAY {meva_name:18s} <- {bvh_name}")
    missing_18 = [
        s for s in MEVA_18
        if canonical_name(s) not in {canonical_name(v) for v in visible_map.values()}
    ]
    if missing_18:
        print("Missing from 18-segment display:", ", ".join(missing_18))
    print()

    if args.mode == "csv":
        missing_required = [
            name for name in bvh.joint_order
            if not bvh.joints[name].is_end_site and mapping[name] is None
        ]
        if missing_required:
            print(
                "WARNING: Some BVH joints are not mapped to CSV q_gs. "
                "Their orientation will inherit the parent orientation."
            )

    n_frames = (
        len(csv_rows) if args.mode == "csv"
        else len(bvh.motion)
    )
    stop = min(args.stop, n_frames)
    indices = list(range(args.start, stop))
    if not indices:
        raise ValueError("No frames selected.")

    fps = (
        100.0 if args.mode == "csv"
        else 1.0 / bvh.frame_time
    )

    model = build_model()
    data = mujoco.MjData(model)

    # Passive viewer playback state. MuJoCo itself does not know the source CSV
    # frame number, so the script keeps it explicitly.
    state = {
        "paused": False,
        "step": 0,          # -1: one frame back, +1: one frame forward
        "frame": indices[0],
    }

    def key_callback(keycode):
        # Space: pause / resume. GLFW arrow key codes: Left=263, Right=262.
        if keycode == 32:
            state["paused"] = not state["paused"]
            status = "PAUSE" if state["paused"] else "PLAY"
            print(f"[{status}] frame {state['frame']}")
        elif keycode == 262 and state["paused"]:
            state["step"] = +1
        elif keycode == 263 and state["paused"]:
            state["step"] = -1

    print("Viewer controls: Space = pause/resume, Left/Right = 1-frame step while paused")

    with mujoco.viewer.launch_passive(
        model, data, key_callback=key_callback
    ) as viewer:
        viewer.cam.lookat[:] = [0.0, 0.0, 0.95]
        viewer.cam.distance = 2.8
        viewer.cam.azimuth = 135
        viewer.cam.elevation = -12

        cursor = 0
        while viewer.is_running():
            frame_idx = indices[cursor]
            state["frame"] = frame_idx
            t0 = time.perf_counter()

            if args.mode == "csv":
                pos, rot = csv_fk(
                    bvh,
                    csv_rows[frame_idx],
                    mapping,
                )
            else:
                pos, rot = bvh_fk(
                    bvh,
                    bvh.motion[frame_idx],
                )

            # Keep root horizontally centered so the skeleton stays visible.
            root_xy = pos[bvh.root_name].copy()
            root_xy[2] = 0.0
            for name in pos:
                pos[name] = pos[name] - root_xy

            with viewer.lock():
                viewer.user_scn.ngeom = 0

                def add_line(a, b, rgba, width=0.012):
                    i = viewer.user_scn.ngeom
                    if i >= viewer.user_scn.maxgeom:
                        return
                    g = viewer.user_scn.geoms[i]
                    mujoco.mjv_initGeom(
                        g,
                        mujoco.mjtGeom.mjGEOM_CAPSULE,
                        np.zeros(3),
                        np.zeros(3),
                        np.eye(3).reshape(-1),
                        np.asarray(rgba, dtype=np.float32),
                    )
                    mujoco.mjv_connector(
                        g,
                        mujoco.mjtGeom.mjGEOM_CAPSULE,
                        width,
                        np.asarray(a, dtype=np.float64),
                        np.asarray(b, dtype=np.float64),
                    )
                    viewer.user_scn.ngeom += 1

                def add_sphere(p, rgba, radius=0.022):
                    i = viewer.user_scn.ngeom
                    if i >= viewer.user_scn.maxgeom:
                        return
                    g = viewer.user_scn.geoms[i]
                    mujoco.mjv_initGeom(
                        g,
                        mujoco.mjtGeom.mjGEOM_SPHERE,
                        np.array([radius, radius, radius]),
                        np.asarray(p, dtype=np.float64),
                        np.eye(3).reshape(-1),
                        np.asarray(rgba, dtype=np.float32),
                    )
                    viewer.user_scn.ngeom += 1

                # Draw only MEVA's 18 segments. Hidden BVH helper joints
                # still participate in FK, so their offsets remain respected.
                for name in visible_names:
                    if name not in pos:
                        continue

                    meva_name = visible_map[name]
                    add_sphere(pos[name], [0.95, 0.95, 0.95, 1.0], 0.022)

                    parent = nearest_visible_ancestor(bvh, name, visible_names)
                    if parent is not None and parent in pos:
                        lname = meva_name.lower()
                        color = [0.2, 0.8, 0.9, 1.0]
                        if "left" in lname:
                            color = [0.2, 0.9, 0.3, 1.0]
                        elif "right" in lname:
                            color = [0.95, 0.3, 0.3, 1.0]
                        add_line(pos[parent], pos[name], color)

                # Show root local axes.
                root = bvh.root_name
                p0 = pos[root]
                q0 = rot[root]
                for axis, color in [
                    ([1, 0, 0], [1, 0, 0, 1]),
                    ([0, 1, 0], [0, 1, 0, 1]),
                    ([0, 0, 1], [0, 0, 1, 1]),
                ]:
                    add_line(
                        p0,
                        p0 + 0.15 * quat_rotate(q0, axis),
                        color,
                        0.005,
                    )

            # Store source time as MuJoCo time. At 100 fps, frame N corresponds
            # to N / 100 seconds from the beginning of the CSV.
            data.time = frame_idx / fps
            mujoco.mj_forward(model, data)
            viewer.sync()

            if state["paused"]:
                step = state["step"]
                if step:
                    state["step"] = 0
                    cursor = max(0, min(len(indices) - 1, cursor + step))
                    state["frame"] = indices[cursor]
                    print(f"[STEP] frame {state['frame']}")
                else:
                    time.sleep(0.01)
                continue

            cursor += 1
            if cursor >= len(indices):
                if args.no_loop:
                    break
                cursor = 0

            target_dt = 1.0 / max(1e-6, fps * args.speed)
            elapsed = time.perf_counter() - t0
            if elapsed < target_dt:
                time.sleep(target_dt - elapsed)


if __name__ == "__main__":
    main()
