from typing import List

from pydantic import BaseModel, ConfigDict, Field


class CartItemBaseScheme(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=1)
    price: float = Field(..., ge=0)


class CartItemCreateScheme(CartItemBaseScheme):
    cart_id: int


class CartItemOutScheme(CartItemBaseScheme):
    id: int
    cart_id: int

    model_config = ConfigDict(from_attributes=True)


class CartBaseScheme(BaseModel):
    user_id: int


class CartCreateScheme(CartBaseScheme):
    pass


class CartOutScheme(CartBaseScheme):
    id: int
    items: List[CartItemOutScheme] = []

    model_config = ConfigDict(from_attributes=True)


__all__ = (
    "CartItemBaseScheme",
    "CartItemCreateScheme",
    "CartItemOutScheme",
    "CartBaseScheme",
    "CartCreateScheme",
    "CartOutScheme",
)
