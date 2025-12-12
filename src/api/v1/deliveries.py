from fastapi import APIRouter, Body, Depends

from db.dependencies.auth import ADMIN_ROLE, get_current_user, require_roles
from db.models.users import User
from schemas.delivery import DeliveryOutScheme
from services.delivery_service import DeliveryService, get_delivery_service
from utils.shortcuts import get_or_404

router = APIRouter(prefix="/deliveries", tags=["Deliveries"])


@router.get("/order/{order_id}", response_model=DeliveryOutScheme)
async def get_delivery(
    order_id: int, service: DeliveryService = Depends(get_delivery_service)
):
    delivery = await get_or_404(
        service.get_delivery_for_order(order_id), "Order not found"
    )
    return delivery


@router.post(
    "/{order_id}/assign",
    response_model=dict,
    dependencies=[Depends(require_roles(ADMIN_ROLE))],
)
async def assign_courier(
    order_id: int,
    courier_id: int = Body(..., embed=True),
    service: DeliveryService = Depends(get_delivery_service),
):
    courier = await service.assign_courier(order_id, courier_id)
    return {"status": "assigned", "courier_id": courier.id}


@router.post("/{order_id}/status", response_model=dict)
async def update_status(
    order_id: int,
    status: str = Body(..., embed=True),
    service: DeliveryService = Depends(get_delivery_service),
    current_user: User = Depends(get_current_user),
):
    # here you could restrict to courier or admin depending on business logic
    delivery = await service.update_status(order_id, status)
    return {"status": delivery.status}
