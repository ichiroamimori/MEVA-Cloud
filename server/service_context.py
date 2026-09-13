from __future__ import annotations

import re
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, field_validator


IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9_-]+$")


class Role(StrEnum):
    ADMIN = "admin"
    USER = "user"
    WORKER = "worker"
    SUPERVISOR = "supervisor"
    SYSTEM_ADMIN = "system_admin"


class Plan(StrEnum):
    FREE = "free"
    TRIAL = "trial"
    STANDARD = "standard"
    ENTERPRISE = "enterprise"


ROLE_LABELS = {
    Role.ADMIN: "Admin",
    Role.USER: "User",
    Role.WORKER: "Worker",
    Role.SUPERVISOR: "Supervisor",
    Role.SYSTEM_ADMIN: "System Admin",
}
PLAN_LABELS = {
    Plan.FREE: "Free",
    Plan.TRIAL: "Trial",
    Plan.STANDARD: "Standard",
    Plan.ENTERPRISE: "Enterprise",
}

STANDARD_REPLACE_ROLES = {Role.SUPERVISOR, Role.SYSTEM_ADMIN}


def can_replace_standard(role: Role | str) -> bool:
    try:
        return Role(role) in STANDARD_REPLACE_ROLES
    except ValueError:
        return False


class User(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    user_id: str
    display_name: str
    email: str | None = None
    role: Role

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, value: str) -> str:
        if not IDENTIFIER_RE.fullmatch(value):
            raise ValueError("Invalid user_id")
        return value


class Workspace(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    workspace_id: str
    display_name: str
    plan: Plan | None = None

    @field_validator("workspace_id")
    @classmethod
    def validate_workspace_id(cls, value: str) -> str:
        if not IDENTIFIER_RE.fullmatch(value):
            raise ValueError("Invalid workspace_id")
        return value


DEVELOPMENT_USER = User(
    user_id="Xenoma_Admin_01",
    display_name="Zenosuke Miyamoto",
    email=None,
    role=Role.SYSTEM_ADMIN,
)
DEVELOPMENT_WORKSPACE = Workspace(
    workspace_id="meva_development",
    display_name="MEVA Cloud Development",
    plan=None,
)

# Existing data remains under workspace/users/local_user. Authentication can
# replace this compatibility mapping without moving current Capsule data.
DEVELOPMENT_STORAGE_USER_ID = "local_user"


def public_service_context() -> dict:
    user = DEVELOPMENT_USER.model_dump()
    workspace = DEVELOPMENT_WORKSPACE.model_dump()
    user["role_label"] = ROLE_LABELS[Role(user["role"])]
    user["can_replace_standard"] = can_replace_standard(user["role"])
    if workspace["plan"] is not None:
        workspace["plan_label"] = PLAN_LABELS[Plan(workspace["plan"])]
    return {"user": user, "workspace": workspace}
