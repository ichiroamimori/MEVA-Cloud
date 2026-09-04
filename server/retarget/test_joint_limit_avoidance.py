# -*- coding: utf-8 -*-
import unittest

import mujoco
import mink
import numpy as np

from ik_solver import JointLimitAvoidanceTask, joint_limit_avoidance_target_and_cost


class JointLimitAvoidanceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = mujoco.MjModel.from_xml_string(
            """
            <mujoco>
              <worldbody>
                <body name="link">
                  <joint name="hinge" type="hinge" range="-100 100"/>
                  <geom type="sphere" size="0.01"/>
                </body>
              </worldbody>
            </mujoco>
            """
        )
        cls.cfg = {
            "enabled": True,
            "default": {
                "limit_zone_percent": 5.0,
                "base_cost": 0.01,
                "max_cost": 0.2,
                "exponent": 2.0,
            },
            "overrides": {},
        }

    def state(self, angle_deg):
        q = np.zeros(self.model.nq)
        q[0] = np.radians(angle_deg)
        return joint_limit_avoidance_target_and_cost(self.model, q, self.cfg)

    def test_safe_region_is_inactive(self):
        target, cost, states = self.state(90.0)
        self.assertEqual(cost[0], 0.0)
        self.assertAlmostEqual(target[0], np.radians(90.0))
        self.assertEqual(states["hinge"]["side"], "safe")

    def test_upper_zone_targets_safe_boundary(self):
        target, cost, states = self.state(95.0)
        self.assertAlmostEqual(target[0], np.radians(90.0))
        self.assertGreater(cost[0], 0.01)
        self.assertLess(cost[0], 0.2)
        self.assertEqual(states["hinge"]["side"], "upper")

    def test_lower_limit_pushes_toward_safe_boundary_and_caps_cost(self):
        target, cost, states = self.state(-100.0)
        self.assertAlmostEqual(target[0], np.radians(-90.0))
        self.assertAlmostEqual(cost[0], 0.2)
        self.assertEqual(states["hinge"]["side"], "lower")

    def test_qp_update_points_away_from_nearest_limit(self):
        task = JointLimitAvoidanceTask(self.model, self.cfg)
        configuration = mink.Configuration(self.model)
        for angle_deg, expected_sign in ((95.0, -1.0), (-95.0, 1.0)):
            q = configuration.q.copy()
            q[0] = np.radians(angle_deg)
            configuration.update(q=q)
            self.assertTrue(task.update_from_configuration(configuration))
            velocity = mink.solve_ik(
                configuration,
                [task],
                dt=0.02,
                solver="daqp",
                damping=1e-8,
                limits=[],
            )
            self.assertGreater(expected_sign * velocity[0], 0.0)


if __name__ == "__main__":
    unittest.main()
