# src/db/models/cart.py
from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import BaseModel


class Cart(BaseModel):
    __tablename__ = "carts"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), unique=True, index=True
    )
    items: Mapped[list["CartItem"]] = relationship(
        "CartItem", back_populates="cart", cascade="all, delete-orphan"
    )
    user: Mapped["User"] = relationship("User", back_populates="cart")  # type: ignore # noqa: F821


class CartItem(BaseModel):
    __tablename__ = "cart_items"

    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"), index=True)
    variant_id: Mapped[int] = mapped_column(
        ForeignKey("product_variants.id"), index=True
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    cart: Mapped["Cart"] = relationship("Cart", back_populates="items")
    variant: Mapped["ProductVariant"] = relationship("ProductVariant")  # type: ignore # noqa: F821
