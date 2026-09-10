"""Standalone MuJoCo robot and motion viewer support.

The viewer deliberately resolves Robot assets through the Robot Registry.  A
motion file is optional: without one the registered initial pose is shown;
with one the same model is driven by the GMR-compatible motion arrays.
"""
from __future__ import annotations

import math
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import mujoco
import mujoco.viewer
import numpy as np

from server.robot_registry import RobotVariant, repository_root, resolve_variant
from server.retarget.motion_io import load_motion
from server.retarget.robot_runtime_definition import load_robot_runtime_definition


RootRotationOrder = Literal["xyzw", "wxyz"]
AxesMode = Literal["off", "selected", "all"]

KEY_SPACE = 32
KEY_C = 67
KEY_L = 76
KEY_M = 77
KEY_T = 84
KEY_ENTER = 257
KEY_DOWN = 264
KEY_UP = 265
KEY_KEYPAD_ENTER = 335
KEY_RIGHT = 262
KEY_LEFT = 263


@dataclass(frozen=True)
class MotionData:
    """Validated motion arrays used by the native MuJoCo viewer."""

    path: Path
    fps: float
    root_pos: np.ndarray
    root_rot: np.ndarray
    dof_pos: np.ndarray
    root_rot_order: RootRotationOrder
    joint_names: tuple[str, ...] | None
    source_frame_indices: np.ndarray | None

    @property
    def frame_count(self) -> int:
        return int(self.root_pos.shape[0])


@dataclass(frozen=True)
class LandmarkCandidate:
    """Model-derived point that can be inspected during Robot installation."""

    label: str
    kind: Literal["body_origin", "body_com", "subtree_com", "midpoint"]
    body_ids: tuple[int, ...]
    reference_body_id: int
    detail: str


@dataclass
class RobotViewerModel:
    """A registered Robot, its initial pose, and output Joint addressing."""

    record: RobotVariant
    model: mujoco.MjModel
    data: mujoco.MjData
    initial_qpos: np.ndarray
    output_joint_names: tuple[str, ...]
    output_qpos_addresses: tuple[int, ...]
    free_qpos_address: int | None
    root_body_id: int

    @classmethod
    def from_variant(
        cls,
        variant_id: str,
        *,
        manufacturer_id: str | None = None,
        robot_id: str | None = None,
        root: Path | None = None,
    ) -> "RobotViewerModel":
        repo = (root or repository_root()).resolve()
        record = resolve_variant(
            variant_id,
            manufacturer_id=manufacturer_id,
            robot_id=robot_id,
            root=repo,
        )
        runtime_definition = load_robot_runtime_definition(
            repo, record.runtime_robot(repo)
        )
        model = runtime_definition.model
        data = mujoco.MjData(model)
        data.qpos[:] = runtime_definition.initial_qpos
        mujoco.mj_forward(model, data)
        initial_qpos = runtime_definition.initial_qpos.copy()

        names, addresses = _output_joint_addresses(model, record)
        manifest_dof = int(record.variant["dof"])
        if len(names) != manifest_dof:
            raise ValueError(
                "Robot output Joint count does not match manifest DoF: "
                f"variant={record.variant_id}, joints={len(names)}, "
                f"manifest={manifest_dof}"
            )

        free_ids = [
            joint_id
            for joint_id in range(model.njnt)
            if int(model.jnt_type[joint_id])
            == int(mujoco.mjtJoint.mjJNT_FREE)
        ]
        if len(free_ids) > 1:
            raise ValueError(
                f"Robot Viewer supports at most one free Joint, got {len(free_ids)}"
            )
        free_address = (
            int(model.jnt_qposadr[free_ids[0]]) if free_ids else None
        )
        root_body_id = mujoco.mj_name2id(
            model,
            mujoco.mjtObj.mjOBJ_BODY,
            runtime_definition.root_body,
        )
        if root_body_id < 0:
            raise ValueError(
                "Robot manifest root_body is not present in the Runtime Model: "
                f"{record.variant['root_body']}"
            )
        return cls(
            record=record,
            model=model,
            data=data,
            initial_qpos=initial_qpos,
            output_joint_names=names,
            output_qpos_addresses=addresses,
            free_qpos_address=free_address,
            root_body_id=int(root_body_id),
        )

    def validate_motion(self, motion: MotionData) -> None:
        expected = len(self.output_joint_names)
        actual = int(motion.dof_pos.shape[1])
        if actual != expected:
            raise ValueError(
                "Motion DoF does not match Robot Variant: "
                f"variant={self.record.variant_id}, motion={actual}, "
                f"expected={expected}"
            )
        if self.free_qpos_address is None:
            raise ValueError(
                "The root_pos/root_rot motion contract requires a floating-base "
                f"Robot: {self.record.variant_id}"
            )
        if motion.joint_names is not None:
            if motion.joint_names != self.output_joint_names:
                raise ValueError(
                    "Motion joint_names do not match the registered "
                    f"output_joint_order for {self.record.variant_id}"
                )

    def reset_initial_pose(self) -> None:
        self.data.qpos[:] = self.initial_qpos
        self.data.qvel[:] = 0.0
        if self.data.act is not None:
            self.data.act[:] = 0.0
        self.data.time = 0.0
        mujoco.mj_forward(self.model, self.data)

    def apply_motion_frame(self, motion: MotionData, frame: int) -> None:
        self.data.qpos[:] = self.initial_qpos
        self.data.qvel[:] = 0.0
        free = self.free_qpos_address
        if free is None:  # validate_motion produces the user-facing error.
            raise ValueError("Motion playback requires a free Joint")
        self.data.qpos[free : free + 3] = motion.root_pos[frame]
        rotation = _normalised_quaternion(motion.root_rot[frame])
        if motion.root_rot_order == "xyzw":
            rotation = rotation[[3, 0, 1, 2]]
        self.data.qpos[free + 3 : free + 7] = rotation
        for column, address in enumerate(self.output_qpos_addresses):
            self.data.qpos[address] = motion.dof_pos[frame, column]
        self.data.time = frame / motion.fps
        mujoco.mj_forward(self.model, self.data)


