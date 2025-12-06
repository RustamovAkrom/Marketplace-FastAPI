# src/services/cart_service.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.carts import Cart, CartItem
from db.models.products import ProductVariant


class CartService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_cart(self, user_id: int) -> Cart:
        stmt = select(Cart).where(Cart.user_id == user_id)
        res = await self.session.execute(stmt)
        cart = res.scalars().first()
        if cart:
            return cart
        cart = Cart(user_id=user_id)
        self.session.add(cart)
        await self.session.commit()
        await self.session.refresh(cart)
        return cart

    async def add_item(self, user_id: int, variant_id: int, qty: int = 1) -> CartItem:
        cart = await self.get_or_create_cart(user_id)
        # check stock
        stmt = select(ProductVariant).where(ProductVariant.id == variant_id)
        res = await self.session.execute(stmt)
        variant = res.scalars().first()
        if not variant or not variant.is_active or variant.stock < qty:
            raise ValueError("Variant not available")

        # check existing item
        for it in cart.items:
            if it.variant_id == variant_id:
                it.quantity += qty
                it.price = float(variant.price)
                self.session.add(it)
                await self.session.commit()
                await self.session.refresh(it)
                return it

        item = CartItem(
            cart_id=cart.id,
            variant_id=variant_id,
            quantity=qty,
            price=float(variant.price),
        )
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def remove_item(self, user_id: int, item_id: int) -> None:
        stmt = select(CartItem).where(CartItem.id == item_id)
        res = await self.session.execute(stmt)
        item = res.scalars().first()
        if item:
            await self.session.delete(item)
            await self.session.commit()
