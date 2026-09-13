from __future__ import annotations

import hashlib
import json
import os
import re
import threading
import unicodedata
import uuid
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from server.service_context import (
    DEVELOPMENT_STORAGE_USER_ID,
    DEVELOPMENT_USER,
    DEVELOPMENT_WORKSPACE,
)


CONFIG_SCHEMA_VERSION = "1.0"
SCOPE = Literal["xenoma_standard", "personal", "workspace", "xenoma", "user"]
CONFIG_STAGE = Literal["primary", "main"]
CONFIG_WRITE_LOCK = threading.Lock()
SAFE_COMPONENT_RE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.-]*$")
INVALID_WINDOWS_FILENAME_RE = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
RESERVED_WINDOWS_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


class ConfigStoreError(ValueError):
    pass


class ConfigNameCollision(ConfigStoreError):
    def __init__(self, message: str, *, filename: str | None = None):
        super().__init__(message)
        self.filename = filename


@dataclass(frozen=True)
class ConfigRecord:
    name: str
    scope: SCOPE
    filename: str
    writable: bool
    legacy: bool
    schema_version: str
    stage: CONFIG_STAGE
    config_id: str
    display_name: str
    owner_id: str | None
    target_robot: dict[str, str]
    version: int
    created_by: str
    source_config_id: str | None
    created_at: str
    updated_at: str
    status: Literal["active", "archived"]
    standard_key: str | None

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "scope": self.scope,
            "filename": self.filename,
            "writable": self.writable,
            "legacy": self.legacy,
            "schema_version": self.schema_version,
            "stage": self.stage,
            "config_id": self.config_id,
            "display_name": self.display_name,
            "owner_id": self.owner_id,
            "target_robot": self.target_robot,
            "version": self.version,
            "created_by": self.created_by,
            "source_config_id": self.source_config_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": self.status,
            "standard_key": self.standard_key,
        }


def canonical_scope(scope: SCOPE | str) -> Literal["xenoma_standard", "personal", "workspace"]:
    aliases = {"xenoma": "xenoma_standard", "user": "personal"}
    value = aliases.get(str(scope), str(scope))
    if value not in {"xenoma_standard", "personal", "workspace"}:
        raise ConfigStoreError("Invalid config scope")
    return value  # type: ignore[return-value]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def workspace_root() -> Path:
    override = os.environ.get("MEVA_WORKSPACE_ROOT")
    return Path(override).resolve() if override else repo_root() / "workspace"


def xenoma_assets_root() -> Path:
    override = os.environ.get("MEVA_RETARGET_ASSETS_ROOT")
    return (
        Path(override).resolve()
        if override
        else repo_root() / "server" / "retarget_assets"
    )


def _safe_component(value: str, label: str) -> str:
    if not SAFE_COMPONENT_RE.fullmatch(value) or value in {".", ".."}:
        raise ConfigStoreError(f"Invalid {label}")
    return value


def config_directory(
    scope: SCOPE,
    *,
    source_type: str,
    manufacturer: str,
    robot_variant: str,
    user_id: str = "local_user",
) -> Path:
    source_type = _safe_component(source_type, "source_type")
    manufacturer = _safe_component(manufacturer, "manufacturer")
    robot_variant = _safe_component(robot_variant, "robot_variant")
    if user_id != DEVELOPMENT_STORAGE_USER_ID:
        raise ConfigStoreError("Only the development storage user is supported")
    normalized_scope = canonical_scope(scope)
    if normalized_scope == "xenoma_standard":
        base = xenoma_assets_root() / "configs"
    elif normalized_scope == "personal":
        base = workspace_root() / "users" / user_id / "retarget_assets" / "configs"
    else:
        base = (
            workspace_root() / "workspaces" / DEVELOPMENT_WORKSPACE.workspace_id
            / "retarget_assets" / "configs"
        )
    return base / source_type / manufacturer / robot_variant


