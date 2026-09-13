from __future__ import annotations

import unittest

import mujoco

from server.retarget.ik_solver import (
    acceleration_soft_weight,
    resolve_joint_acceleration_limit,
)


class AccelerationSoftWeightTest(unittest.TestCase):
    def test_requested_weight_curve(self) -> None:
        weight_at_2x = 0.2
        expected = {
            0.5: 0.0,
            1.0: 0.0,
            1.2: 0.2 * weight_at_2x,
            1.5: 0.5 * weight_at_2x,
            2.0: 1.0 * weight_at_2x,
            3.0: 2.0 * weight_at_2x,
        }
        for ratio, weight in expected.items():
            with self.subTest(ratio=ratio):
                self.assertAlmostEqual(
                    acceleration_soft_weight(ratio, weight_at_2x), weight
                )

    def test_zero_weight_disables_soft_cost(self) -> None:
        self.assertEqual(acceleration_soft_weight(10.0, 0.0), 0.0)

    def test_common_limit_is_expanded_to_each_hinge_joint(self) -> None:
        model = mujoco.MjModel.from_xml_string("""
            <mujoco>
              <worldbody>
                <body name="base">
                  <freejoint name="root"/>
                  <geom type="sphere" size="0.01" mass="1"/>
                  <body name="first">
                    <joint name="joint_a" type="hinge" axis="1 0 0"/>
                    <geom type="sphere" size="0.01" mass="1"/>
                    <body name="second">
                      <joint name="joint_b" type="hinge" axis="0 1 0"/>
                      <geom type="sphere" size="0.01" mass="1"/>
                    </body>
                  </body>
                </body>
              </worldbody>
            </mujoco>
        """)
        enabled, limits = resolve_joint_acceleration_limit(model, {
            "enabled": True,
            "default_rad_s2": 220.0,
            "overrides": {},
        })
        self.assertTrue(enabled)
        self.assertEqual(limits, {"joint_a": 220.0, "joint_b": 220.0})
        self.assertNotIn("root", limits)

    def test_legacy_per_joint_overrides_remain_supported(self) -> None:
        model = mujoco.MjModel.from_xml_string("""
            <mujoco>
              <worldbody>
                <body name="body">
                  <joint name="joint_a" type="hinge"/>
                  <geom type="sphere" size="0.01" mass="1"/>
                </body>
              </worldbody>
            </mujoco>
        """)
        enabled, limits = resolve_joint_acceleration_limit(model, {
            "enabled": True,
            "default_rad_s2": 0.0,
            "overrides": {"joint_a": {"max_rad_s2": 140.0}},
        })
        self.assertTrue(enabled)
        self.assertEqual(limits, {"joint_a": 140.0})


if __name__ == "__main__":
    unittest.main()
