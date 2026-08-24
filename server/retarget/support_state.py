# -*- coding: utf-8 -*-
"""Support-state values shared by Main preprocessing, IK, and anchoring."""
from enum import IntEnum


class SupportState(IntEnum):
    FLYING = 0
    SINGLE_LEFT = 1
    SINGLE_RIGHT = 2
    DOUBLE_LEFT_MAIN = 3
    DOUBLE_RIGHT_MAIN = 4


def main_support_side(state: SupportState) -> str | None:
    """Return the foot fixed by Main postprocessing for ``state``."""
    if state in (SupportState.SINGLE_LEFT, SupportState.DOUBLE_LEFT_MAIN):
        return "left"
    if state in (SupportState.SINGLE_RIGHT, SupportState.DOUBLE_RIGHT_MAIN):
        return "right"
    return None