def load_viewer_motion(
    path: Path,
    *,
    root_rot_order: RootRotationOrder | None = None,
) -> MotionData:
    """Load and validate canonical NPZ or trusted GMR-compatible PKL motion."""
    resolved = path.resolve()
    if not resolved.is_file():
        raise FileNotFoundError(f"Motion file not found: {resolved}")
    if resolved.suffix.lower() not in {".pkl", ".npz"}:
        raise ValueError("Motion file must use .pkl or .npz")
    raw = load_motion(resolved)
    required = ("fps", "root_pos", "root_rot", "dof_pos")
    missing = [key for key in required if key not in raw]
    if missing:
        raise KeyError(f"Motion is missing required keys: {missing}")

    root_pos = np.asarray(raw["root_pos"], dtype=np.float64)
    root_rot = np.asarray(raw["root_rot"], dtype=np.float64)
    dof_pos = np.asarray(raw["dof_pos"], dtype=np.float64)
    if root_pos.ndim != 2 or root_pos.shape[1] != 3:
        raise ValueError(f"root_pos must have shape (N, 3), got {root_pos.shape}")
    frames = int(root_pos.shape[0])
    if frames <= 0:
        raise ValueError("Motion must contain at least one frame")
    if root_rot.shape != (frames, 4):
        raise ValueError(f"root_rot must have shape (N, 4), got {root_rot.shape}")
    if dof_pos.ndim != 2 or dof_pos.shape[0] != frames:
        raise ValueError(
            f"dof_pos must have shape (N, DoF), got {dof_pos.shape}"
        )
    for name, values in (
        ("root_pos", root_pos),
        ("root_rot", root_rot),
        ("dof_pos", dof_pos),
    ):
        if not np.all(np.isfinite(values)):
            raise ValueError(f"{name} contains NaN or infinite values")
    quaternion_norms = np.linalg.norm(root_rot, axis=1)
    if np.any(quaternion_norms <= 1e-12):
        frame = int(np.flatnonzero(quaternion_norms <= 1e-12)[0])
        raise ValueError(f"root_rot contains a zero quaternion at frame {frame}")

    fps = float(raw["fps"])
    if not math.isfinite(fps) or fps <= 0.0:
        raise ValueError(f"fps must be finite and positive, got {fps}")
    metadata = raw.get("metadata")
    metadata_order = metadata.get("root_rot_order") if isinstance(metadata, dict) else None
    order_value = str(
        root_rot_order
        or raw.get("root_rot_order")
        or metadata_order
        or "xyzw"
    ).lower()
    if order_value not in {"xyzw", "wxyz"}:
        raise ValueError(f"Unsupported root_rot_order: {order_value}")

    joint_names_value = raw.get("joint_names")
    joint_names = None
    if joint_names_value is not None:
        flattened = np.asarray(joint_names_value).reshape(-1)
        joint_names = tuple(str(value) for value in flattened.tolist())
        if len(joint_names) != dof_pos.shape[1]:
            raise ValueError(
                "joint_names count does not match dof_pos columns: "
                f"names={len(joint_names)}, dof={dof_pos.shape[1]}"
            )

    source_value = raw.get("source_frame_indices")
    if source_value is None:
        source_value = raw.get("source_frame_nearest")
    source_frames = None
    if source_value is not None:
        source_frames = np.asarray(source_value, dtype=np.int64)
        if source_frames.shape != (frames,):
            raise ValueError(
                "source frame indices must have shape (N,), got "
                f"{source_frames.shape}"
            )
    return MotionData(
        path=resolved,
        fps=fps,
        root_pos=root_pos,
        root_rot=root_rot,
        dof_pos=dof_pos,
        root_rot_order=order_value,  # type: ignore[arg-type]
        joint_names=joint_names,
        source_frame_indices=source_frames,
    )