def _config_path(directory: Path, filename: str) -> Path:
    if (
        Path(filename).name != filename
        or not filename.lower().endswith(".json")
        or INVALID_WINDOWS_FILENAME_RE.search(filename)
    ):
        raise ConfigStoreError("Invalid config filename")
    resolved_directory = directory.resolve()
    path = (resolved_directory / filename).resolve()
    if path.parent != resolved_directory:
        raise ConfigStoreError("Unsafe config path")
    return path


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ConfigStoreError("Config not found") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigStoreError(f"Could not read config: {path.name}") from exc
    if not isinstance(value, dict):
        raise ConfigStoreError(f"Config must be a JSON object: {path.name}")
    return value


def atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def inferred_name(config: dict[str, Any], filename: str) -> str:
    explicit = str(config.get("name") or config.get("config_name") or "").strip()
    if explicit:
        return explicit
    return Path(filename).stem.replace("_", " ").replace("-", " ").title()


def inferred_stage(config: dict[str, Any]) -> CONFIG_STAGE:
    explicit = str(config.get("retarget_stage") or "").strip().lower()
    if explicit in {"primary", "main"}:
        return explicit  # type: ignore[return-value]
    return "main" if isinstance(config.get("main"), dict) else "primary"


def _target_robot(config: dict[str, Any], robot_variant: str) -> dict[str, str]:
    value = config.get("target_robot")
    if not isinstance(value, dict):
        value = config.get("robot") if isinstance(config.get("robot"), dict) else {}
    target = {
        "manufacturer": str(value.get("manufacturer") or ""),
        "robot_id": str(value.get("robot_id") or value.get("model") or ""),
        "variant": str(value.get("variant") or robot_variant),
    }
    if target["variant"] != robot_variant:
        raise ConfigStoreError(
            f"Config target_robot {target['variant']!r} does not match {robot_variant!r}"
        )
    return target


def _legacy_config_id(scope: str, path: Path) -> str:
    # Keep generated IDs stable across repository roots and Windows machines.
    logical_tail = "/".join(path.parts[-5:]).lower()
    identity = f"{scope}:{logical_tail}"
    return "cfg_" + hashlib.sha256(identity.encode("utf-8")).hexdigest()[:24]


def _metadata_values(
    config: dict[str, Any], *, scope: str, path: Path, robot_variant: str,
) -> dict[str, Any]:
    normalized_scope = canonical_scope(scope)
    display_name = str(
        config.get("display_name") or inferred_name(config, path.name)
    ).strip()
    status = str(config.get("status") or "active").lower()
    if status not in {"active", "archived"}:
        status = "active"
    try:
        version = max(1, int(config.get("version") or 1))
    except (TypeError, ValueError):
        version = 1
    fallback_time = datetime.fromtimestamp(
        path.stat().st_mtime if path.exists() else 0, tz=timezone.utc
    ).isoformat()
    if normalized_scope == "personal":
        owner_id: str | None = DEVELOPMENT_USER.user_id
        default_creator = DEVELOPMENT_USER.user_id
    elif normalized_scope == "workspace":
        owner_id = DEVELOPMENT_WORKSPACE.workspace_id
        default_creator = DEVELOPMENT_USER.user_id
    else:
        owner_id = None
        default_creator = "system"
    return {
        "config_id": str(config.get("config_id") or _legacy_config_id(normalized_scope, path)),
        "display_name": display_name,
        "scope": normalized_scope,
        "owner_id": config.get("owner_id", owner_id),
        "target_robot": _target_robot(config, robot_variant),
        "version": version,
        "created_by": str(config.get("created_by") or default_creator),
        "source_config_id": config.get("source_config_id"),
        "created_at": str(config.get("created_at") or fallback_time),
        "updated_at": str(config.get("updated_at") or fallback_time),
        "status": status,
        "standard_key": (
            str(config.get("standard_key") or "") or None
            if normalized_scope == "xenoma_standard" else None
        ),
    }


