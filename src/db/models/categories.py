from __future__ import annotations

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(
        String(150), unique=True, nullable=False, index=True
    )
    slug: Mapped[str] = mapped_column(
        String(200), unique=True, nullable=False, index=True
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")  # type: ignore # noqa: F821


__all__ = ("Category",)
