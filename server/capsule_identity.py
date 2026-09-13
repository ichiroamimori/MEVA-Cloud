from __future__ import annotations

import re


CAPSULE_ID_RE = re.compile(r"^\d{10}$")
PUBLIC_CAPSULE_PREFIX = "000000"


def is_valid_capsule_id(capsule_id: str) -> bool:
    return bool(CAPSULE_ID_RE.fullmatch(str(capsule_id)))


def is_public_capsule(capsule_id: str) -> bool:
    value = str(capsule_id)
    return is_valid_capsule_id(value) and value.startswith(PUBLIC_CAPSULE_PREFIX)
