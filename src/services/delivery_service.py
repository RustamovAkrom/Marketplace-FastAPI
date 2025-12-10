from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.order import OrderCRUD
from db.dependencies.sessions import get_db_session
from db.models.couriers import Courier, CourierStatus
from db.models.delivery import Delivery, DeliveryStatus


class DeliveryService:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session
        self.crud = OrderCRUD(session)  # OrderCRUD contains create_delivery and helpers

    async def get_delivery_for_order(self, order_id: int) -> Optional[Delivery]:
        order = await self.crud.get_order(order_id)
        if not order:
            raise HTTPException(404, "Order not found")
        return order.delivery

    async def assign_courier(self, order_id: int, courier_id: int) -> Optional[Courier]:
        # delegate to OrderService.assign_courier or implement similar logic
        order = await self.crud.get_order(order_id)
        if not order:
            raise HTTPException(404, "Order not found")
        delivery = order.delivery
        if not delivery:
            raise HTTPException(404, "Delivery not found for order")

        courier = await self.session.get(Courier, courier_id)
        if not courier or not courier.is_available or not courier.is_verified:
            raise HTTPException(400, "Courier not available")

        delivery.courier_id = courier.id
        delivery.status = DeliveryStatus.assigned.value
        delivery.assigned_at = datetime.utcnow()
        self.session.add(delivery)

        courier.is_available = False
        courier.status = CourierStatus.busy.value
        self.session.add(courier)

        await self.session.commit()
        await self.session.refresh(delivery)
        await self.session.refresh(courier)
        return courier

    async def update_status(self, order_id: int, status: str) -> Delivery:
        order = await self.crud.get_order(order_id)
        if not order or not order.delivery:
            raise HTTPException(404, "Delivery not found")
        delivery = order.delivery
        delivery.status = status
        if status == DeliveryStatus.delivered.value:
            delivery.delivered_at = datetime.utcnow()
        self.session.add(delivery)
        await self.session.commit()
        await self.session.refresh(delivery)
        return delivery
