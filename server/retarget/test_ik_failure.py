from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

import mink
import mujoco

from ik_solver import (
    IKFrameSpec,
    IKSequenceFailure,
    PreparedIKFrame,
    SolverSettings,
    solve_ik_sequence,
)


class IKFailureTests(unittest.TestCase):
    def test_unexpected_solver_exception_becomes_sequence_failure(self) -> None:
        root = Path(__file__).resolve().parents[2]
        model = mujoco.MjModel.from_xml_path(
            str(root / "server/robots/unitree/g1/g1_29dof.xml")
        )
        configuration = mink.Configuration(model)
        settings = SolverSettings(
            solver_name="daqp", dt_s=0.02, global_damping=1e-8,
            max_iterations=1, convergence_joint_delta_deg=0.01,
            convergence_consecutive_iterations=1, output_frame_dt_s=0.01,
            enforce_hard_xml_limits=False, joint_limit_avoidance={"enabled": False},
            velocity_limit_enabled=False, velocity_limit_default_rad_s=1.0,
            velocity_limit_by_joint={}, acceleration_limit_enabled=False,
            acceleration_limit_by_joint={}, acceleration_weight_at_2x_limit=0.0,
            self_collision_avoidance={"enabled": False},
            temporal_regularization_enabled=False, temporal_regularization_cost=0.0,
        )
        frames = [IKFrameSpec(
            source_frame=123,
            prepare=lambda _: PreparedIKFrame(tasks=[]),
        )]
        with patch("ik_solver.mink.solve_ik", side_effect=RuntimeError("solver boom")):
            with self.assertRaises(IKSequenceFailure) as caught:
                solve_ik_sequence(
                    model=model, initial_configuration=configuration,
                    frame_specs=frames, solver_settings=settings,
                    diagnostic_keys=[],
                )
        failure = caught.exception
        self.assertEqual(failure.output_index, 0)
        self.assertEqual(failure.source_frame, 123)
        self.assertEqual(len(failure.result.qpos), 0)
        self.assertIn("RuntimeError: solver boom", str(failure))


if __name__ == "__main__":
    unittest.main()
