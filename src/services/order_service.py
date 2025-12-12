from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.order import OrderCRUD
from db.dependencies.sessions import get_db_session
from db.models.couriers import Courier, CourierStatus
from db.models.delivery import DeliveryStatus
from db.models.orders import Order, OrderItem, OrderStatus
from db.models.products import ProductVariant


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.crud = OrderCRUD(session)

    async def checkout(
        self,
        user_id: int,
        address_id: int,
        items: List[OrderItem],
        promo_code: Optional[str] = None,
        currency: str = "USD",
    ) -> Order:
        if not items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        total: float = 0.0
        variants_cache: Dict[int, ProductVariant] = {}

        for it in items:
            variant: ProductVariant | None = await self.crud.get_variant(it.variant_id)
            if not variant:
                raise HTTPException(
                    status_code=404, detail=f"Viariant {it.variant_id} not found"
                )
            if variant.stock < it.quantity:
                raise HTTPException(
                    status_code=404,
                    detail=f"Not enough stock for variant {variant.sku}",
                )
            total += float(variant.price) * it.quantity
            variants_cache[it.variant_id] = variant

        # 2. Apply promo code
        discount: float = 0.0
        if promo_code:
            promo = await self.crud.get_promo_by_code(promo_code)
            if promo:
                now = datetime.now(timezone.utc)
                if (promo.valid_from and now < promo.valid_from) or (
                    promo.valid_to and now > promo.valid_to
                ):
                    raise HTTPException(status_code=400, detail="Promo code not valid")

                if promo.discount_percent:
                    discount = total * (promo.discount_percent / 100)
                else:
                    discount = float(promo.discount_amount or 0)
            else:
                raise HTTPException(status_code=404, detail="Promo code not found")

        final_total: float = max(0.0, total - discount)

        # 3. Create order and items; **reverse stock by decrementing**
        order = await self.crud.create_order(user_id, final_total, currency)
        # flush didn't commit; order.id available after flush
        await self.session.flush()
        # 4. Create order items
        for it in items:
            variant = variants_cache[it.variant_id]
            await self.crud.create_order_item(
                order.id, variant.id, it.quantity, float(variant.price)
            )
            # reverse stock
            variant.stock = variant.stock - it.quantity
            self.session.add(variant)

        # create delivery record (order -> delivery) (courier assignment deferred)
        delivery = await self.crud.create_delivery(order.id, None, address_id)

        # commit everything
        await self.crud.commit()
        await self.crud.refresh(order)
        await self.crud.refresh(delivery)

        return order

    async def on_payment_success(self, order_id: int):
        order = await self.crud.get_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if order.status != OrderStatus.PENDING_PAYMENT.value:
            raise HTTPException(
                status_code=400, detail="Order not in pending_payment state"
            )

        # mark paid
        await self.crud.set_order_status(order, OrderStatus.PAID.value)

        # assign courier automatically (best-effort)
        await self.assign_courier(order.id)

        return order

    async def cancel_order(self, order_id: int) -> Order:
        order = await self.crud.get_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        # restore stock for items
        for item in order.items:
            variant = await self.crud.get_variant(item.variant_id)
            if variant:
                variant.stock = variant.stock + item.quantity
                self.session.add(variant)

        # set status
        await self.crud.set_order_status(order, OrderStatus.CANCELLED.value)
        return order

    async def assign_courier(self, order_id: int) -> Optional[Courier]:
        # naive best-effort: pick first available & verified courier
        stmt = await self.session.execute(
            select(Courier).where(
                Courier.is_available.is_(True), Courier.is_verified.is_(True)
            )
        )
        courier = stmt.scalars().first()
        if not courier:
            return None

        # attach courier to delivery
        # fetch delivery
        order = await self.crud.get_order(order_id)
        if not order or not order.delivery:
            return None
        delivery = order.delivery
        delivery.courier_id = courier.id
        delivery.status = DeliveryStatus.assigned.value
        delivery.assigned_at = datetime.utcnow()
        self.session.add(delivery)

        # mark courier busy
        courier.is_available = False
        courier.status = CourierStatus.busy.value
        self.session.add(courier)

        await self.session.commit()
        await self.session.refresh(delivery)
        await self.session.refresh(courier)
        return courier


async def get_order_service(
    session: AsyncSession = Depends(get_db_session),
) -> OrderService:
    return OrderService(session)
