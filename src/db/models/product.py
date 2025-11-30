from sqlalchemy import Boolean, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import BaseModel

from .seller import Seller


class Product(BaseModel):
    __tablename__ = "products"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    old_price: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)

    in_stock: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    brand_id: Mapped[int | None] = mapped_column(ForeignKey("brands.id"), nullable=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey("sellers.id"), nullable=True)

    images: Mapped[list["ProductImage"]] = relationship(back_populates="product")
    seller: Mapped["Seller"] = relationship(back_populates="products")

    def __repr__(self):
        return f"<Product(id={self.id}, title={self.title}, price={self.price})>"


class ProductImage(BaseModel):
    __tablename__ = "product_images"

    url: Mapped[str] = mapped_column(String(500), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    product: Mapped["Product"] = relationship(back_populates="images")

    def __repr__(self):
        return f"<ProductImage(id={self.id}, url={self.url})>"


__all__ = (
    "Product",
    "ProductImage",
)
