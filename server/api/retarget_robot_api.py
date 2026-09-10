from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Literal

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from server.robot_registry import (
    RobotRegistryError,
    RobotVariant,
    apply_variant_to_runtime_config,
    public_catalog,
    resolve_variant,
    validate_retarget_config,
    variant_retargeting_metadata,
)


router = APIRouter()


def repo_root() -> Path:
    # server/api/retarget_api.py -> repo root
    return Path(__file__).resolve().parents[2]

def _registered_variant(
    robot_variant: str,
    *,
    manufacturer: str | None = None,
    robot_id: str | None = None,
) -> RobotVariant:
    try:
        return resolve_variant(
            robot_variant,
            manufacturer_id=manufacturer,
            robot_id=robot_id,
            root=repo_root(),
        )
    except RobotRegistryError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

def _runtime_robot_config(config: dict[str, Any], record: RobotVariant) -> dict[str, Any]:
    return apply_variant_to_runtime_config(config, record, root=repo_root())

def _assert_config_robot(config: dict[str, Any], record: RobotVariant) -> None:
    robot = config.get("robot")
    if not isinstance(robot, dict):
        raise HTTPException(status_code=400, detail="Config robot identity is required")
    actual = (
        str(robot.get("manufacturer") or ""),
        str(robot.get("model") or ""),
        str(robot.get("variant") or ""),
    )
    expected = (record.manufacturer_id, record.robot_id, record.variant_id)
    if actual != expected:
        raise HTTPException(
            status_code=400,
            detail=(
                "Config Robot identity mismatch: "
                f"expected {expected[0]}/{expected[1]}/{expected[2]}, "
                f"found {actual[0]}/{actual[1]}/{actual[2]}"
            ),
        )

def _validate_retarget_config_or_http(
    record: RobotVariant, config: dict[str, Any]
) -> dict[str, Any]:
    try:
        return validate_retarget_config(record, config)
    except RobotRegistryError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

