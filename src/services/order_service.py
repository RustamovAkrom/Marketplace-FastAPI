# src/services/order_service.py
from datetime import datetime
from typing import Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.order import OrderCRUD
from db.models.carts import Cart
from db.models.orders import OrderStatus
from db.models.products import ProductVariant


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.crud = OrderCRUD(session)

    async def checkout(
        self,
        user_id: int,
        cart: Cart,
        promo_code: Optional[str] = None,
        shipping: Optional[Dict] = None,
    ):
        if not cart.items:
            raise ValueError("Cart is empty")

        total: float = 0.0
        variants_cache: dict[int, ProductVariant] = {}

        # 1. Validate stock and calculate total
        for item in cart.items:
            variant = await self.crud.get_variant(item.variant_id)
            if not variant:
                raise ValueError(f"Product variant {item.variant_id} not found")
            if variant.stock < item.quantity:
                raise ValueError(f"Not enough stock for {variant.sku}")
            total += float(variant.price) * item.quantity
            variants_cache[item.variant_id] = variant

        # 2. Apply promo code
        promo_discount: float = 0.0
        if promo_code:
            promo = await self.crud.get_promo(promo_code)
            if promo and (not promo.valid_to or promo.valid_to >= datetime.utcnow()):
                if promo.discount_percent is not None:
                    promo_discount = total * (promo.discount_percent / 100)
                else:
                    promo_discount = float(promo.discount_amount or 0)

        final_total: float = max(0.0, total - promo_discount)

        # 3. Create order
        order = await self.crud.create_order(user_id, final_total)

        # 4. Create order items
        for item in cart.items:
            variant = variants_cache[item.variant_id]
            await self.crud.create_order_item(
                order.id, variant.id, item.quantity, float(variant.price)
            )

        # 5. Commit
        await self.crud.commit()
        await self.crud.refresh(order)

        return order

    async def on_payment_success(self, order_id: int):
        order = await self.crud.get_order(order_id)
        if not order:
            raise ValueError("Order not found")

        # Decrease stock
        for item in order.items:
            variant = await self.crud.get_variant(item.variant_id)
            if not variant:
                raise ValueError(f"Product variant {item.variant_id} not found")
            if variant.stock < item.quantity:
                raise ValueError("Stock inconsistency")
            variant.stock -= item.quantity

        order.status = OrderStatus.PAID.value
        await self.crud.commit()
        await self.crud.refresh(order)

        return order
