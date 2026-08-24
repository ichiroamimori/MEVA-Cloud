from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

import numpy as np

from main_diagnostics import write_main_diagnostics_csv


class MainDiagnosticsTest(unittest.TestCase):
    def test_centered_acceleration_ratio_and_soft_weight(self) -> None:
        diagnostics = [
            (100, 0.1, 2.0, 3, True, 0.01),
            (101, 0.2, 3.0, 4, False, 0.02),
            (102, 0.3, 4.0, 5, True, 0.03),
        ]
        expected_weights = {1.0: 0.0, 1.5: 0.25, 2.0: 0.5, 3.0: 1.0}
        for ratio, expected_weight in expected_weights.items():
            with self.subTest(ratio=ratio), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "main_diagnostics.csv"
                # fps=10 -> dt^2=.01, so q[2]=ratio*.01 gives a[1]=ratio.
                q = np.asarray([[0.0], [0.0], [ratio * 0.01]])
                write_main_diagnostics_csv(
                    path,
                    diagnostics=diagnostics,
                    dof_pos=q,
                    source_frame_indices=np.asarray([100, 101, 102]),
                    fps=10.0,
                    joint_names=["joint_a"],
                    acceleration_limits={"joint_a": 1.0},
                    weight_at_2x_limit=0.5,
                )
                with path.open(encoding="utf-8-sig", newline="") as stream:
                    rows = list(csv.DictReader(stream))
                self.assertEqual(len(rows), 3)
                self.assertEqual(rows[1]["source_frame"], "101")
                self.assertEqual(rows[1]["max_acceleration_joint"], "joint_a")
                self.assertAlmostEqual(float(rows[1]["max_acceleration_ratio"]), ratio)
                self.assertAlmostEqual(
                    float(rows[1]["acceleration_soft_weight"]), expected_weight
                )
                self.assertEqual(rows[0]["max_acceleration_ratio"], "")
                self.assertEqual(rows[2]["max_acceleration_ratio"], "")


if __name__ == "__main__":
    unittest.main()