def _sole_geom_descriptors(config: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Expose the manifest-defined Foot support points to the existing UI."""
    robot = config.get("robot", {})
    contacts = robot.get("foot_contacts") if isinstance(robot, dict) else None
    if not isinstance(contacts, dict):
        contacts = None
    if contacts is None:
        try:
            variant = resolve_variant(
                str(robot.get("variant") or ""),
                manufacturer_id=str(robot.get("manufacturer") or "") or None,
                robot_id=str(robot.get("model") or "") or None,
                root=repo_root(),
            )
            value = variant_retargeting_metadata(variant).get("foot_contacts")
            contacts = value if isinstance(value, dict) else None
        except RobotRegistryError:
            contacts = None
    result: dict[str, list[dict[str, Any]]] = {"left": [], "right": []}
    if contacts is None:
        return result
    for side in ("left", "right"):
        definition = contacts.get(side)
        if not isinstance(definition, dict):
            continue
        points = definition.get("support_points")
        if not isinstance(points, list):
            continue
        for index, point in enumerate(points):
            if not isinstance(point, dict):
                continue
            position = point.get("local_position")
            if not isinstance(position, list) or len(position) != 3:
                continue
            name = str(point.get("name") or f"support_{index + 1}")
            result[side].append({
                "index": index,
                "name": name,
                "display": f"{side}_{name}",
                "pos": " ".join(f"{float(value):g}" for value in position),
                "size": "",
                "body": str(definition.get("body") or ""),
                "source_geom": str(definition.get("source_geom") or ""),
                "generation_method": str(
                    definition.get("generation_method") or "explicit"
                ),
            })
    return result

def _manifest_robot_foot_to_ground_offset(config: dict[str, Any]) -> float | None:
    """Read the installer-confirmed Robot Foot offset from manifest metadata."""
    robot = config.get("robot", {})
    contacts = robot.get("foot_contacts") if isinstance(robot, dict) else None
    if not isinstance(contacts, dict):
        try:
            variant = resolve_variant(
                str(robot.get("variant") or ""),
                manufacturer_id=str(robot.get("manufacturer") or "") or None,
                robot_id=str(robot.get("model") or "") or None,
                root=repo_root(),
            )
            value = variant_retargeting_metadata(variant).get("foot_contacts")
            contacts = value if isinstance(value, dict) else None
        except RobotRegistryError:
            contacts = None
    if not isinstance(contacts, dict):
        return None
    try:
        value = float(contacts["robot_foot_to_ground_offset_m"])
    except (KeyError, TypeError, ValueError):
        return None
    return value if math.isfinite(value) and value >= 0.0 else None

@router.get("/robots")
def get_robot_catalog():
    try:
        return public_catalog(repo_root())
    except RobotRegistryError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/robots/viewer/launch")
def launch_registered_robot_viewer(
    robot_variant: str,
    manufacturer: str,
    robot_id: str,
    capsule_id: str,
    run_id: str,
    stage: Literal["primary", "main"] = "primary",
    main_id: str = "legacy",
    user_id: str = "local_user",
):
    record = _registered_variant(
        robot_variant, manufacturer=manufacturer, robot_id=robot_id,
    )
    from server.api.retarget_artifact_api import (
        MAIN_ID_RE, RUN_RE, resolve_main_result_dir, robot_dir,
    )
    from server.api.capsule_api import CAPSULE_ID_RE
    from server.robot_viewer_launcher import launch_robot_viewer

    if not CAPSULE_ID_RE.fullmatch(capsule_id) or user_id != "local_user":
        raise HTTPException(status_code=400, detail="Invalid Viewer context")
    if not RUN_RE.fullmatch(run_id):
        raise HTTPException(status_code=400, detail="Retargeted Data IDを選択してください。")
    run = robot_dir(capsule_id, robot_variant, user_id) / run_id
    if stage == "main":
        if main_id == "new":
            raise HTTPException(status_code=400, detail="Main Resultを選択してください。")
        if main_id == "legacy":
            result_dir, file_id = run, run_id
        else:
            if not MAIN_ID_RE.fullmatch(main_id) or not main_id.startswith(f"{run_id}-"):
                raise HTTPException(status_code=400, detail="Invalid main_id")
            result_dir = resolve_main_result_dir(
                capsule_id, robot_variant, run_id, main_id, user_id,
            )
            file_id = main_id
        candidates = (
            result_dir / f"{file_id}_main.pkl",
            result_dir / f"{file_id}_main.npz",
        )
    else:
        candidates = (
            run / f"{run_id}_primary.pkl",
            run / f"{run_id}_primary.npz",
            run / "primary.pkl",
        )
    motion = next((path for path in candidates if path.is_file()), None)
    if motion is None:
        raise HTTPException(
            status_code=404,
            detail=f"{stage.title()} motionが見つかりません。Retargetingを実行してください。",
        )

    try:
        pid = launch_robot_viewer(record, motion)
    except (FileNotFoundError, OSError, RuntimeError) as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {
        "ok": True, "pid": pid, "robot_variant": record.variant_id,
        "stage": stage, "motion_file": motion.name,
    }


@router.get("/robots/viewer/browser/config")
def get_browser_robot_viewer_config(
    robot_variant: str,
    manufacturer: str,
    robot_id: str,
    capsule_id: str | None = None,
    run_id: str | None = None,
    stage: Literal["primary", "main"] = "primary",
    main_id: str = "legacy",
    user_id: str = "local_user",
):
    """Describe one registered MJCF and its transitive browser-loadable assets."""
    record = _registered_variant(
        robot_variant, manufacturer=manufacturer, robot_id=robot_id,
    )
    motion_query = None
    if any(value is not None for value in (capsule_id, run_id)):
        from server.api.capsule_api import CAPSULE_ID_RE
        from server.api.retarget_artifact_api import MAIN_ID_RE, RUN_RE

        if (
            user_id != "local_user"
            or not capsule_id
            or not CAPSULE_ID_RE.fullmatch(capsule_id)
            or not run_id
            or not RUN_RE.fullmatch(run_id)
        ):
            raise HTTPException(status_code=400, detail="Invalid Viewer motion context")
        if stage == "main" and main_id not in {"legacy"} and (
            not MAIN_ID_RE.fullmatch(main_id) or not main_id.startswith(f"{run_id}-")
        ):
            raise HTTPException(status_code=400, detail="Invalid main_id")
        motion_query = {
            "capsule_id": capsule_id,
            "run_id": run_id,
            "robot_variant": robot_variant,
            "stage": stage,
            "main_id": main_id,
            "user_id": user_id,
        }
    from server.robot_browser_viewer import (
        RobotBrowserViewerError, browser_viewer_config,
    )
    try:
        return browser_viewer_config(record, motion_query=motion_query)
    except (OSError, RobotBrowserViewerError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/robots/viewer/browser/asset")
def get_browser_robot_viewer_asset(
    path: str,
    robot_variant: str,
    manufacturer: str,
    robot_id: str,
):
    record = _registered_variant(
        robot_variant, manufacturer=manufacturer, robot_id=robot_id,
    )
    from server.robot_browser_viewer import (
        RobotBrowserViewerError, resolve_browser_asset,
    )
    try:
        asset = resolve_browser_asset(record, path)
    except (OSError, RobotBrowserViewerError) as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return FileResponse(
        asset,
        filename=asset.name,
        headers={"Cache-Control": "public, max-age=3600"},
    )
