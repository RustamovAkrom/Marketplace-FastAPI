from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies.sessions import get_db_session
from schemas.order import CheckoutRequestScheme, OrderOutScheme
from services.order_service import OrderService
from utils.shortcuts import get_or_404

router = APIRouter(prefix="/orders", tags=["Orders"])


async def get_order_service(
    session: AsyncSession = Depends(get_db_session),
) -> OrderService:
    return OrderService(session)


@router.post(
    "/checkout", response_model=OrderOutScheme, status_code=status.HTTP_201_CREATED
)
async def checkout(
    payload: CheckoutRequestScheme, service: OrderService = Depends(get_order_service)
):
    order = await service.checkout(
        user_id=payload.user_id,
        address_id=payload.address_id,
        delivery_id=payload.delivery_id,
        items=payload.items,
        promo_code=payload.promo_code,
        currency=payload.currency,
    )
    return order


@router.post("/{order_id}/pay", status_code=status.HTTP_200_OK)
async def pay_success(
    order_id: int, service: OrderService = Depends(get_order_service)
):
    order = await service.on_payment_success(order_id)
    return {"detail": "Payment confirmed", "order_id": order.id}


@router.post("/{order_id}/cancel", status_code=status.HTTP_200_OK)
async def cancel(order_id: int, service: OrderService = Depends(get_order_service)):
    order = await service.cancel_order(order_id)
    return {"detail": "Order cancelled", "order_id": order.id}


@router.get("/{order_id}", response_model=OrderOutScheme)
async def get_order(order_id: int, service: OrderService = Depends(get_order_service)):
    order = await service.crud.get_order(order_id)
    order = await get_or_404(order, "Order not found")
    return order
