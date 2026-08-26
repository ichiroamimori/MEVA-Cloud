from __future__ import annotations

import unittest

import mink
import mujoco
import numpy as np

from ik_solver import (
    SelfCollisionDampingTask,
    _integrate_with_collision_backtracking,
)


MODEL_XML = """
<mujoco>
  <worldbody>
    <body name="a" pos="0 0 0">
      <joint name="a_x" type="slide" axis="1 0 0"/>
      <geom name="a_geom" type="sphere" size="0.1"/>
    </body>
    <body name="b" pos="0.19 0 0">
      <joint name="b_x" type="slide" axis="1 0 0"/>
      <geom name="b_geom" type="sphere" size="0.1"/>
    </body>
  </worldbody>
</mujoco>
"""


class SelfCollisionDampingTaskTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = mujoco.MjModel.from_xml_string(MODEL_XML)
        self.geom_pair = [(
            mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_GEOM, "a_geom"),
            mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_GEOM, "b_geom"),
        )]

    def _configuration(self, separation_delta: float) -> mink.Configuration:
        q = self.model.qpos0.copy()
        q[1] = separation_delta
        return mink.Configuration(self.model, q=q)

    def _distance(self, configuration: mink.Configuration) -> float:
        return float(mujoco.mj_geomDistance(
            self.model,
            configuration.data,
            self.geom_pair[0][0],
            self.geom_pair[0][1],
            1e6,
            np.empty(6, dtype=float),
        ))

    def _numeric_residual_jacobian(
        self, configuration: mink.Configuration, zone_m: float
    ) -> np.ndarray:
        epsilon = 1e-7
        values = []
        for dof in range(self.model.nv):
            direction = np.zeros(self.model.nv)
            direction[dof] = 1.0
            q_plus = configuration.q.copy()
            q_minus = configuration.q.copy()
            mujoco.mj_integratePos(self.model, q_plus, direction, epsilon)
            mujoco.mj_integratePos(self.model, q_minus, -direction, epsilon)
            plus = self._distance(mink.Configuration(self.model, q=q_plus))
            minus = self._distance(mink.Configuration(self.model, q=q_minus))
            residual_plus = max(zone_m - plus, 0.0)
            residual_minus = max(zone_m - minus, 0.0)
            values.append((residual_plus - residual_minus) / (2.0 * epsilon))
        return np.asarray(values)

    def test_residual_is_non_negative_and_zero_outside_zone(self) -> None:
        zone = 0.005
        task = SelfCollisionDampingTask(self.model, self.geom_pair, zone, 0.01, 5.0)

        penetrating = self._configuration(0.0)  # signed distance = -0.01 m
        self.assertAlmostEqual(float(task.compute_error(penetrating)[0]), 0.015)

        outside = self._configuration(0.02)  # signed distance = +0.01 m
        self.assertEqual(float(task.compute_error(outside)[0]), 0.0)
        np.testing.assert_allclose(task.compute_jacobian(outside), 0.0)

    def test_jacobian_matches_finite_difference_on_both_sides_of_contact(self) -> None:
        zone = 0.005
        for separation_delta in (0.0, 0.012):  # -10 mm and +2 mm distance
            with self.subTest(separation_delta=separation_delta):
                configuration = self._configuration(separation_delta)
                task = SelfCollisionDampingTask(
                    self.model, self.geom_pair, zone, 0.01, 5.0
                )
                task.compute_error(configuration)
                analytic = task.compute_jacobian(configuration)[0]
                numeric = self._numeric_residual_jacobian(configuration, zone)
                np.testing.assert_allclose(analytic, numeric, atol=1e-6, rtol=1e-5)

    def test_one_solver_step_reduces_penetration_violation(self) -> None:
        configuration = self._configuration(0.0)
        task = SelfCollisionDampingTask(
            self.model, self.geom_pair, 0.005, 0.01, 5.0
        )
        before = self._distance(configuration)
        velocity = mink.solve_ik(
            configuration,
            [task],
            dt=0.02,
            solver="daqp",
            damping=1e-8,
            limits=[],
            safety_break=True,
        )
        configuration.integrate_inplace(velocity, 0.02)
        self.assertGreater(self._distance(configuration), before)

    def test_backtracking_prevents_a_safe_pose_from_crossing_contact(self) -> None:
        configuration = self._configuration(0.018)  # +8 mm signed distance
        task = SelfCollisionDampingTask(
            self.model, self.geom_pair, 0.005, 0.01, 5.0
        )
        velocity = np.asarray([0.0, -2.0])  # Full step would penetrate deeply.
        scale = _integrate_with_collision_backtracking(
            configuration,
            velocity,
            task,
            dt_s=0.02,
            factor=0.8,
            minimum_step_scale=0.01,
        )
        self.assertGreater(scale, 0.0)
        self.assertLess(scale, 1.0)
        self.assertGreaterEqual(self._distance(configuration), -1e-9)

    def test_backtracking_rejects_a_step_that_deepens_penetration(self) -> None:
        configuration = self._configuration(0.0)  # -10 mm signed distance
        task = SelfCollisionDampingTask(
            self.model, self.geom_pair, 0.005, 0.01, 5.0
        )
        before = self._distance(configuration)
        scale = _integrate_with_collision_backtracking(
            configuration,
            np.asarray([0.0, -1.0]),
            task,
            dt_s=0.02,
            factor=0.8,
            minimum_step_scale=0.05,
        )
        self.assertEqual(scale, 0.0)
        self.assertAlmostEqual(self._distance(configuration), before)


if __name__ == "__main__":
    unittest.main()
