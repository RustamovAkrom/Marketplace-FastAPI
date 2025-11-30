from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import BaseModel


class Brand(BaseModel):
    __tablename__ = "brands"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    logo_url: Mapped[str] = mapped_column(String(255), nullable=True)
    website_url: Mapped[str] = mapped_column(String(255), nullable=True)
    parent_brand_id: Mapped[int | None] = mapped_column(
        ForeignKey("brands.id"), nullable=True
    )

    def __repr__(self):
        return f"<Brand(name={self.name}, description={self.description})>"


__all__ = ("Brand",)
