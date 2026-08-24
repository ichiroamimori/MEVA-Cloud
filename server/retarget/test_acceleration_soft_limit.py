from __future__ import annotations

import unittest

from ik_solver import acceleration_soft_weight


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


if __name__ == "__main__":
    unittest.main()