def _record(
    config: dict[str, Any], *, scope: str, path: Path,
    robot_variant: str, stage: CONFIG_STAGE,
) -> ConfigRecord:
    metadata = _metadata_values(
        config, scope=scope, path=path, robot_variant=robot_variant,
    )
    return ConfigRecord(
        name=metadata["display_name"],
        scope=metadata["scope"],  # type: ignore[arg-type]
        filename=path.name,
        writable=metadata["scope"] in {"personal", "workspace"},
        legacy=any(key not in config for key in (
            "config_id", "display_name", "scope", "target_robot", "version",
            "created_by", "created_at", "updated_at", "status",
        )),
        schema_version=str(config.get("schema_version") or CONFIG_SCHEMA_VERSION),
        stage=stage,
        config_id=metadata["config_id"],
        display_name=metadata["display_name"],
        owner_id=metadata["owner_id"],
        target_robot=metadata["target_robot"],
        version=metadata["version"],
        created_by=metadata["created_by"],
        source_config_id=metadata["source_config_id"],
        created_at=metadata["created_at"],
        updated_at=metadata["updated_at"],
        status=metadata["status"],
        standard_key=metadata["standard_key"],
    )


def _with_metadata(
    config: dict[str, Any], *, name: str, stage: CONFIG_STAGE, scope: str,
    robot_variant: str, existing: dict[str, Any] | None = None,
    source_config_id: str | None = None,
) -> dict[str, Any]:
    document = normalized_shared_config(config, name=name, stage=stage)
    now = datetime.now(timezone.utc).isoformat()
    old = existing or {}
    normalized_scope = canonical_scope(scope)
    if normalized_scope == "personal":
        owner_id: str | None = DEVELOPMENT_USER.user_id
    elif normalized_scope == "workspace":
        owner_id = DEVELOPMENT_WORKSPACE.workspace_id
    else:
        owner_id = None
    document.update({
        "config_id": str(old.get("config_id") or f"cfg_{uuid.uuid4().hex}"),
        "display_name": name.strip(),
        "scope": normalized_scope,
        "owner_id": owner_id,
        "target_robot": _target_robot(config, robot_variant),
        "version": int(old.get("version") or 0) + 1,
        "created_by": str(old.get("created_by") or DEVELOPMENT_USER.user_id),
        "source_config_id": (
            source_config_id if source_config_id is not None
            else old.get("source_config_id")
        ),
        "created_at": str(old.get("created_at") or now),
        "updated_at": now,
        "status": str(old.get("status") or "active"),
        "standard_key": (
            str(old.get("standard_key") or config.get("standard_key") or "") or None
            if normalized_scope == "xenoma_standard" else None
        ),
    })
    return document


def normalized_shared_config(
    config: dict[str, Any],
    *,
    name: str,
    stage: CONFIG_STAGE = "primary",
) -> dict[str, Any]:
    """Return the reusable Config document without Capsule/Run/cache identity."""
    display_name = name.strip()
    if not display_name:
        raise ConfigStoreError("Config name is required")
    if len(display_name) > 200 or any(ord(ch) < 32 for ch in display_name):
        raise ConfigStoreError("Config name is invalid")

    shared = deepcopy(config)
    shared["schema_version"] = CONFIG_SCHEMA_VERSION
    shared["name"] = display_name
    shared["retarget_stage"] = stage
    # config_name remains a runtime compatibility alias only.
    shared.pop("config_name", None)
    robot = shared.get("robot")
    if isinstance(robot, dict):
        # Model location and initial pose are fixed Variant metadata resolved
        # from server/robots at runtime. Keep only the reusable Robot identity
        # in newly saved Shared Configs. Legacy Configs containing these keys
        # remain readable.
        for key in (
            "mjcf", "model_file", "model_format", "manifest",
            "initial_keyframe", "initial_pose", "root_body", "floating_base",
            "output_joint_order",
        ):
            robot.pop(key, None)
    for key in (
        "capsule_id", "source", "frame_range", "sampling", "offsets", "note",
        "retarget_job",
    ):
        shared.pop(key, None)
    for key in (
        "primary_run_id", "main_id", "primary_post_csv", "main_input_csv",
        "main_calibration", "main_target_analysis", "artifact_generation_id",
        "primary_motion_file", "primary_target_npz", "main_target_npz",
        "main_runtime_context",
    ):
        shared.pop(key, None)

    output = shared.get("output")
    if isinstance(output, dict):
        for key in (
            "run_id", "pkl_name", "overwrite_existing", "config_snapshot_name"
        ):
            output.pop(key, None)
        if not output:
            shared.pop("output", None)
    return shared


