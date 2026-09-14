from __future__ import annotations

import json
import os
import re
import sys
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from server.ik_contract import (
    IKRequest,
    canonical_value_sha256,
    mujoco_asset_fingerprint,
    robot_manifest_matches,
    sha256_file,
)
from server.managed_process import (
    ManagedProcessCancelled,
    ManagedProcessTimeout,
    run_managed_process,
)
from server.robot_registry import apply_variant_to_runtime_config, resolve_variant
from server.retarget.viewer_data import FORMAT_VERSION, read_viewer_bin


PROGRESS_RE = re.compile(r"^\[(\d+)/(\d+)\] frame (\d+)")
RUN_ID_RE = re.compile(r"^\d{10}$")
MAIN_ID_RE = re.compile(r"^(\d{10})-(\d{2})$")


class IKExecutionError(RuntimeError):
    def __init__(
        self, code: str, message: str, *, logs: list[str] | None = None,
        output_directory: Path | None = None,
    ):
        super().__init__(message)
        self.code = code
        self.logs = logs or []
        self.output_directory = output_directory


@dataclass(frozen=True)
class IKExecutionResult:
    output_directory: Path
    logs: tuple[str, ...]


def _relative_to_repository(path: Path, repository_root: Path) -> str:
    try:
        return path.resolve().relative_to(repository_root.resolve()).as_posix()
    except ValueError as exc:
        raise IKExecutionError("input_load_failure", "Worker input is outside repository workspace") from exc


