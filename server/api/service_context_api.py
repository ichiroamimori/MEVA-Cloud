from fastapi import APIRouter

from server.service_context import public_service_context


router = APIRouter(prefix="/api/service-context", tags=["service-context"])


@router.get("")
def get_service_context() -> dict:
    return public_service_context()
