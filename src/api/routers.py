from fastapi import APIRouter

from api.v1.user import router as user_router
from core.config import settings

api_router = APIRouter(
    prefix=f"{settings.API_V1_PREFIX}",
)

api_router.include_router(user_router, prefix="/auth", tags=["Auth"])


__all__ = ("api_router",)
