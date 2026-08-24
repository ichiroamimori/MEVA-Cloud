"""Canonical fixed-column layout for MEVA position and raw GCP data."""

MEVA_HEADER_ROW_1BASED = 8

# Zero-based CSV indices (Excel Pelvis LW/LX/LY, Feet BD/BE/BF and NI/NJ/NK).
MEVA_POSITION_COLUMN_INDICES = {
    "Pelvis": (334, 335, 336),
    "LeftFoot": (55, 56, 57),
    "RightFoot": (372, 373, 374),
}

MEVA_GCP_COLUMN_INDICES = {
    "left_ff": 58,
    "left_ca": 59,
    "right_ff": 375,
    "right_ca": 376,
}
