# src/db/models/products.py
from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import BaseModel


class Product(BaseModel):
    __tablename__ = "products"

    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    old_price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)

    in_stock: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False, index=True
    )
    brand_id: Mapped[int | None] = mapped_column(
        ForeignKey("brands.id"), nullable=True, index=True
    )
    seller_id: Mapped[int | None] = mapped_column(
        ForeignKey("sellers.id"), nullable=True, index=True
    )

    # relations
    images: Mapped[list["ProductImage"]] = relationship(
        "ProductImage", back_populates="product", cascade="all, delete-orphan"
    )
    variants: Mapped[list["ProductVariant"]] = relationship(
        "ProductVariant", back_populates="product", cascade="all, delete-orphan"
    )

    category: Mapped["Category"] = relationship("Category", back_populates="products")  # type: ignore # noqa: F821
    brand: Mapped["Brand"] = relationship("Brand", back_populates="products")  # type: ignore # noqa: F821
    seller: Mapped["Seller"] = relationship("Seller", back_populates="products")  # type: ignore # noqa: F821


class ProductImage(BaseModel):
    __tablename__ = "product_images"

    url: Mapped[str] = mapped_column(String(500), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    product: Mapped["Product"] = relationship("Product", back_populates="images")


class ProductVariant(BaseModel):
    __tablename__ = "product_variants"

    sku: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    attributes: Mapped[str | None] = mapped_column(
        String(500), nullable=True  # could be JSON string
    )  # e.g. JSON string: {"color":"red","size":"M"}
    price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    product: Mapped["Product"] = relationship("Product", back_populates="variants")