def runtime_config(
    shared_config: dict[str, Any],
    runtime_context: dict[str, Any],
) -> dict[str, Any]:
    """Merge reusable settings with the currently open Capsule context."""
    display_name = inferred_name(shared_config, "config.json")
    runtime = deepcopy(shared_config)
    runtime["schema_version"] = str(
        shared_config.get("schema_version") or CONFIG_SCHEMA_VERSION
    )
    runtime["name"] = display_name
    runtime["config_name"] = display_name
    runtime["capsule_id"] = runtime_context["capsule_id"]
    runtime["source"] = deepcopy(runtime_context["source"])
    runtime["frame_range"] = deepcopy(
        runtime_context.get("frame_range", {"start": 0, "stop": None, "step": 1})
    )
    runtime["sampling"] = deepcopy(
        runtime_context.get("sampling", {"rate_fps": 30.0})
    )

    output = runtime.setdefault("output", {})
    output.update(deepcopy(runtime_context.get("output", {})))
    output.setdefault("run_id", "auto")
    output.setdefault("config_snapshot_name", "config.json")
    output.setdefault("root_rot_order", "xyzw")
    output.setdefault("save_diagnostics_csv", False)
    return runtime


def list_configs(
    *,
    source_type: str,
    manufacturer: str,
    robot_variant: str,
    user_id: str = "local_user",
    stage: CONFIG_STAGE = "primary",
    include_archived: bool = False,
) -> list[ConfigRecord]:
    records: list[ConfigRecord] = []
    for scope in ("xenoma_standard", "personal", "workspace"):
        directory = config_directory(
            scope,
            source_type=source_type,
            manufacturer=manufacturer,
            robot_variant=robot_variant,
            user_id=user_id,
        )
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.json")):
            try:
                config = read_json(path)
            except ConfigStoreError:
                continue
            config_stage = inferred_stage(config)
            if config_stage != stage:
                continue
            record = _record(
                config, scope=scope, path=path,
                robot_variant=robot_variant, stage=config_stage,
            )
            if include_archived or record.status == "active":
                records.append(record)
    order = {"xenoma_standard": 0, "personal": 1, "workspace": 2}
    records.sort(key=lambda item: (order[item.scope], item.name.casefold()))
    return records


def load_config(
    *,
    scope: SCOPE,
    filename: str,
    source_type: str,
    manufacturer: str,
    robot_variant: str,
    user_id: str = "local_user",
    stage: CONFIG_STAGE = "primary",
) -> tuple[ConfigRecord, dict[str, Any]]:
    directory = config_directory(
        scope,
        source_type=source_type,
        manufacturer=manufacturer,
        robot_variant=robot_variant,
        user_id=user_id,
    )
    path = _config_path(directory, filename)
    config = read_json(path)
    config_stage = inferred_stage(config)
    if config_stage != stage:
        raise ConfigStoreError("Config not found for this retarget stage")
    record = _record(
        config, scope=scope, path=path,
        robot_variant=robot_variant, stage=config_stage,
    )
    normalized = deepcopy(config)
    normalized.setdefault("schema_version", CONFIG_SCHEMA_VERSION)
    normalized.setdefault("name", record.name)
    normalized.setdefault("retarget_stage", config_stage)
    normalized.update({
        key: value for key, value in record.as_dict().items()
        if key in {
            "config_id", "display_name", "scope", "owner_id", "target_robot",
            "version", "created_by", "source_config_id", "created_at",
            "updated_at", "status",
            "standard_key",
        }
    })
    return record, normalized


