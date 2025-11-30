from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import BaseModel

from .product import Product
from .users import User


class Review(BaseModel):
    __tablename__ = "reviews"

    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    user: Mapped["User"] = relationship()
    product: Mapped["Product"] = relationship()

    def __repr__(self):
        return f"<Review(id={self.id}, rating={self.rating}, user_id={self.user_id}, product_id={self.product_id})>"


__all__ = ("Review",)
