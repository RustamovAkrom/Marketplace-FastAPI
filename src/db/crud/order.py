# src/db/crud/order.py
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.delivery import Delivery
from db.models.orders import Order, OrderItem, OrderStatus
from db.models.products import ProductVariant
from db.models.promo_codes import PromoCode


class OrderCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    # Create order
    async def create_order(
        self, user_id: int, total_amount: float, currency: str = "USD"
    ) -> Order:
        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            currency=currency,
            status=OrderStatus.PENDING_PAYMENT.value,
        )
        self.session.add(order)
        await self.session.flush()
        return order

    # Create order items
    async def create_order_item(
        self, order_id: int, variant_id: int, quantity: int, price: float
    ) -> OrderItem:
        item = OrderItem(
            order_id=order_id, variant_id=variant_id, quantity=quantity, price=price
        )
        self.session.add(item)
        return item

    # Commit and refresh
    async def commit(self):
        await self.session.commit()

    async def refresh(self, obj):
        await self.session.refresh(obj)

    # Get order by id
    async def get_order(self, order_id: int) -> Optional[Order]:
        return await self.session.get(Order, order_id)

    # Cart-related helpers (получение варианта товара)
    async def get_variant(self, variant_id: int) -> Optional[ProductVariant]:
        return await self.session.get(ProductVariant, variant_id)

    # promo helper
    async def get_promo_by_code(self, code: str) -> Optional[PromoCode]:
        res = await self.session.execute(
            select(PromoCode).where(PromoCode.code == code, PromoCode.is_active)
        )
        return res.scalars().first()

    # delivery creation
    async def create_delivery(
        self, order_id: int, courier_id: int | None, address_id: int
    ) -> Delivery:
        delivery = Delivery(
            order_id=order_id, courier_id=courier_id or None, address_id=address_id
        )
        self.session.add(delivery)
        await self.session.flush()
        return delivery

    # change order status
    async def set_order_status(self, order: Order, status: str) -> Order:
        order.status = status
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return order