def safe_filename(name: str) -> str:
    normalized = unicodedata.normalize("NFKC", name).strip()
    stem = re.sub(r"\s+", "_", normalized)
    stem = INVALID_WINDOWS_FILENAME_RE.sub("", stem)
    stem = re.sub(r"[^\w.-]+", "_", stem, flags=re.UNICODE)
    stem = re.sub(r"_+", "_", stem).strip(" ._").lower()
    if not stem:
        stem = "config_" + hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:10]
    if stem.upper() in RESERVED_WINDOWS_NAMES:
        stem = f"config_{stem}"
    return stem[:120].rstrip(" .") + ".json"


def save_user_config(
    config: dict[str, Any],
    *,
    name: str,
    source_type: str,
    manufacturer: str,
    robot_variant: str,
    selected_scope: SCOPE | None = None,
    selected_filename: str | None = None,
    overwrite: bool = False,
    user_id: str = "local_user",
    stage: CONFIG_STAGE = "primary",
) -> tuple[ConfigRecord, dict[str, Any]]:
    display_name = name.strip()
    selected_normalized = canonical_scope(selected_scope) if selected_scope else None
    destination_scope = "workspace" if selected_normalized == "workspace" else "personal"
    destination_directory = config_directory(
        destination_scope,
        source_type=source_type,
        manufacturer=manufacturer,
        robot_variant=robot_variant,
        user_id=user_id,
    )
    current_path: Path | None = None
    if selected_normalized == destination_scope and selected_filename:
        current_path = _config_path(destination_directory, selected_filename)
    existing = read_json(current_path) if current_path and current_path.exists() else None
    destination = current_path or _unique_path(destination_directory, display_name)
    source_config_id = None if existing else config.get("config_id")
    shared = _with_metadata(
        config,
        name=display_name,
        stage=stage,
        scope=destination_scope,
        robot_variant=robot_variant,
        existing=existing,
        source_config_id=str(source_config_id) if source_config_id else None,
    )
    atomic_write_json(destination, shared)
    record = _record(
        shared,
        scope=destination_scope,
        path=destination,
        robot_variant=robot_variant,
        stage=stage,
    )
    return record, shared


def _unique_path(directory: Path, name: str) -> Path:
    filename = safe_filename(name)
    destination = _config_path(directory, filename)
    if not destination.exists():
        return destination
    digest = hashlib.sha256(name.encode("utf-8")).hexdigest()[:8]
    stem = f"{Path(filename).stem}_{digest}"
    destination = _config_path(directory, f"{stem}.json")
    suffix = 2
    while destination.exists():
        destination = _config_path(directory, f"{stem}_{suffix}.json")
        suffix += 1
    return destination


def publish_to_workspace(
    config: dict[str, Any],
    *,
    name: str,
    source_type: str,
    manufacturer: str,
    robot_variant: str,
    user_id: str = "local_user",
    stage: CONFIG_STAGE = "primary",
) -> tuple[ConfigRecord, dict[str, Any]]:
    directory = config_directory(
        "workspace",
        source_type=source_type,
        manufacturer=manufacturer,
        robot_variant=robot_variant,
        user_id=user_id,
    )
    destination = _unique_path(directory, name)
    shared = _with_metadata(
        config,
        name=name,
        stage=stage,
        scope="workspace",
        robot_variant=robot_variant,
        source_config_id=str(config.get("config_id") or "") or None,
    )
    atomic_write_json(destination, shared)
    record = _record(
        shared,
        scope="workspace",
        path=destination,
        robot_variant=robot_variant,
        stage=stage,
    )
    return record, shared


