from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

# * Product Images *


class ProductImageBaseScheme(BaseModel):
    url: str = Field(..., max_length=500)


class ProductImageCreateScheme(ProductImageBaseScheme):
    product_id: int


class ProductImageOutScheme(ProductImageBaseScheme):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ProductVariantCreateScheme(BaseModel):
    sku: str
    attributes: Optional[str] = None
    price: float
    stock: int


class ProductVariantsOutScheme(ProductVariantCreateScheme):
    id: int

    model_config = ConfigDict(from_attributes=True)


# * Product *
class ProductBaseScheme(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    slug: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None

    price: float = Field(..., ge=0)
    old_price: Optional[float] = Field(None, ge=0)

    is_stock: bool = True
    is_active: bool = True

    category_id: int
    brand_id: Optional[int] = None
    seller_id: Optional[int] = None

    images: Optional[List[ProductImageOutScheme]] = []
    variants: Optional[List[ProductVariantsOutScheme]] = []


class ProductCreateScheme(ProductBaseScheme):
    pass


class ProductUpdateScheme(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=255)
    slug: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    old_price: Optional[float] = Field(None, ge=0)
    in_stock: Optional[bool] = None
    is_active: Optional[bool] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    seller_id: Optional[int] = None


class ProductOutScheme(ProductBaseScheme):
    id: int
    images: List[ProductImageOutScheme] = []

    model_config = ConfigDict(from_attributes=True)


__all__ = (
    "ProductImageBaseScheme",
    "ProductImageCreateScheme",
    "ProductVariantCreateScheme",
    "ProductVariantsOutScheme",
    "ProductImageOutScheme",
    "ProductBaseScheme",
    "ProductCreateScheme",
    "ProductUpdateScheme",
    "ProductOutScheme",
)
