from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from db.models.order import OrderStatus


class OrderItemBaseScheme(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=1)
    price: float = Field(..., ge=0)


class OrderItemCreateScheme(OrderItemBaseScheme):
    pass


class OrderItemOutScheme(OrderItemBaseScheme):
    id: int
    order_id: int

    model_config = ConfigDict(from_attributes=True)


class OrderBaseScheme(BaseModel):
    user_id: int
    total_amount: float = Field(..., ge=0)
    status: OrderStatus = OrderStatus.pending


class OrderCreateScheme(OrderBaseScheme):
    items: List[OrderItemCreateScheme]


class OrderUpdateScheme(BaseModel):
    status: Optional[OrderStatus] = None


class OrderOutScheme(OrderBaseScheme):
    id: int
    items: List[OrderItemOutScheme] = []

    model_config = ConfigDict(from_attributes=True)


__all__ = (
    "OrderItemBaseScheme",
    "OrderItemCreateScheme",
    "OrderItemOutScheme",
    "OrderBaseScheme",
    "OrderCreateScheme",
    "OrderUpdateScheme",
    "OrderOutScheme",
)