def _maximize_current_process_window() -> bool:
    """Maximize this process's visible native Viewer window on Windows."""
    if sys.platform != "win32":
        return False
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.WinDLL("user32", use_last_error=True)
    process_id = os.getpid()
    found: list[int] = []
    callback_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

    def visit(window: int, _parameter: int) -> bool:
        owner = wintypes.DWORD()
        user32.GetWindowThreadProcessId(window, ctypes.byref(owner))
        if owner.value == process_id and user32.IsWindowVisible(window):
            found.append(window)
            return False
        return True

    callback = callback_type(visit)
    deadline = time.monotonic() + 3.0
    while time.monotonic() < deadline:
        found.clear()
        user32.EnumWindows(callback, 0)
        if found:
            user32.ShowWindow(found[0], 3)  # SW_MAXIMIZE
            return True
        time.sleep(0.05)
    return False


def _motion_frame_for_elapsed(
    origin_frame: int,
    elapsed_s: float,
    *,
    frame_count: int,
    fps: float,
    speed: float,
    loop: bool,
) -> tuple[int, bool]:
    """Return the wall-clock motion frame and whether playback reached its end."""
    unwrapped = origin_frame + int(max(0.0, elapsed_s) * fps * speed)
    if unwrapped < frame_count:
        return unwrapped, False
    if loop:
        return unwrapped % frame_count, False
    return frame_count - 1, True


