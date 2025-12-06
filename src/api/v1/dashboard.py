from fastapi import APIRouter, Depends

from db.dependencies.auth import get_current_user
from db.models.users import User
from schemas.user import UserOutScheme

router = APIRouter()


@router.get("/me", response_model=UserOutScheme)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/dashboard")
async def dashboard(current_user: User = Depends(get_current_user)):
    orders_count = 0
    total_spent = 0
    recent_orders = 0

    return {
        "message": f"Welcome, {current_user.username}",
        "orders_count": orders_count,
        "total_spent": total_spent,
        "recent_orders": recent_orders,
    }


# TODO: Create Dashboard Service
# @router.get("/dashboard")
# async def dashboard(current_user: User = Depends(get_current_user), dashboard_service: DashboardService = Depends(get_dashboard_service)):
#     return await dashboard_service.get_user_stats(current_user.id)


__all__ = ("router",)
