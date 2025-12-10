# src/services/cart_service.py
from __future__ import annotations

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.cart import CartCRUD
from db.crud.product import ProductCRUD  # ты будешь использовать свой
from db.dependencies.sessions import get_db_session
from db.models.carts import Cart, CartItem
from db.models.products import ProductVariant


class CartService:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session
        self.cart_crud = CartCRUD(session)
        self.product_crud = ProductCRUD(session)

    async def get_user_cart(self, user_id: int) -> Cart:
        cart = await self.cart_crud.get_cart_by_user(user_id)
        if not cart:
            cart = await self.cart_crud.create_cart_for_user(user_id)
        return cart

    async def add_to_cart(
        self, user_id: int, variant_id: int, quantity: int
    ) -> CartItem:
        cart = await self.get_user_cart(user_id)

        variant: ProductVariant | None = await self.product_crud.get_variant_by_id(
            variant_id
        )
        if not variant:
            raise HTTPException(status_code=404, detail="Variant not found")

        if variant.stock < quantity:
            raise HTTPException(status_code=400, detail="Not enough stock")

        existing_item = await self.cart_crud.get_item(cart.id, variant_id)

        if existing_item:
            new_qty = existing_item.quantity + quantity
            return await self.cart_crud.update_item_quantity(existing_item, new_qty)

        return await self.cart_crud.add_item(cart, variant, quantity)

    async def update_quantity(
        self, user_id: int, variant_id: int, quantity: int
    ) -> CartItem:
        cart = await self.get_user_cart(user_id)

        item = await self.cart_crud.get_item(cart.id, variant_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found in cart")

        if quantity <= 0:
            await self.cart_crud.remove_item(item)
            raise HTTPException(status_code=200, detail="Item removed")

        return await self.cart_crud.update_item_quantity(item, quantity)

    async def remove_from_cart(self, user_id: int, variant_id: int) -> None:
        cart = await self.get_user_cart(user_id)
        item = await self.cart_crud.get_item(cart.id, variant_id)

        if not item:
            raise HTTPException(status_code=404, detail="Item not in cart")

        await self.cart_crud.remove_item(item)

    async def clear_cart(self, user_id: int) -> None:
        cart = await self.get_user_cart(user_id)
        await self.cart_crud.clear_cart(cart.id)

    async def get_variant_by_id(self, variant_id: int) -> ProductVariant | None:
        return await self.session.get(ProductVariant, variant_id)