def run_native_viewer(
    robot: RobotViewerModel,
    motion: MotionData | None = None,
    *,
    speed: float = 1.0,
    loop: bool = True,
    axes: AxesMode = "off",
    axis_length_m: float | None = None,
    show_labels: bool = False,
    start_paused: bool = False,
    maximized: bool = False,
) -> None:
    """Open MuJoCo's interactive native viewer."""
    if not math.isfinite(speed) or speed <= 0.0:
        raise ValueError(f"Playback speed must be positive, got {speed}")
    if axes not in {"off", "selected", "all"}:
        raise ValueError(f"Unsupported axes mode: {axes}")
    if axis_length_m is None:
        axis_length_m = max(0.08, min(0.3, float(robot.model.stat.extent) * 0.12))
    if not math.isfinite(axis_length_m) or axis_length_m <= 0.0:
        raise ValueError(f"Axis length must be positive, got {axis_length_m}")
    if motion is not None:
        robot.validate_motion(motion)
        robot.apply_motion_frame(motion, 0)
    else:
        robot.reset_initial_pose()

    body_ids = tuple(range(1, robot.model.nbody))
    body_names = tuple(_body_name(robot.model, body_id) for body_id in body_ids)
    selection_body_ids = (0,) + body_ids
    selection_names = ("No select",) + body_names
    landmark_candidates = _landmark_candidates(robot)
    original_geom_rgba = np.asarray(robot.model.geom_rgba, dtype=np.float32).copy()
    state: dict[str, Any] = {
        "paused": motion is None or bool(start_paused),
        "frame": 0,
        "step": 0,
        "axes": axes,
        "selected": 0,
        "cursor": 0,
        "selection_pending": True,
        "link_list": bool(show_labels),
        "landmark_list": False,
        "active_list": "links",
        "landmark_cursor": 0,
        "landmark_selected": 0,
        "camera_mode": "free" if motion is None else "tracking",
        "camera_dirty": True,
        "transparent": False,
        "appearance_dirty": True,
        "dirty": True,
        "playback_origin_frame": 0,
        "playback_origin_time": time.perf_counter(),
    }

    def selected_label() -> str:
        return selection_names[int(state["selected"])]

    def cursor_label() -> str:
        return selection_names[int(state["cursor"])]

    def frame_label() -> str:
        if motion is None:
            return "initial pose"
        frame = int(state["frame"])
        if motion.source_frame_indices is None:
            return f"motion frame {frame}"
        return (
            f"source frame {int(motion.source_frame_indices[frame])} "
            f"(motion frame {frame})"
        )

    def key_callback(keycode: int) -> None:
        if keycode == KEY_SPACE and motion is not None:
            state["paused"] = not state["paused"]
            if not state["paused"]:
                state["playback_origin_frame"] = int(state["frame"])
                state["playback_origin_time"] = time.perf_counter()
            print(f"[{'PAUSE' if state['paused'] else 'PLAY'}] {frame_label()}")
        elif keycode == KEY_RIGHT and motion is not None and state["paused"]:
            state["step"] = 1
        elif keycode == KEY_LEFT and motion is not None and state["paused"]:
            state["step"] = -1
        elif keycode in {KEY_DOWN, KEY_UP}:
            direction = 1 if keycode == KEY_DOWN else -1
            if state["active_list"] == "landmarks" and landmark_candidates:
                state["landmark_cursor"] = (
                    int(state["landmark_cursor"]) + direction
                ) % len(landmark_candidates)
                print(
                    "[LANDMARK CURSOR] "
                    f"{landmark_candidates[int(state['landmark_cursor'])].label}"
                )
            else:
                state["cursor"] = (
                    int(state["cursor"]) + direction
                ) % len(selection_names)
                print(f"[CURSOR] {cursor_label()}")
            state["dirty"] = True
        elif keycode in {KEY_ENTER, KEY_KEYPAD_ENTER}:
            if state["active_list"] == "landmarks" and landmark_candidates:
                state["landmark_selected"] = int(state["landmark_cursor"])
                candidate = landmark_candidates[int(state["landmark_selected"])]
                position = _landmark_world_position(robot, candidate)
                local = _world_to_body_local(
                    robot, candidate.reference_body_id, position
                )
                print(
                    f"[LANDMARK] {candidate.label}: world={position.tolist()}, "
                    f"reference_body={_body_name(robot.model, candidate.reference_body_id)}, "
                    f"local={local.tolist()} ({candidate.detail})"
                )
            else:
                state["selected"] = int(state["cursor"])
                state["axes"] = (
                    "off" if int(state["selected"]) == 0 else "selected"
                )
                state["selection_pending"] = True
                print(f"[LINK] {selected_label()}")
            state["dirty"] = True
        elif keycode == KEY_L:
            if state["link_list"] and state["active_list"] == "links":
                state["link_list"] = False
                state["active_list"] = (
                    "landmarks" if state["landmark_list"] else "links"
                )
            else:
                state["link_list"] = True
                state["active_list"] = "links"
            state["dirty"] = True
            print(f"[LINK LIST] {'on' if state['link_list'] else 'off'}")
        elif keycode == KEY_M:
            if state["landmark_list"] and state["active_list"] == "landmarks":
                state["landmark_list"] = False
                state["active_list"] = "links"
            else:
                state["landmark_list"] = True
                state["active_list"] = "landmarks"
            state["dirty"] = True
            print(
                f"[LANDMARK LIST] {'on' if state['landmark_list'] else 'off'}"
            )
        elif keycode == KEY_C:
            state["camera_mode"] = (
                "tracking" if state["camera_mode"] == "free" else "free"
            )
            state["camera_dirty"] = True
            print(f"[CAMERA] {str(state['camera_mode']).upper()}")
        elif keycode == KEY_T:
            state["transparent"] = not state["transparent"]
            state["appearance_dirty"] = True
            state["dirty"] = True
            print(
                f"[ROBOT SHELL] {'30% opacity' if state['transparent'] else 'normal'}"
            )

    print(
        "Robot: "
        f"{robot.record.manufacturer_name} / {robot.record.robot_name} / "
        f"{robot.record.variant['name']}"
    )
    print(f"Model: {robot.record.model_path}")
    print(f"Output Joints: {len(robot.output_joint_names)}")
    if motion is None:
        print("Motion: none (registered initial pose)")
    else:
        print(f"Motion: {motion.path}")
        print(
            f"Frames: {motion.frame_count}, FPS: {motion.fps:g}, "
            f"Duration: {motion.frame_count / motion.fps:.3f} s"
        )
        print(f"Root quaternion order: {motion.root_rot_order}")
    print("Controls:")
    print("  Mouse       Rotate / zoom / pan using the MuJoCo viewer")
    print("  Space       Play / pause (motion mode)")
    print("  Left/Right  Step one frame while paused")
    print("  Up/Down     Move cursor in the Link list")
    print("  Enter       Select Link + show axes (No select clears both)")
    print("  Double-click  Select a Link + show its axes in the 3D view")
    print("  L           Toggle the Link list in the 3D view")
    print("  M           Toggle the Landmark candidate list (left side)")
    print("  C           Toggle FREE / TRACKING camera")
    print("  T           Toggle Robot shell opacity (100% / 30%)")
    if sys.platform == "win32":
        print("  Alt+Left drag  Pan camera (touchpad alternative)")
    print(f"Selected Link: {selected_label()}")

    with mujoco.viewer.launch_passive(
        robot.model,
        robot.data,
        key_callback=key_callback,
        show_left_ui=False,
        show_right_ui=False,
    ) as viewer:
        if maximized:
            _maximize_current_process_window()
        viewer.cam.type = (
            mujoco.mjtCamera.mjCAMERA_FREE
            if state["camera_mode"] == "free"
            else mujoco.mjtCamera.mjCAMERA_TRACKING
        )
        viewer.cam.trackbodyid = (
            -1 if state["camera_mode"] == "free" else robot.root_body_id
        )
        # Model stat.center describes the compiled reference model and can be far
        # from a motion's first root position. Frame the pose actually displayed.
        viewer.cam.lookat[:] = robot.data.subtree_com[robot.root_body_id]
        viewer.cam.distance = max(0.5, float(robot.model.stat.extent) * 1.7)
        viewer.cam.azimuth = 135.0
        viewer.cam.elevation = -15.0

        # Window creation/maximization can deliver transient input and can take
        # several seconds on a large display. Start playback from frame zero only
        # after that work is complete.
        state["paused"] = motion is None or bool(start_paused)
        state["playback_origin_frame"] = int(state["frame"])
        state["playback_origin_time"] = time.perf_counter()

        last_frame = -1
        alt_pan = _WindowsAltLeftPan(viewer) if sys.platform == "win32" else None
        while viewer.is_running():
            if state["camera_dirty"]:
                with viewer.lock():
                    viewer.cam.type = (
                        mujoco.mjtCamera.mjCAMERA_FREE
                        if state["camera_mode"] == "free"
                        else mujoco.mjtCamera.mjCAMERA_TRACKING
                    )
                    viewer.cam.trackbodyid = (
                        -1
                        if state["camera_mode"] == "free"
                        else robot.root_body_id
                    )
                state["camera_dirty"] = False
            if motion is not None:
                if not state["paused"]:
                    frame, ended = _motion_frame_for_elapsed(
                        int(state["playback_origin_frame"]),
                        time.perf_counter() - float(state["playback_origin_time"]),
                        frame_count=motion.frame_count,
                        fps=motion.fps,
                        speed=speed,
                        loop=loop,
                    )
                    state["frame"] = frame
                    if ended:
                        state["paused"] = True
                        print(f"[END] {frame_label()}")
                frame = int(state["frame"])
                if state["paused"] and int(state["step"]):
                    frame = max(
                        0,
                        min(motion.frame_count - 1, frame + int(state["step"])),
                    )
                    state["frame"] = frame
                    state["step"] = 0
                    state["dirty"] = True
                    print(f"[STEP] {frame_label()}")
                if frame != last_frame:
                    with viewer.lock():
                        robot.apply_motion_frame(motion, frame)
                    last_frame = frame
                    state["dirty"] = True

            if state["dirty"]:
                with viewer.lock():
                    if state["appearance_dirty"]:
                        robot.model.geom_rgba[:] = original_geom_rgba
                        if state["transparent"]:
                            robot.model.geom_rgba[:, 3] = np.minimum(
                                robot.model.geom_rgba[:, 3], 0.6
                            )
                        viewer.opt.flags[
                            mujoco.mjtVisFlag.mjVIS_TRANSPARENT
                        ] = bool(state["transparent"])
                        state["appearance_dirty"] = False
                    viewer.opt.label = mujoco.mjtLabel.mjLABEL_NONE
                    if state["selection_pending"]:
                        viewer.perturb.select = selection_body_ids[
                            int(state["selected"])
                        ]
                        state["selection_pending"] = False
                    _update_axis_geometries(
                        viewer,
                        robot,
                        mode=state["axes"],
                        selected_body_id=selection_body_ids[
                            int(state["selected"])
                        ],
                        axis_length_m=float(axis_length_m),
                        landmark=(
                            landmark_candidates[int(state["landmark_selected"])]
                            if state["landmark_list"] and landmark_candidates
                            else None
                        ),
                    )
                texts = []
                if state["link_list"]:
                    texts.append(
                        (
                            mujoco.mjtFont.mjFONT_NORMAL,
                            mujoco.mjtGridPos.mjGRID_TOPRIGHT,
                            _link_list_text(
                                selection_names,
                                cursor_index=int(state["cursor"]),
                                selected_index=int(state["selected"]),
                                active=state["active_list"] == "links",
                            ),
                            "",
                        )
                    )
                if state["landmark_list"]:
                    texts.append(
                        (
                            mujoco.mjtFont.mjFONT_NORMAL,
                            mujoco.mjtGridPos.mjGRID_TOPLEFT,
                            _landmark_list_text(
                                landmark_candidates,
                                cursor_index=int(state["landmark_cursor"]),
                                selected_index=int(state["landmark_selected"]),
                                active=state["active_list"] == "landmarks",
                            ),
                            "",
                        )
                    )
                if texts:
                    viewer.set_texts(texts)
                else:
                    viewer.clear_texts()
                state["dirty"] = False
            viewer.sync()
            if alt_pan is not None and state["camera_mode"] == "free":
                alt_pan.update()

            # MuJoCo updates perturb.select when a Body is double-clicked.
            viewer_selected = int(viewer.perturb.select)
            if viewer_selected < 0 or viewer_selected not in selection_body_ids:
                viewer_selected = 0
            selected_entry = selection_body_ids.index(viewer_selected)
            if selected_entry != int(state["selected"]):
                state["selected"] = selected_entry
                state["cursor"] = selected_entry
                state["axes"] = "off" if selected_entry == 0 else "selected"
                state["dirty"] = True
                print(f"[LINK] {selected_label()} (3D selection)")

            if motion is None or state["paused"]:
                time.sleep(0.01)
                continue
            rate = motion.fps * speed
            elapsed = time.perf_counter() - float(state["playback_origin_time"])
            completed_intervals = int(max(0.0, elapsed) * rate)
            next_deadline = (
                float(state["playback_origin_time"])
                + (completed_intervals + 1) / rate
            )
            delay = next_deadline - time.perf_counter()
            if delay > 0.0:
                time.sleep(delay)


