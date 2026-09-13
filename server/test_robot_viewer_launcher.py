from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from fastapi import HTTPException

from server.api.retarget_robot_api import launch_registered_robot_viewer
from server.robot_registry import resolve_variant
from server.robot_viewer_launcher import launch_robot_viewer
from server.retarget.robot_motion_viewer import _motion_frame_for_elapsed


class RobotViewerLauncherTest(unittest.TestCase):
    def test_motion_playback_follows_wall_clock_and_skips_late_render_frames(self):
        self.assertEqual(
            _motion_frame_for_elapsed(
                0, 0.51, frame_count=100, fps=30.0, speed=1.0, loop=True,
            ),
            (15, False),
        )
        self.assertEqual(
            _motion_frame_for_elapsed(
                95, 0.20, frame_count=100, fps=30.0, speed=1.0, loop=True,
            ),
            (1, False),
        )
        self.assertEqual(
            _motion_frame_for_elapsed(
                95, 0.20, frame_count=100, fps=30.0, speed=1.0, loop=False,
            ),
            (99, True),
        )

    def test_registered_variants_use_existing_cli_with_selected_motion(self):
        with tempfile.TemporaryDirectory() as directory:
            motion = Path(directory) / "selected.pkl"
            motion.touch()
            for variant in ("g1_29dof", "k1_22dof"):
                with self.subTest(variant=variant), patch(
                    "server.robot_viewer_launcher.subprocess.Popen"
                ) as popen, patch(
                    "server.robot_viewer_launcher.threading.Thread"
                ) as thread:
                    record = resolve_variant(variant)
                    popen.return_value = Mock(pid=123)
                    popen.return_value.wait.side_effect = subprocess.TimeoutExpired(
                        "viewer", 1
                    )
                    self.assertEqual(launch_robot_viewer(record, motion), 123)
                    args, kwargs = popen.call_args
                    self.assertEqual(args[0], [
                        sys.executable, "-m", "server.retarget.tools.view_robot",
                        str(motion.resolve()),
                        "--manufacturer", record.manufacturer_id,
                        "--robot", record.robot_id, "--variant", variant,
                        "--maximized",
                    ])
                    self.assertEqual(
                        kwargs["cwd"], str(record.repository_root_path)
                    )
                    self.assertNotIn("shell", kwargs)
                    thread.return_value.start.assert_called_once()
                    kwargs["stdout"].close()

    def test_startup_failure_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            motion = Path(directory) / "selected.npz"
            motion.touch()
            with patch("server.robot_viewer_launcher.subprocess.Popen") as popen:
                popen.return_value.wait.return_value = 1
                with self.assertRaisesRegex(RuntimeError, "exited during startup"):
                    launch_robot_viewer(resolve_variant("g1_29dof"), motion)
                self.assertTrue(popen.call_args.kwargs["stdout"].closed)

    def test_api_validates_identity_and_reports_launch_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run_id = "2609010001"
            run = root / run_id
            run.mkdir()
            (run / f"{run_id}_primary.pkl").touch()
            with patch(
                "server.robot_viewer_launcher.launch_robot_viewer", return_value=42
            ) as launch, patch(
                "server.api.retarget_artifact_api.robot_dir", return_value=root
            ):
                for variant, manufacturer, robot in (
                    ("g1_29dof", "unitree", "g1"),
                    ("k1_22dof", "booster", "k1"),
                ):
                    response = launch_registered_robot_viewer(
                        variant, manufacturer, robot, "2609010000", run_id,
                    )
                    self.assertEqual(response["robot_variant"], variant)
                    self.assertEqual(
                        response["motion_file"], f"{run_id}_primary.pkl"
                    )
                    self.assertEqual(launch.call_args.args[0].variant_id, variant)
                    self.assertEqual(
                        launch.call_args.args[1], run / f"{run_id}_primary.pkl"
                    )
                launch.reset_mock()
                for variant in ("missing", "g1_23dof", "../g1_29dof"):
                    with self.assertRaises(HTTPException) as caught:
                        launch_registered_robot_viewer(
                            variant, "unitree", "g1", "2609010000", run_id,
                        )
                    self.assertEqual(caught.exception.status_code, 400)
                launch.assert_not_called()
                with self.assertRaises(HTTPException) as caught:
                    launch_registered_robot_viewer(
                        "g1_29dof", "unitree", "g1",
                        "../workspace", run_id,
                    )
                self.assertEqual(caught.exception.status_code, 400)
                launch.side_effect = OSError("Cannot start viewer")
                with self.assertRaises(HTTPException) as caught:
                    launch_registered_robot_viewer(
                        "g1_29dof", "unitree", "g1",
                        "2609010000", run_id,
                    )
                self.assertEqual(caught.exception.status_code, 500)
                self.assertIn("Cannot start viewer", caught.exception.detail)

    def test_api_resolves_selected_main_result(self):
        with tempfile.TemporaryDirectory() as directory:
            result = Path(directory)
            main_id = "2609010001-01"
            motion = result / f"{main_id}_main.pkl"
            motion.touch()
            with patch(
                "server.api.retarget_artifact_api.resolve_main_result_dir",
                return_value=result,
            ), patch(
                "server.api.retarget_artifact_api.robot_dir",
                return_value=result.parent,
            ), patch(
                "server.robot_viewer_launcher.launch_robot_viewer", return_value=42,
            ) as launch:
                response = launch_registered_robot_viewer(
                    "g1_29dof", "unitree", "g1", "2609010000",
                    "2609010001", "main", main_id,
                )
            self.assertEqual(response["stage"], "main")
            self.assertEqual(response["motion_file"], motion.name)
            self.assertEqual(launch.call_args.args[1], motion)


if __name__ == "__main__":
    unittest.main()
