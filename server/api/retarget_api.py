"""Aggregate the domain-specific Retargeting API routers."""
from fastapi import APIRouter

from server.api.retarget_artifact_api import router as artifact_router
from server.api.retarget_config_api import router as config_router
from server.api.retarget_robot_api import router as robot_router
from server.api.retarget_run_api import router as run_router
from server.api.retarget_viewer_api import router as viewer_router


router = APIRouter(prefix="/api/retarget", tags=["retarget"])
router.include_router(robot_router)
router.include_router(config_router)
router.include_router(artifact_router)
router.include_router(run_router)
router.include_router(viewer_router)