def _apply_registered_initial_pose(
    record: RobotVariant,
    model: mujoco.MjModel,
    data: mujoco.MjData,
) -> None:
    initial = record.variant.get("initial_pose", {"type": "model_default"})
    kind = str(initial.get("type") or "model_default")
    if kind == "model_default":
        mujoco.mj_resetData(model, data)
    elif kind == "keyframe":
        name = str(initial.get("name") or "")
        key_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_KEY, name)
        if key_id < 0:
            raise ValueError(
                f"Initial-pose keyframe not found in Runtime Model: {name}"
            )
        mujoco.mj_resetDataKeyframe(model, data, int(key_id))
    else:
        raise ValueError(f"Unsupported registered initial_pose type: {kind}")
    mujoco.mj_forward(model, data)


def _output_joint_addresses(
    model: mujoco.MjModel,
    record: RobotVariant,
) -> tuple[tuple[str, ...], tuple[int, ...]]:
    configured = record.variant.get("output_joint_order", "model_hinge_order")
    scalar_by_name: dict[str, int] = {}
    hinge_names: list[str] = []
    for joint_id in range(model.njnt):
        kind = int(model.jnt_type[joint_id])
        if kind not in {
            int(mujoco.mjtJoint.mjJNT_HINGE),
            int(mujoco.mjtJoint.mjJNT_SLIDE),
        }:
            continue
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, joint_id)
        if not name:
            raise ValueError(f"Output Joint has no name: joint_id={joint_id}")
        scalar_by_name[str(name)] = int(model.jnt_qposadr[joint_id])
        if kind == int(mujoco.mjtJoint.mjJNT_HINGE):
            hinge_names.append(str(name))
    if configured == "model_hinge_order":
        names = tuple(hinge_names)
    else:
        names = tuple(str(name) for name in configured)
    missing = [name for name in names if name not in scalar_by_name]
    if missing:
        raise ValueError(
            "output_joint_order references missing or non-scalar Joints: "
            f"{missing}"
        )
    if len(set(names)) != len(names):
        raise ValueError("output_joint_order contains duplicate Joint names")
    return names, tuple(scalar_by_name[name] for name in names)


