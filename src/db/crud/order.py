# src/db/crud/order.py
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.orders import Order, OrderItem, OrderStatus
from db.models.products import ProductVariant
from db.models.promo_codes import PromoCode


class OrderCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    # Cart-related helpers (получение варианта товара)
    async def get_variant(self, variant_id: int) -> Optional[ProductVariant]:
        return await self.session.get(ProductVariant, variant_id)

    # Promo code
    async def get_promo(self, code: str) -> Optional[PromoCode]:
        stmt = select(PromoCode).where(PromoCode.code == code, PromoCode.is_active)
        res = await self.session.execute(stmt)
        return res.scalars().first()

    # Create order
    async def create_order(self, user_id: int, total_amount: float) -> Order:
        order = Order(
            user_id=user_id,
            total_amount=total_amount,
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
