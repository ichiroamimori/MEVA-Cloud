from __future__ import annotations

import pickle
import tempfile
import unittest
from pathlib import Path

import numpy as np

from server.robot_registry import repository_root
from server.retarget.robot_motion_viewer import (
    RobotViewerModel,
    _link_list_text,
    load_viewer_motion,
)


class RobotMotionViewerTest(unittest.TestCase):
    def test_link_list_marks_cursor_and_selected_body(self) -> None:
        text = _link_list_text(
            ("No select", "pelvis", "torso", "left_arm", "left_forearm"),
            cursor_index=2,
            selected_index=1,
            visible_rows=3,
        )
        self.assertIn(" * pelvis", text)
        self.assertIn(">  torso", text)
        self.assertIn("Selected: pelvis", text)

    def test_registered_initial_pose_and_output_order(self) -> None:
        expected = {"g1_29dof": 29, "k1_22dof": 22}
        for variant, dof in expected.items():
            with self.subTest(variant=variant):
                robot = RobotViewerModel.from_variant(
                    variant,
                    root=repository_root(),
                )
                self.assertEqual(len(robot.output_joint_names), dof)
                self.assertEqual(len(robot.output_qpos_addresses), dof)
                self.assertTrue(np.all(np.isfinite(robot.initial_qpos)))
                self.assertGreater(robot.root_body_id, 0)

    def test_gmr_motion_load_and_apply(self) -> None:
        robot = RobotViewerModel.from_variant(
            "k1_22dof",
            root=repository_root(),
        )
        frames = 2
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "motion.npz"
            np.savez(
                path,
                fps=np.asarray(30.0),
                root_pos=np.zeros((frames, 3)),
                root_rot=np.tile([0.0, 0.0, 0.0, 1.0], (frames, 1)),
                root_rot_order=np.asarray("xyzw"),
                joint_names=np.asarray(robot.output_joint_names),
                dof_pos=np.zeros((frames, 22)),
                source_frame_nearest=np.arange(frames),
            )
            motion = load_viewer_motion(path)
            robot.validate_motion(motion)
            robot.apply_motion_frame(motion, 1)
            self.assertTrue(np.all(np.isfinite(robot.data.qpos)))
            self.assertAlmostEqual(robot.data.time, 1.0 / 30.0)

    def test_gmr_pickle_defaults_to_xyzw(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "motion.pkl"
            with path.open("wb") as stream:
                pickle.dump(
                    {
                        "fps": 50.0,
                        "root_pos": np.zeros((1, 3)),
                        "root_rot": np.asarray([[0.0, 0.0, 0.0, 1.0]]),
                        "dof_pos": np.zeros((1, 22)),
                        "local_body_pos": None,
                        "link_body_list": None,
                    },
                    stream,
                )
            motion = load_viewer_motion(path)
            self.assertEqual(motion.root_rot_order, "xyzw")
            self.assertEqual(motion.frame_count, 1)

    def test_motion_dof_mismatch_is_rejected(self) -> None:
        robot = RobotViewerModel.from_variant(
            "k1_22dof",
            root=repository_root(),
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "motion.npz"
            np.savez(
                path,
                fps=np.asarray(30.0),
                root_pos=np.zeros((1, 3)),
                root_rot=np.asarray([[0.0, 0.0, 0.0, 1.0]]),
                dof_pos=np.zeros((1, 29)),
            )
            motion = load_viewer_motion(path)
            with self.assertRaisesRegex(ValueError, "Motion DoF"):
                robot.validate_motion(motion)


if __name__ == "__main__":
    unittest.main()