def _normalised_quaternion(value: np.ndarray) -> np.ndarray:
    quaternion = np.asarray(value, dtype=np.float64).reshape(4)
    norm = float(np.linalg.norm(quaternion))
    if not math.isfinite(norm) or norm <= 1e-12:
        raise ValueError(f"Invalid quaternion: {quaternion}")
    return quaternion / norm


def _body_name(model: mujoco.MjModel, body_id: int) -> str:
    return (
        mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, body_id)
        or f"body_{body_id}"
    )


def _landmark_candidates(
    robot: RobotViewerModel,
) -> tuple[LandmarkCandidate, ...]:
    """Create inspectable, model-derived pelvis landmark candidates."""
    root_id = int(robot.root_body_id)
    candidates = [
        LandmarkCandidate(
            label=f"{_body_name(robot.model, root_id)} origin",
            kind="body_origin",
            body_ids=(root_id,),
            reference_body_id=root_id,
            detail="Root Body coordinate origin",
        ),
        LandmarkCandidate(
            label=f"{_body_name(robot.model, root_id)} body COM",
            kind="body_com",
            body_ids=(root_id,),
            reference_body_id=root_id,
            detail="Root Body inertial center of mass (not symmetry-corrected)",
        ),
        LandmarkCandidate(
            label="Whole robot COM",
            kind="subtree_com",
            body_ids=(root_id,),
            reference_body_id=root_id,
            detail="Mass center of the complete root subtree",
        ),
    ]

    body_names = {
        _body_name(robot.model, body_id): body_id
        for body_id in range(1, robot.model.nbody)
    }
    lower_names = {name.lower(): (name, body_id) for name, body_id in body_names.items()}
    seen_pairs: set[tuple[int, int]] = set()
    for lower_name, (name, body_id) in lower_names.items():
        if "hip" not in lower_name or "left" not in lower_name:
            continue
        right_key = lower_name.replace("left", "right", 1)
        right_entry = lower_names.get(right_key)
        if right_entry is None:
            continue
        right_name, right_id = right_entry
        pair = (min(body_id, right_id), max(body_id, right_id))
        if pair in seen_pairs:
            continue
        seen_pairs.add(pair)
        label_base = name
        for prefix in ("Left_", "left_", "LEFT_"):
            if label_base.startswith(prefix):
                label_base = label_base[len(prefix) :]
                break
        candidates.append(
            LandmarkCandidate(
                label=f"{label_base} L/R midpoint",
                kind="midpoint",
                body_ids=(body_id, right_id),
                reference_body_id=root_id,
                detail=f"Midpoint of {name} and {right_name} Body origins",
            )
        )
    return tuple(candidates)


