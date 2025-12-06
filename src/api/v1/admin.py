from fastapi import APIRouter, Depends

from db.dependencies.auth import require_admin
from db.models.users import User

router = APIRouter()


@router.get("/admin/stats")
async def admin_stats(admin_user: User = Depends(require_admin)):
    return {"status": "ok", "admin": admin_user.username}


__all__ = ("router",)