def archive_config(
    *,
    scope: SCOPE,
    filename: str,
    source_type: str,
    manufacturer: str,
    robot_variant: str,
    user_id: str = "local_user",
    stage: CONFIG_STAGE = "primary",
) -> ConfigRecord:
    normalized_scope = canonical_scope(scope)
    if normalized_scope not in {"personal", "workspace"}:
        raise ConfigStoreError("Only Personal or Workspace configs can be archived")
    directory = config_directory(
        normalized_scope,
        source_type=source_type,
        manufacturer=manufacturer,
        robot_variant=robot_variant,
        user_id=user_id,
    )
    path = _config_path(directory, filename)
    config = read_json(path)
    if inferred_stage(config) != stage:
        raise ConfigStoreError("Config not found for this retarget stage")
    config["status"] = "archived"
    config["version"] = max(1, int(config.get("version") or 1)) + 1
    config["updated_at"] = datetime.now(timezone.utc).isoformat()
    atomic_write_json(path, config)
    return _record(
        config,
        scope=normalized_scope,
        path=path,
        robot_variant=robot_variant,
        stage=stage,
    )


def replace_xenoma_standard(
    config: dict[str, Any],
    *,
    name: str,
    filename: str,
    source_type: str,
    manufacturer: str,
    robot_variant: str,
    user_id: str = "local_user",
    stage: CONFIG_STAGE = "primary",
) -> tuple[ConfigRecord, dict[str, Any], ConfigRecord]:
    """Create a new active Standard and retain the selected generation archived."""
    directory = config_directory(
        "xenoma_standard",
        source_type=source_type,
        manufacturer=manufacturer,
        robot_variant=robot_variant,
        user_id=user_id,
    )
    active_path = _config_path(directory, filename)
    with CONFIG_WRITE_LOCK:
        previous = read_json(active_path)
        if inferred_stage(previous) != stage:
            raise ConfigStoreError("Config not found for this retarget stage")
        previous_record = _record(
            previous, scope="xenoma_standard", path=active_path,
            robot_variant=robot_variant, stage=stage,
        )
        if previous_record.status != "active":
            raise ConfigStoreError("Only an active Xenoma Standard can be replaced")

        now = datetime.now(timezone.utc).isoformat()
        archived = deepcopy(previous)
        archived.update({
            "config_id": previous_record.config_id,
            "display_name": previous_record.display_name,
            "scope": "xenoma_standard",
            "owner_id": previous_record.owner_id,
            "target_robot": previous_record.target_robot,
            "version": previous_record.version,
            "created_by": previous_record.created_by,
            "source_config_id": previous_record.source_config_id,
            "created_at": previous_record.created_at,
            "status": "archived",
            "updated_at": now,
            "standard_key": previous_record.standard_key or (
                f"{manufacturer}_{robot_variant}_{stage}"
            ),
        })
        archive_path = _unique_path(
            directory, f"archived_{previous_record.config_id}"
        )
        atomic_write_json(archive_path, archived)

        replacement = _with_metadata(
            config,
            name=name,
            stage=stage,
            scope="xenoma_standard",
            robot_variant=robot_variant,
            source_config_id=previous_record.config_id,
        )
        replacement.update({
            "version": previous_record.version + 1,
            "created_at": now,
            "updated_at": now,
            "created_by": DEVELOPMENT_USER.user_id,
            "status": "active",
            "standard_key": previous_record.standard_key or (
                f"{manufacturer}_{robot_variant}_{stage}"
            ),
        })
        atomic_write_json(active_path, replacement)

    replacement_record = _record(
        replacement, scope="xenoma_standard", path=active_path,
        robot_variant=robot_variant, stage=stage,
    )
    archived_record = _record(
        archived, scope="xenoma_standard", path=archive_path,
        robot_variant=robot_variant, stage=stage,
    )
    return replacement_record, replacement, archived_record
