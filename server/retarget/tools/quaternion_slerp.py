from __future__ import annotations

import numpy as np


def _normalize(quaternions: np.ndarray) -> np.ndarray:
    q = np.asarray(quaternions, dtype=np.float64)
    norms = np.linalg.norm(q, axis=-1, keepdims=True)
    if np.any(~np.isfinite(q)) or np.any(norms < 1e-12):
        raise ValueError("Quaternion series contains an invalid quaternion")
    return q / norms


def quaternion_slerp_resample(
    input_time_s: np.ndarray,
    quaternions: np.ndarray,
    output_time_s: np.ndarray,
) -> np.ndarray:
    """Shortest-path SLERP for a wxyz or xyzw series without changing order."""
    source_time = np.asarray(input_time_s, dtype=np.float64)
    target_time = np.asarray(output_time_s, dtype=np.float64)
    source = _normalize(quaternions)
    if source_time.ndim != 1 or source.shape != (source_time.size, 4):
        raise ValueError("SLERP expects quaternion shape (N, 4)")
    if source_time.size == 1:
        return np.repeat(source, target_time.size, axis=0)
    if source_time.size < 2 or not np.all(np.diff(source_time) > 0.0):
        raise ValueError("SLERP input time must be strictly increasing")
    if np.any(target_time < source_time[0] - 1e-12) or np.any(
        target_time > source_time[-1] + 1e-12
    ):
        raise ValueError("SLERP target time is outside input range")

    out = np.empty((target_time.size, 4), dtype=np.float64)
    right = np.searchsorted(source_time, target_time, side="right")
    right = np.clip(right, 1, source_time.size - 1)
    left = right - 1
    exact_last = np.isclose(target_time, source_time[-1], atol=1e-12, rtol=0.0)
    left[exact_last] = source_time.size - 2
    right[exact_last] = source_time.size - 1
    for index, (lo, hi, time_value) in enumerate(zip(left, right, target_time)):
        q0 = source[lo]
        q1 = source[hi]
        span = source_time[hi] - source_time[lo]
        fraction = float((time_value - source_time[lo]) / span)
        dot = float(np.dot(q0, q1))
        if dot < 0.0:
            q1 = -q1
            dot = -dot
        dot = float(np.clip(dot, -1.0, 1.0))
        if dot > 0.9995:
            out[index] = q0 + fraction * (q1 - q0)
        else:
            angle = float(np.arccos(dot))
            denominator = float(np.sin(angle))
            out[index] = (
                np.sin((1.0 - fraction) * angle) / denominator * q0
                + np.sin(fraction * angle) / denominator * q1
            )
    return _normalize(out)
