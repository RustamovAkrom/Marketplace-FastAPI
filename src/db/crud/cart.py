# src/crud/cart_crud.py
from __future__ import annotations

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies.sessions import get_db_session
from db.models.carts import Cart, CartItem
from db.models.products import ProductVariant


class CartCRUD:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def get_cart_by_user(self, user_id: int) -> Cart | None:
        result = await self.session.execute(select(Cart).where(Cart.user_id == user_id))
        return result.scalars().first()

    async def create_cart_for_user(self, user_id: int) -> Cart:
        cart = Cart(user_id=user_id)
        self.session.add(cart)
        await self.session.commit()
        await self.session.refresh(cart)
        return cart

    async def get_item(self, cart_id: int, variant_id: int) -> CartItem | None:
        result = await self.session.execute(
            select(CartItem).where(
                CartItem.cart_id == cart_id, CartItem.variant_id == variant_id
            )
        )
        return result.scalars().first()

    async def add_item(
        self, cart: Cart, variant: ProductVariant, quantity: int
    ) -> CartItem:
        item = CartItem(
            cart_id=cart.id,
            variant_id=variant.id,
            quantity=quantity,
            price=variant.price,
        )
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def update_item_quantity(self, item: CartItem, quantity: int) -> CartItem:
        item.quantity = quantity
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def remove_item(self, item: CartItem) -> None:
        await self.session.delete(item)
        await self.session.commit()

    async def clear_cart(self, cart_id: int) -> None:
        await self.session.execute(delete(CartItem).where(CartItem.cart_id == cart_id))
        await self.session.commit()
