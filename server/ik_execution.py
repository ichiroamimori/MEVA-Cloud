from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from server.ik_contract import IKRequest, mujoco_asset_fingerprint, sha256_file
from server.robot_registry import apply_variant_to_runtime_config, resolve_variant


PROGRESS_RE = re.compile(r"^\[(\d+)/(\d+)\] frame (\d+)")


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


def _prepare_config(
    request: IKRequest, package_directory: Path, execution_directory: Path,
    repository_root: Path,
) -> tuple[Path, Path]:
    source_config = package_directory / request.config_path
    cfg = _load_config(source_config)
    try:
        record = resolve_variant(
            request.robot["variant"],
            manufacturer_id=request.robot["manufacturer"],
            robot_id=request.robot["robot_id"],
            root=repository_root,
        )
        if sha256_file(record.manifest_path) != request.robot["manifest_sha256"]:
            raise IKExecutionError(
                "robot_model_load_failure",
                "Remote robot manifest differs from the MEVA Cloud manifest",
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
        cfg = apply_variant_to_runtime_config(cfg, record, root=repository_root)
    except IKExecutionError:
        raise
    except Exception as exc:
        raise IKExecutionError("robot_model_load_failure", str(exc)) from exc

    if request.stage == "primary":
        source = package_directory / request.file_for_role("source")["path"]
        cfg.setdefault("source", {})["file"] = _relative_to_repository(source, repository_root)
        run_id = str(cfg.get("output", {}).get("run_id") or "")
        if not run_id:
            raise IKExecutionError("config_error", "Primary output.run_id is required")
        cfg.setdefault("output", {})["overwrite_existing"] = False
        config_directory = execution_directory
        output_directory = execution_directory / run_id
        config_name = f".{run_id}_request_config.json"
    else:
        primary_run_id = str(cfg.get("primary_run_id") or "")
        main_id = str(cfg.get("main_id") or "")
        if not primary_run_id or not main_id:
            raise IKExecutionError("config_error", "Main primary_run_id and main_id are required")
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
) -> IKExecutionResult:
    """Run one existing Primary or Main CLI without changing solver behavior."""
    execution_directory.mkdir(parents=True, exist_ok=False)
    config_path, output_directory = _prepare_config(
        request, package_directory, execution_directory, repository_root,
    )
    script = repository_root / "server" / "retarget" / (
        "primary_retarget.py" if request.stage == "primary" else "main_retarget.py"
    )
    command = [sys.executable, "-u", str(script), str(config_path)]
    if request.stage == "primary" and request.iteration_diagnostics:
        command.append("--iteration-diagnostics")
    try:
        process = subprocess.Popen(
            command,
            cwd=str(repository_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )
    except OSError as exc:
        raise IKExecutionError("ik_solver_failure", f"Could not start IK process: {exc}") from exc

    logs: list[str] = []
    assert process.stdout is not None
    for raw_line in process.stdout:
        line = raw_line.rstrip()
        if line:
            logs.append(line)
            if len(logs) > 1000:
                logs = logs[-1000:]
        match = PROGRESS_RE.match(line.strip())
        if match and progress_callback is not None:
            progress_callback(*(int(value) for value in match.groups()))
    return_code = process.wait()
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
