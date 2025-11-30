from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import BaseModel


class Seller(BaseModel):
    __tablename__ = "sellers"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    shop_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500))

    products: Mapped[list["Product"]] = relationship(back_populates="seller")  # type: ignore # noqa: F821

    def __repr__(self):
        return f"<Seller(id={self.id}, shop_name={self.shop_name}, user_id={self.user_id})>"


__all__ = ("Seller",)