def _load_config(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IKExecutionError("config_error", f"Could not load IK config: {exc}") from exc
    if not isinstance(value, dict):
        raise IKExecutionError("config_error", "IK config must be a JSON object")
    return value


def _validated_output_ids(request: IKRequest, cfg: dict) -> tuple[str, str | None]:
    if request.stage == "primary":
        run_id = str(cfg.get("output", {}).get("run_id") or "")
        if not RUN_ID_RE.fullmatch(run_id):
            raise IKExecutionError("config_error", "Invalid Primary output.run_id")
        return run_id, None
    primary_run_id = str(cfg.get("primary_run_id") or "")
    main_id = str(cfg.get("main_id") or "")
    match = MAIN_ID_RE.fullmatch(main_id)
    if (
        not RUN_ID_RE.fullmatch(primary_run_id)
        or not match
        or match.group(1) != primary_run_id
    ):
        raise IKExecutionError("config_error", "Invalid Main primary_run_id or main_id")
    return primary_run_id, main_id


def _prepare_config(
    request: IKRequest, package_directory: Path, execution_directory: Path,
    repository_root: Path,
) -> tuple[Path, Path]:
    source_config = package_directory / request.config_path
    cfg = _load_config(source_config)
    primary_run_id, validated_main_id = _validated_output_ids(request, cfg)
    try:
        record = resolve_variant(
            request.robot["variant"],
            manufacturer_id=request.robot["manufacturer"],
            robot_id=request.robot["robot_id"],
            root=repository_root,
        )
        if not robot_manifest_matches(record.manifest_path, request.robot):
            raise IKExecutionError(
                "robot_model_load_failure",
                "Remote robot manifest content differs from the MEVA Cloud manifest",
            )
        if sha256_file(record.model_path) != request.robot["model_sha256"]:
            raise IKExecutionError(
                "robot_model_load_failure",
                "Remote robot MJCF differs from the MEVA Cloud MJCF",
            )
        if (
            mujoco_asset_fingerprint(record.model_path, record.robot_directory)
            != request.robot["asset_bundle_sha256"]
        ):
            raise IKExecutionError(
                "robot_model_load_failure",
                "Remote MuJoCo mesh/texture asset bundle differs from MEVA Cloud",
            )
        if record.meva_offset_policy != request.robot.get("offset_policy"):
            raise IKExecutionError(
                "robot_model_load_failure",
                "Remote Robot approved Offset policy differs from MEVA Cloud",
            )
        if record.meva_offset_policy == "missing":
            raise IKExecutionError(
                "robot_model_load_failure",
                "Robot manifest does not declare a production MEVA Offset policy",
            )
        if record.meva_offset_policy == "approved":
            offset_path = record.approved_meva_offset_path
            expected_sha = request.robot.get("offset_asset_sha256")
            if (
                offset_path is None
                or not offset_path.is_file()
                or record.approved_meva_offset_sha256 != expected_sha
                or sha256_file(offset_path) != expected_sha
            ):
                raise IKExecutionError(
                    "robot_model_load_failure",
                    "Remote approved MEVA Offset asset differs from MEVA Cloud",
                )
            offset_asset = _load_config(offset_path)
            if (
                str(offset_asset.get("algorithm") or "")
                != request.robot.get("offset_algorithm")
                or canonical_value_sha256(offset_asset.get("fingerprint"))
                != request.robot.get("offset_fingerprint_sha256")
            ):
                raise IKExecutionError(
                    "robot_model_load_failure",
                    "Remote approved MEVA Offset provenance differs from MEVA Cloud",
                )
        cfg = apply_variant_to_runtime_config(cfg, record, root=repository_root)
    except IKExecutionError:
        raise
    except Exception as exc:
        raise IKExecutionError("robot_model_load_failure", str(exc)) from exc

    if request.stage == "primary":
        source = package_directory / request.file_for_role("source")["path"]
        if source.suffix.lower() != ".bin":
            raise IKExecutionError(
                "input_load_failure", "Remote Primary requires a MEVA BIN input",
            )
        try:
            bin_header, _ = read_viewer_bin(source)
        except (OSError, ValueError, KeyError) as exc:
            raise IKExecutionError(
                "input_load_failure", f"Could not load MEVA BIN: {exc}",
            ) from exc
        if (
            bin_header.get("kind") != "meva"
            or int(bin_header.get("format_version", 0)) < FORMAT_VERSION
        ):
            raise IKExecutionError("input_load_failure", "Unsupported MEVA BIN format")
        capsule_id = str(bin_header.get("capsule_id") or "")
        if not RUN_ID_RE.fullmatch(capsule_id):
            raise IKExecutionError("input_load_failure", "MEVA BIN has an invalid Capsule ID")
        cfg["capsule_id"] = capsule_id
        job = cfg.setdefault("retarget_job", {})
        if isinstance(job, dict):
            job["capsule_id"] = capsule_id
        cfg.setdefault("source", {})["file"] = _relative_to_repository(source, repository_root)
        cfg["source"].pop("bvh", None)
        run_id = primary_run_id
        cfg.setdefault("output", {})["overwrite_existing"] = False
        config_directory = execution_directory
        output_directory = execution_directory / run_id
        config_name = f".{run_id}_request_config.json"
    else:
        main_id = validated_main_id
        assert main_id is not None
        primary_directory = execution_directory / primary_run_id
        primary_directory.mkdir(parents=True, exist_ok=False)
        for role in ("primary_motion", "primary_target"):
            source = package_directory / request.file_for_role(role)["path"]
            target_name = (
                f"{primary_run_id}_primary{source.suffix.lower()}" if role == "primary_motion"
                else f"{primary_run_id}_primary_target.npz"
            )
            target = primary_directory / target_name
            target.write_bytes(source.read_bytes())
        config_directory = primary_directory / f".{main_id}.remote.staging"
        config_directory.mkdir(parents=False, exist_ok=False)
        output_directory = config_directory
        config_name = f"{main_id}_main_config.json"

    config_path = config_directory / config_name
    config_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return config_path, output_directory


def run_python_ik(
    request: IKRequest,
    package_directory: Path,
    execution_directory: Path,
    repository_root: Path,
    progress_callback: Callable[[int, int, int], None] | None = None,
    cancel_event: threading.Event | None = None,
    timeout_sec: float | None = None,
) -> IKExecutionResult:
    """Run one existing Primary or Main CLI without changing solver behavior."""
    execution_directory.mkdir(parents=True, exist_ok=False)
    config_path, output_directory = _prepare_config(
        request, package_directory, execution_directory, repository_root,
    )
    module = (
        "server.retarget.primary_retarget"
        if request.stage == "primary"
        else "server.retarget.main_retarget"
    )
    command = [sys.executable, "-u", "-m", module, str(config_path)]
    if request.stage == "primary" and request.iteration_diagnostics:
        command.append("--iteration-diagnostics")
    logs: list[str] = []

    def process_line(line: str) -> None:
        match = PROGRESS_RE.match(line.strip())
        if match and progress_callback is not None:
            progress_callback(*(int(value) for value in match.groups()))

    try:
        return_code, logs = run_managed_process(
            command,
            cwd=repository_root,
            cancel_event=cancel_event,
            timeout_sec=(
                timeout_sec
                if timeout_sec is not None
                else float(os.environ.get("MEVA_IK_JOB_TIMEOUT_SEC", "7200"))
            ),
            line_callback=process_line,
            log_limit=1000,
        )
    except ManagedProcessCancelled as exc:
        raise IKExecutionError(
            "cancelled", str(exc), logs=logs, output_directory=output_directory,
        ) from exc
    except ManagedProcessTimeout as exc:
        raise IKExecutionError(
            "timeout", str(exc), logs=logs, output_directory=output_directory,
        ) from exc
    except OSError as exc:
        raise IKExecutionError(
            "ik_solver_failure", f"Could not start IK process: {exc}"
        ) from exc
    if return_code != 0:
        joined = "\n".join(logs[-120:]).lower()
        if any(value in joined for value in ("xml error", "could not open file", "mesh", "mjmodel")):
            error_code = "robot_model_load_failure"
        elif any(value in joined for value in ("permissionerror", "no space left", "write")):
            error_code = "output_write_failure"
        elif any(value in joined for value in ("filenotfounderror", "could not load", "input")):
            error_code = "input_load_failure"
        elif any(value in joined for value in ("keyerror", "config_error", "invalid config")):
            error_code = "config_error"
        else:
            error_code = "ik_solver_failure"
        raise IKExecutionError(
            error_code,
            f"{request.stage.capitalize()} IK process exited with code {return_code}",
            logs=logs,
            output_directory=output_directory,
        )
    if not output_directory.is_dir():
        raise IKExecutionError("output_write_failure", "IK output directory was not created", logs=logs)
    return IKExecutionResult(output_directory=output_directory, logs=tuple(logs))
