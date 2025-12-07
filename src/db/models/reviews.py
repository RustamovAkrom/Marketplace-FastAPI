# src/db/models/review.py
from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import BaseModel


class Review(BaseModel):
    __tablename__ = "reviews"

    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)

    user: Mapped["User"] = relationship("User")  # type: ignore # noqa: F821
    product: Mapped["Product"] = relationship("Product")  # type: ignore # noqa: F821

    def __repr__(self):
        return f"<Review(id={self.id}, rating={self.rating}, user_id={self.user_id}, product_id={self.product_id})>"
