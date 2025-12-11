# src/schemas/cart.py
from pydantic import BaseModel, ConfigDict


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

    model_config = ConfigDict(from_attributes=True)


class CartResponse(BaseModel):
    id: int
    user_id: int
    items: list[CartItemScheme]

    model_config = ConfigDict(from_attributes=True)
