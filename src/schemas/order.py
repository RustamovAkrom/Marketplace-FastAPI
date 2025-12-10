from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class CheckoutItemScheme(BaseModel):
    variant_id: int
    quantity: int = Field(..., gt=0)


class CheckoutRequestScheme(BaseModel):
    user_id: int
    address_id: int
    delivery_id: int
    items: List[CheckoutItemScheme]
    promo_code: Optional[str] = None
    currency: Optional[str] = "USD"


class OrderItemOutScheme(BaseModel):
    id: int
    variant_id: int
    quantity: int
    price: float

    model_config = ConfigDict(from_attributes=True)


class DeliveryOutScheme(BaseModel):
    id: int
    courier_id: Optional[int]
    status: str
    assigned_at: Optional[datetime]
    delivered_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class OrderOutScheme(BaseModel):
    id: int
    user_id: int
    total_amount: float
    currency: str
    status: str
    items: List[OrderItemOutScheme]
    delivery: Optional[DeliveryOutScheme]

    model_config = ConfigDict(from_attributes=True)
