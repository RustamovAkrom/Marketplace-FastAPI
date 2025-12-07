from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import BaseModel


class Brand(BaseModel):
    __tablename__ = "brands"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    logo_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    website_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    parent_brand_id: Mapped[int | None] = mapped_column(
        ForeignKey("brands.id"), nullable=True
    )

    products: Mapped[list["Product"]] = relationship("Product", back_populates="brand")  # type: ignore # noqa: F821

    def __repr__(self):
        return f"<Brand(name={self.name}"


__all__ = ("Brand",)
