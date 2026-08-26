from __future__ import annotations

import hashlib
import json
import os
import re
import unicodedata
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal


CONFIG_SCHEMA_VERSION = "1.0"
SCOPE = Literal["xenoma", "user"]
CONFIG_STAGE = Literal["primary", "main"]
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

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "scope": self.scope,
            "filename": self.filename,
            "writable": self.writable,
            "legacy": self.legacy,
            "schema_version": self.schema_version,
            "stage": self.stage,
        }


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
    if user_id != "local_user":
        raise ConfigStoreError("Only local_user configs are supported")
    if scope == "xenoma":
        base = xenoma_assets_root() / "configs"
    elif scope == "user":
        base = workspace_root() / "users" / user_id / "retarget_assets" / "configs"
    else:
        raise ConfigStoreError("Invalid config scope")
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
    for key in ("capsule_id", "source", "frame_range", "sampling", "offsets"):
        shared.pop(key, None)
    for key in (
        "primary_run_id", "main_id", "primary_post_csv", "main_input_csv",
        "main_calibration", "main_target_analysis",
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
) -> list[ConfigRecord]:
    records: list[ConfigRecord] = []
    for scope in ("xenoma", "user"):
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
            records.append(ConfigRecord(
                name=inferred_name(config, path.name),
                scope=scope,
                filename=path.name,
                writable=scope == "user",
                legacy="schema_version" not in config or "name" not in config,
                schema_version=str(config.get("schema_version") or CONFIG_SCHEMA_VERSION),
                stage=config_stage,
            ))
    records.sort(key=lambda item: (0 if item.scope == "xenoma" else 1, item.name.casefold()))
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
    record = ConfigRecord(
        name=inferred_name(config, path.name),
        scope=scope,
        filename=path.name,
        writable=scope == "user",
        legacy="schema_version" not in config or "name" not in config,
        schema_version=str(config.get("schema_version") or CONFIG_SCHEMA_VERSION),
        stage=config_stage,
    )
    normalized = deepcopy(config)
    normalized.setdefault("schema_version", CONFIG_SCHEMA_VERSION)
    normalized.setdefault("name", record.name)
    normalized.setdefault("retarget_stage", config_stage)
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
    shared = normalized_shared_config(config, name=display_name, stage=stage)
    records = list_configs(
        source_type=source_type,
        manufacturer=manufacturer,
        robot_variant=robot_variant,
        user_id=user_id,
        stage=stage,
    )
    same_name = [item for item in records if item.name.casefold() == display_name.casefold()]
    xenoma_match = next((item for item in same_name if item.scope == "xenoma"), None)
    if xenoma_match:
        raise ConfigNameCollision(
            "Xenoma-provided config cannot be overwritten. Please save with a different name.",
            filename=xenoma_match.filename,
        )

    user_directory = config_directory(
        "user",
        source_type=source_type,
        manufacturer=manufacturer,
        robot_variant=robot_variant,
        user_id=user_id,
    )
    current_path: Path | None = None
    if selected_scope == "user" and selected_filename:
        current_path = _config_path(user_directory, selected_filename)

    user_match = next((item for item in same_name if item.scope == "user"), None)
    if user_match:
        matched_path = _config_path(user_directory, user_match.filename)
        same_selected_file = current_path is not None and matched_path == current_path
        if not same_selected_file and not overwrite:
            raise ConfigNameCollision(
                "A User config with this name already exists.",
                filename=user_match.filename,
            )
        destination = matched_path
    elif current_path is not None:
        try:
            current = read_json(current_path)
            same_current_name = inferred_name(current, current_path.name).casefold() == display_name.casefold()
        except ConfigStoreError:
            same_current_name = False
        destination = current_path if same_current_name else _unique_path(user_directory, display_name)
    else:
        destination = _unique_path(user_directory, display_name)

    atomic_write_json(destination, shared)
    record = ConfigRecord(
        name=display_name,
        scope="user",
        filename=destination.name,
        writable=True,
        legacy=False,
        schema_version=CONFIG_SCHEMA_VERSION,
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
