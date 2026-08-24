from __future__ import annotations

import numpy as np
from scipy.interpolate import CubicSpline


def cubic_spline_resample(
    input_time_s: np.ndarray,
    values: np.ndarray,
    output_time_s: np.ndarray,
) -> np.ndarray:
    """Resample finite scalar/vector coordinates along axis 0."""
    source_time = np.asarray(input_time_s, dtype=np.float64)
    source_values = np.asarray(values, dtype=np.float64)
    target_time = np.asarray(output_time_s, dtype=np.float64)
    if source_time.ndim != 1 or source_values.shape[0] != source_time.size:
        raise ValueError("CubicSpline time/value shapes do not match")
    if source_time.size == 1:
        return np.broadcast_to(source_values[0], (target_time.size, *source_values.shape[1:])).copy()
    if source_time.size < 2 or not np.all(np.diff(source_time) > 0.0):
        raise ValueError("CubicSpline input time must be strictly increasing")
    if not np.all(np.isfinite(source_values)):
        raise ValueError("CubicSpline input contains NaN/Inf")
    result = np.asarray(CubicSpline(source_time, source_values, axis=0)(target_time))
    if not np.all(np.isfinite(result)):
        raise ValueError("CubicSpline output contains NaN/Inf")
    return result
