"""Versioned MEVA segment geometry used by retarget offset derivation.

The vectors are normalized directions in the MEVA BVH segment-local frame.
They were verified against the two supported reference MEVA skeletons; those
skeletons have different bone lengths but identical normalized directions.
Runtime Capsule BVH data must not be consulted by the offset algorithm.
"""
from __future__ import annotations

import hashlib
import json

import numpy as np


CANONICAL_GEOMETRY_VERSION = "meva-canonical-geometry-1.0"

MEVA_CANONICAL_GEOMETRY = {
    "Pelvis": [-0.194738478, 0.980855201, 0.0],
    "Thoracic2": [0.437306804, 0.899312381, -0.000004832],
    "Thoracic2+LumberSpine": [-0.402039067, 0.915622514, 0.000012580],
    "LeftUpperArm": [0.045840186, -0.998388154, 0.033462985],
    "LeftForearm": [0.003140607, -0.999773277, 0.021060180],
    "RightUpperArm": [0.045840186, -0.998388154, -0.033462985],
    "RightForearm": [0.003140607, -0.999773277, -0.021060180],
    "LeftUpperLeg": [-0.019438030, -0.999782893, 0.007505321],
    "LeftLowerLeg": [-0.029193343, -0.999573784, 0.0],
    "RightUpperLeg": [-0.019438030, -0.999782893, -0.007505321],
    "RightLowerLeg": [-0.029193343, -0.999573784, 0.0],
}


def canonical_direction(segment: str) -> np.ndarray:
    try:
        value = np.asarray(MEVA_CANONICAL_GEOMETRY[segment], dtype=np.float64)
    except KeyError as exc:
        raise KeyError(f"No canonical MEVA geometry for segment: {segment}") from exc
    norm = float(np.linalg.norm(value))
    if value.shape != (3,) or not np.isfinite(norm) or norm <= 1e-12:
        raise ValueError(f"Invalid canonical MEVA geometry for segment: {segment}")
    return value / norm


def canonical_geometry_hash(*, terminal_semantics: dict | None = None) -> str:
    document = {
        "version": CANONICAL_GEOMETRY_VERSION,
        "directions": MEVA_CANONICAL_GEOMETRY,
        "terminal_semantics": terminal_semantics or {},
    }
    raw = json.dumps(document, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