def _landmark_world_position(
    robot: RobotViewerModel, candidate: LandmarkCandidate
) -> np.ndarray:
    if candidate.kind == "body_origin":
        return np.asarray(robot.data.xpos[candidate.body_ids[0]], dtype=np.float64).copy()
    if candidate.kind == "body_com":
        return np.asarray(robot.data.xipos[candidate.body_ids[0]], dtype=np.float64).copy()
    if candidate.kind == "subtree_com":
        return np.asarray(
            robot.data.subtree_com[candidate.body_ids[0]], dtype=np.float64
        ).copy()
    return np.mean(
        np.asarray([robot.data.xpos[body_id] for body_id in candidate.body_ids]),
        axis=0,
    )


def _world_to_body_local(
    robot: RobotViewerModel, body_id: int, world_position: np.ndarray
) -> np.ndarray:
    origin = np.asarray(robot.data.xpos[body_id], dtype=np.float64)
    rotation = np.asarray(robot.data.xmat[body_id], dtype=np.float64).reshape(3, 3)
    return rotation.T @ (np.asarray(world_position, dtype=np.float64) - origin)


class _WindowsAltLeftPan:
    """Touchpad-friendly pan while preserving MuJoCo's native mouse controls."""

    def __init__(self, viewer) -> None:
        import ctypes

        self._viewer = viewer
        self._user32 = ctypes.windll.user32
        self._point_type = type(
            "POINT",
            (ctypes.Structure,),
            {"_fields_": [("x", ctypes.c_long), ("y", ctypes.c_long)]},
        )
        self._last: tuple[int, int] | None = None
        self._azimuth = 0.0
        self._elevation = 0.0

    def _pressed(self, virtual_key: int) -> bool:
        return bool(self._user32.GetAsyncKeyState(virtual_key) & 0x8000)

    def _cursor(self) -> tuple[int, int]:
        point = self._point_type()
        self._user32.GetCursorPos(point)
        return int(point.x), int(point.y)

    def update(self) -> None:
        dragging = self._pressed(0x12) and self._pressed(0x01)  # Alt + LButton
        if not dragging:
            self._last = None
            return
        current = self._cursor()
        if self._last is None:
            self._last = current
            self._azimuth = float(self._viewer.cam.azimuth)
            self._elevation = float(self._viewer.cam.elevation)
            return
        dx = current[0] - self._last[0]
        dy = current[1] - self._last[1]
        self._last = current

        # Native left-drag rotates the camera. Restore its orientation so the
        # Alt gesture acts only as a pan.
        self._viewer.cam.azimuth = self._azimuth
        self._viewer.cam.elevation = self._elevation
        viewport = self._viewer.viewport
        height = max(1, int(viewport.height) if viewport is not None else 800)
        fovy = math.radians(float(self._viewer.m.vis.global_.fovy))
        scale = 2.0 * float(self._viewer.cam.distance) * math.tan(fovy * 0.5) / height
        azimuth = math.radians(self._azimuth)
        elevation = math.radians(self._elevation)
        right = np.asarray(
            [math.sin(azimuth), -math.cos(azimuth), 0.0], dtype=np.float64
        )
        camera_out = np.asarray(
            [
                math.cos(elevation) * math.cos(azimuth),
                math.cos(elevation) * math.sin(azimuth),
                math.sin(elevation),
            ],
            dtype=np.float64,
        )
        up = np.cross(right, camera_out)
        up /= max(float(np.linalg.norm(up)), 1e-12)
        self._viewer.cam.lookat[:] += (-right * dx + up * dy) * scale


