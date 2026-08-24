from __future__ import annotations

import numpy as np


def target_timeline(
    *, start_frame: int, end_frame: int, source_fps: float, target_fps: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return local frame, time, float source frame and half-up nearest frame."""
    start = int(start_frame)
    end = int(end_frame)
    source_rate = float(source_fps)
    target_rate = float(target_fps)
    if start < 0 or end < start:
        raise ValueError("Frame range must satisfy 0 <= start <= end")
    if not np.isfinite(source_rate) or source_rate <= 0.0:
        raise ValueError("source_fps must be positive")
    if not np.isfinite(target_rate) or target_rate <= 0.0:
        raise ValueError("target_fps must be positive")
    count = int(np.ceil((end + 1 - start) * target_rate / source_rate - 1e-12))
    frame = np.arange(max(0, count), dtype=np.int32)
    time_s = frame.astype(np.float64) / target_rate
    source_float = start + time_s * source_rate
    valid = source_float < end + 1 - 1e-10
    frame, time_s, source_float = frame[valid], time_s[valid], source_float[valid]
    nearest = np.floor(source_float + 0.5).astype(np.int64)
    nearest = np.clip(nearest, start, end).astype(np.int32)
    return frame, time_s, source_float, nearest
