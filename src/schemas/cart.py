# src/schemas/cart.py
from pydantic import BaseModel


class AddToCartScheme(BaseModel):
    variant_id: int
    quantity: int = 1


class UpdateQuantityScheme(BaseModel):
    variant_id: int
    quantity: int


class CartItemScheme(BaseModel):
    id: int
    variant_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    id: int
    user_id: int
    items: list[CartItemScheme]

    class Config:
        from_attributes = True
