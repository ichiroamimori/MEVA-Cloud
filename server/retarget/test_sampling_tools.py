from __future__ import annotations

import unittest

import numpy as np

from tools.cubic_spline import cubic_spline_resample
from tools.quaternion_slerp import quaternion_slerp_resample
from tools.sampling import target_timeline


class SamplingToolTests(unittest.TestCase):
    def test_1000_source_frames_at_100_hz_become_300_at_30_fps(self):
        frame, time_s, source_float, nearest = target_timeline(
            start_frame=0, end_frame=999, source_fps=100.0, target_fps=30.0
        )
        self.assertEqual(len(frame), 300)
        np.testing.assert_allclose(time_s[:4], [0.0, 1 / 30, 2 / 30, 3 / 30])
        np.testing.assert_allclose(source_float[:4], [0.0, 10 / 3, 20 / 3, 10.0])
        np.testing.assert_array_equal(nearest[:4], [0, 3, 7, 10])
        self.assertTrue(np.all(source_float < 1000.0))

    def test_slerp_is_unit_length_and_exact_at_source_samples(self):
        source_time = np.asarray([0.0, 1.0, 2.0])
        source_quat = np.asarray([
            [1.0, 0.0, 0.0, 0.0],
            [np.sqrt(0.5), 0.0, 0.0, np.sqrt(0.5)],
            [0.0, 0.0, 0.0, 1.0],
        ])
        result = quaternion_slerp_resample(
            source_time, source_quat, np.asarray([0.0, 0.5, 1.0, 1.5, 2.0])
        )
        np.testing.assert_allclose(np.linalg.norm(result, axis=1), 1.0, atol=1e-12)
        np.testing.assert_allclose(result[[0, 2, 4]], source_quat, atol=1e-12)

    def test_cubic_spline_is_finite_and_exact_at_source_samples(self):
        source_time = np.linspace(0.0, 1.0, 11)
        source = np.column_stack((source_time**3, np.sin(source_time)))
        result = cubic_spline_resample(source_time, source, source_time)
        self.assertTrue(np.all(np.isfinite(result)))
        np.testing.assert_allclose(result, source, atol=1e-12)

    def test_single_source_sample_is_stable(self):
        target_time = np.asarray([0.0])
        np.testing.assert_allclose(
            cubic_spline_resample(np.asarray([0.0]), np.asarray([2.5]), target_time),
            [2.5],
        )
        np.testing.assert_allclose(
            quaternion_slerp_resample(
                np.asarray([0.0]), np.asarray([[2.0, 0.0, 0.0, 0.0]]), target_time
            ),
            [[1.0, 0.0, 0.0, 0.0]],
        )


if __name__ == "__main__":
    unittest.main()
