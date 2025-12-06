from fastapi import APIRouter

from api.v1 import (  # noqa
    admin,
    auth,
    category,
    dashboard,
    social_auth,
    users,
)
from core.config import settings

api_router = APIRouter(
    prefix=f"{settings.API_V1_PREFIX}",
)

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(
    social_auth.router, prefix="/social_auth", tags=["Social Auth"]
)
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(category.router, prefix="/categories", tags=["Categories"])

__all__ = ("api_router",)
