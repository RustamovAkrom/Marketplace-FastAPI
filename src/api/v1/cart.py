# src/api/endpoints/cart.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies.auth import get_current_user  # твоя функция
from db.dependencies.sessions import get_db_session
from db.models.users import User
from schemas.cart import (
    AddToCartScheme,
    CartResponse,
    UpdateQuantityScheme,
)
from services.cart_service import CartService

router = APIRouter(prefix="/carts", tags=["Carts"])


def get_cart_service(session: AsyncSession = Depends(get_db_session)) -> CartService:
    return CartService(session)


@router.get("/", response_model=CartResponse)
async def get_cart(
    current_user: User = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service),
):
    cart = await cart_service.get_user_cart(current_user.id)
    return cart


@router.post("/add", response_model=CartResponse)
async def add_to_cart(
    data: AddToCartScheme,
    current_user: User = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service),
):
    await cart_service.add_to_cart(current_user.id, data.variant_id, data.quantity)
    return await cart_service.get_user_cart(current_user.id)


@router.post("/update", response_model=CartResponse)
async def update_quantity(
    data: UpdateQuantityScheme,
    current_user: User = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service),
):
    await cart_service.update_quantity(current_user.id, data.variant_id, data.quantity)
    return await cart_service.get_user_cart(current_user.id)


@router.delete("/{variant_id}")
async def remove_item(
    variant_id: int,
    current_user: User = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service),
):
    await cart_service.remove_from_cart(current_user.id, variant_id)
    return {"detail": "Item removed"}


@router.delete("/", status_code=200)
async def clear_cart(
    current_user: User = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service),
):
    await cart_service.clear_cart(current_user.id)
    return {"detail": "Cart cleared"}