def _link_list_text(
    body_names: tuple[str, ...],
    *,
    cursor_index: int,
    selected_index: int,
    active: bool = False,
    visible_rows: int = 11,
) -> str:
    """Build a compact, fixed-position Link selector for the 3D overlay."""
    if not body_names:
        return "LINKS\n(no bodies)"
    rows = max(3, int(visible_rows))
    cursor = max(0, min(len(body_names) - 1, int(cursor_index)))
    selected = max(0, min(len(body_names) - 1, int(selected_index)))
    start = max(0, cursor - rows // 2)
    start = min(start, max(0, len(body_names) - rows))
    stop = min(len(body_names), start + rows)
    prefix = "LINKS (ACTIVE)" if active else "LINKS"
    lines = [f"{prefix}  [L: focus/toggle]"]
    if start > 0:
        lines.append("  ...")
    for index in range(start, stop):
        cursor_marker = ">" if index == cursor else " "
        selected_marker = "*" if index == selected else " "
        lines.append(f"{cursor_marker}{selected_marker} {body_names[index]}")
    if stop < len(body_names):
        lines.append("  ...")
    lines.append(f"Selected: {body_names[selected]}")
    return "\n".join(lines)


def _landmark_list_text(
    candidates: tuple[LandmarkCandidate, ...],
    *,
    cursor_index: int,
    selected_index: int,
    active: bool,
    visible_rows: int = 9,
) -> str:
    if not candidates:
        return "LANDMARKS\n(no candidates)"
    rows = max(3, int(visible_rows))
    cursor = max(0, min(len(candidates) - 1, int(cursor_index)))
    selected = max(0, min(len(candidates) - 1, int(selected_index)))
    start = max(0, cursor - rows // 2)
    start = min(start, max(0, len(candidates) - rows))
    stop = min(len(candidates), start + rows)
    prefix = "LANDMARKS (ACTIVE)" if active else "LANDMARKS"
    lines = [f"{prefix}  [M: focus/toggle]"]
    for index in range(start, stop):
        lines.append(
            f"{'>' if index == cursor else ' '}{'*' if index == selected else ' '} "
            f"{candidates[index].label}"
        )
    selected_candidate = candidates[selected]
    lines.append(f"Selected: {selected_candidate.label}")
    lines.append(selected_candidate.detail)
    return "\n".join(lines)


def _update_axis_geometries(
    viewer,
    robot: RobotViewerModel,
    *,
    mode: AxesMode,
    selected_body_id: int,
    axis_length_m: float,
    landmark: LandmarkCandidate | None = None,
) -> None:
    scene = viewer.user_scn
    scene.ngeom = 0
    if landmark is not None:
        position = _landmark_world_position(robot, landmark)
        reference_origin = np.asarray(
            robot.data.xpos[landmark.reference_body_id], dtype=np.float64
        )
        _append_connector(
            scene,
            geom_type=mujoco.mjtGeom.mjGEOM_CAPSULE,
            width=max(0.001, axis_length_m * 0.012),
            start=reference_origin,
            end=position,
            colour=np.asarray([1.0, 0.85, 0.1, 0.9], dtype=np.float32),
        )
        _append_marker(scene, position, radius=max(0.006, axis_length_m * 0.055))
    if mode == "off" or (mode == "selected" and selected_body_id <= 0):
        return
    body_ids = (
        (selected_body_id,)
        if mode == "selected"
        else tuple(range(1, robot.model.nbody))
    )
    colours = (
        np.asarray([0.9, 0.1, 0.1, 1.0], dtype=np.float32),
        np.asarray([0.1, 0.75, 0.15, 1.0], dtype=np.float32),
        np.asarray([0.1, 0.25, 0.95, 1.0], dtype=np.float32),
    )
    width = max(0.002, axis_length_m * 0.025)
    for body_id in body_ids:
        # Keep the Body-frame orientation, but place the triad at the Link's
        # inertial COM so it remains visible through the translucent shell.
        display_origin = np.asarray(robot.data.xipos[body_id], dtype=np.float64)
        rotation = np.asarray(robot.data.xmat[body_id], dtype=np.float64).reshape(3, 3)
        if mode == "selected":
            if not _append_marker(
                scene, display_origin, radius=max(0.004, width * 1.6)
            ):
                return
        for axis_index, colour in enumerate(colours):
            target = display_origin + rotation[:, axis_index] * axis_length_m
            if not _append_connector(
                scene,
                geom_type=mujoco.mjtGeom.mjGEOM_CAPSULE,
                width=width,
                start=display_origin,
                end=target,
                colour=colour,
            ):
                return


def _append_connector(
    scene,
    *,
    geom_type,
    width: float,
    start: np.ndarray,
    end: np.ndarray,
    colour: np.ndarray,
) -> bool:
    geom_index = int(scene.ngeom)
    if geom_index >= int(scene.maxgeom):
        return False
    geom = scene.geoms[geom_index]
    mujoco.mjv_initGeom(
        geom,
        geom_type,
        np.zeros(3),
        np.zeros(3),
        np.eye(3).reshape(-1),
        colour,
    )
    mujoco.mjv_connector(geom, geom_type, width, start, end)
    geom.emission = 1.0
    scene.ngeom += 1
    return True


def _append_marker(scene, position: np.ndarray, *, radius: float) -> bool:
    geom_index = int(scene.ngeom)
    if geom_index >= int(scene.maxgeom):
        return False
    geom = scene.geoms[geom_index]
    mujoco.mjv_initGeom(
        geom,
        mujoco.mjtGeom.mjGEOM_SPHERE,
        np.full(3, radius, dtype=np.float64),
        position,
        np.eye(3).reshape(-1),
        np.asarray([1.0, 1.0, 1.0, 0.95], dtype=np.float32),
    )
    geom.emission = 1.0
    scene.ngeom += 1
    return True
