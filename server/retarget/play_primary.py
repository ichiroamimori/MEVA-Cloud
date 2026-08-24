# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import pickle
import time
from pathlib import Path

import mujoco
import mujoco.viewer
import numpy as np


KEY_SPACE = 32
KEY_RIGHT = 262
KEY_LEFT = 263


def normalize_quat(q: np.ndarray) -> np.ndarray:
    q = np.asarray(q, dtype=np.float64).reshape(4)
    n = np.linalg.norm(q)
    if not np.isfinite(n) or n <= 1e-12:
        raise ValueError(f"Invalid quaternion: {q}")
    return q / n


def load_motion(path: Path) -> dict:
    with path.open("rb") as f:
        data = pickle.load(f)

    required = ("root_pos", "root_rot", "dof_pos", "fps")
    for key in required:
        if key not in data:
            raise KeyError(f"PKL is missing required key: {key}")

    root_pos = np.asarray(data["root_pos"], dtype=np.float64)
    root_rot = np.asarray(data["root_rot"], dtype=np.float64)
    dof_pos = np.asarray(data["dof_pos"], dtype=np.float64)

    if root_pos.ndim != 2 or root_pos.shape[1] != 3:
        raise ValueError(f"root_pos must be (N,3), got {root_pos.shape}")
    if root_rot.shape != (root_pos.shape[0], 4):
        raise ValueError(f"root_rot must be (N,4), got {root_rot.shape}")
    if dof_pos.ndim != 2 or dof_pos.shape[0] != root_pos.shape[0]:
        raise ValueError(f"dof_pos shape mismatch: {dof_pos.shape}")

    return data


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Play a primary-retarget PKL in MuJoCo."
    )
    parser.add_argument(
        "pkl",
        nargs="?",
        type=Path,
        default=Path(
            "workspace/users/local_user/capsules/2606050001/"
            "retarget/g1_29dof/2608100001/primary.pkl"
        ),
    )
    parser.add_argument(
        "--xml",
        type=Path,
        default=Path("server/robots/unitree/g1/g1_29dof.xml"),
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=1.0,
        help="Playback speed multiplier. Example: 0.5, 1, 2",
    )
    parser.add_argument(
        "--no-loop",
        action="store_true",
        help="Stop after one playback.",
    )
    args = parser.parse_args()

    pkl_path = args.pkl.resolve()
    xml_path = args.xml.resolve()

    if not pkl_path.exists():
        raise FileNotFoundError(f"PKL not found: {pkl_path}")
    if not xml_path.exists():
        raise FileNotFoundError(f"MJCF not found: {xml_path}")

    motion = load_motion(pkl_path)
    root_pos = np.asarray(motion["root_pos"], dtype=np.float64)
    root_rot = np.asarray(motion["root_rot"], dtype=np.float64)
    dof_pos = np.asarray(motion["dof_pos"], dtype=np.float64)
    fps = float(motion["fps"])

    source_frame_indices = motion.get("source_frame_indices")
    if source_frame_indices is not None:
        source_frame_indices = np.asarray(source_frame_indices, dtype=np.int64)
        if source_frame_indices.shape != (root_pos.shape[0],):
            print(
                "WARNING: source_frame_indices shape mismatch; "
                "showing PKL frame only."
            )
            source_frame_indices = None

    root_rot_order = (
        motion.get("metadata", {}).get("root_rot_order", "xyzw")
    )

    model = mujoco.MjModel.from_xml_path(str(xml_path))
    data = mujoco.MjData(model)

    expected_nq = 7 + dof_pos.shape[1]
    if model.nq != expected_nq:
        raise ValueError(
            f"MJCF nq={model.nq}, but PKL requires 7 + {dof_pos.shape[1]} "
            f"= {expected_nq}. Check robot model / DoF order."
        )

    nframes = root_pos.shape[0]
    frame_dt = 1.0 / (fps * args.speed)

    state = {
        "paused": False,
        "index": 0,
        "step": 0,
    }

    def frame_label(i: int) -> str:
        if source_frame_indices is None:
            return f"PKL frame {i}"
        return (
            f"source frame {int(source_frame_indices[i])} "
            f"(PKL frame {i})"
        )

    def key_callback(keycode: int) -> None:
        if keycode == KEY_SPACE:
            state["paused"] = not state["paused"]
            status = "PAUSE" if state["paused"] else "RESUME"
            print(f"[{status}] {frame_label(state['index'])}")
        elif keycode == KEY_RIGHT:
            if state["paused"]:
                state["step"] = 1
        elif keycode == KEY_LEFT:
            if state["paused"]:
                state["step"] = -1

    def show_frame(i: int, viewer) -> None:
        data.qpos[0:3] = root_pos[i]

        q = normalize_quat(root_rot[i])
        if root_rot_order == "xyzw":
            x, y, z, w = q
            data.qpos[3:7] = [w, x, y, z]
        elif root_rot_order == "wxyz":
            data.qpos[3:7] = q
        else:
            raise ValueError(
                f"Unsupported root_rot_order: {root_rot_order}"
            )

        data.qpos[7:] = dof_pos[i]
        data.time = i / fps
        mujoco.mj_forward(model, data)
        viewer.sync()

    print(f"PKL : {pkl_path}")
    print(f"MJCF: {xml_path}")
    print(f"Frames: {nframes}")
    print(f"FPS: {fps}")
    print(f"Duration: {nframes / fps:.3f} s")
    print(f"root_rot order: {root_rot_order}")
    if source_frame_indices is not None:
        print(
            f"Source frames: {int(source_frame_indices[0])} "
            f".. {int(source_frame_indices[-1])}"
        )
    print("Controls: Space = Pause/Resume, Left/Right = step while paused")
    print("Close the MuJoCo viewer window to exit.")

    with mujoco.viewer.launch_passive(
        model,
        data,
        key_callback=key_callback,
    ) as viewer:
        show_frame(state["index"], viewer)

        while viewer.is_running():
            if state["paused"]:
                if state["step"] != 0:
                    new_index = state["index"] + state["step"]
                    new_index = max(0, min(nframes - 1, new_index))
                    if new_index != state["index"]:
                        state["index"] = new_index
                        show_frame(state["index"], viewer)
                        print(f"[STEP] {frame_label(state['index'])}")
                    state["step"] = 0
                else:
                    viewer.sync()
                    time.sleep(0.01)
                continue

            frame_start = time.perf_counter()
            show_frame(state["index"], viewer)

            next_index = state["index"] + 1
            if next_index >= nframes:
                if args.no_loop:
                    break
                next_index = 0
            state["index"] = next_index

            elapsed = time.perf_counter() - frame_start
            sleep_s = frame_dt - elapsed
            if sleep_s > 0:
                time.sleep(sleep_s)


if __name__ == "__main__":
    main()
