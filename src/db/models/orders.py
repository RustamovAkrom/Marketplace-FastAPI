# src/db/models/orders.py
from __future__ import annotations

import enum

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import BaseModel


class OrderStatus(str, enum.Enum):
    CREATED = "created"
    PENDING_PAYMENT = "pending_payment"
    PAID = "paid"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class Order(BaseModel):
    __tablename__ = "orders"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    total_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    status: Mapped[OrderStatus] = mapped_column(
        String(50), nullable=False, default=OrderStatus.CREATED.value
    )

    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )
    user: Mapped["User"] = relationship("User", back_populates="orders")  # type: ignore # noqa: F821
    delivery: Mapped["Delivery"] = relationship(  # type: ignore # noqa: F821
        "Delivery", back_populates="order", uselist=False
    )


class OrderItem(BaseModel):
    __tablename__ = "order_items"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), index=True)
    variant_id: Mapped[int] = mapped_column(
        ForeignKey("product_variants.id"), index=True
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    variant: Mapped["ProductVariant"] = relationship("ProductVariant")  # type: ignore # noqa: F821
