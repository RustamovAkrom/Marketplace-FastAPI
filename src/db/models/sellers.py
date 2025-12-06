from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import BaseModel


class Seller(BaseModel):
    __tablename__ = "sellers"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), unique=True, index=True
    )
    shop_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="seller")  # type: ignore # noqa: F821
    products: Mapped[list["Product"]] = relationship("Product", back_populates="seller", cascade="all, delete-orphan")  # type: ignore # noqa: F821

    def __repr__(self):
        return f"<Seller(id={self.id}, shop_name={self.shop_name}, user_id={self.user_id})>"


__all__ = ("Seller",)
