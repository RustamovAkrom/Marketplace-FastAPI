from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, validator

# * Product Images *


class ProductImageCreateScheme(BaseModel):
    url: str = Field(..., max_length=500)


class ProductImageOutScheme(BaseModel):
    id: int
    url: str = Field(..., max_length=500)
    is_main: bool

    model_config = ConfigDict(from_attributes=True)


class ProductVariantCreateScheme(BaseModel):
    sku: str = Field(..., max_length=100)
    attributes: Optional[str] = None
    price: float
    stock: int = 0
    is_active: Optional[bool] = True


class ProductVariantUpdateScheme(BaseModel):
    attributes: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None


class ProductVariantsOutScheme(BaseModel):
    id: int
    sku: str
    attributes: Optional[str]
    price: float
    stock: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class ProductCreateScheme(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    old_price: Optional[float] = Field(None, ge=0)
    is_stock: Optional[bool] = True
    is_active: Optional[bool] = True
    category_id: int
    brand_id: Optional[int] = None
    seller_id: Optional[int] = None
    images: Optional[List[ProductImageOutScheme]] = []
    variants: Optional[List[ProductVariantsOutScheme]] = []

    @validator("images", pre=True, always=True)
    def ensure_list_images(cls, v):
        raise v or []

    @validator("variants", pre=True, always=True)
    def ensure_list_variants(cls, v):
        return v or []


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


class ProductOutScheme(BaseModel):
    title: str
    slug: str
    description: Optional[str]
    price: float
    old_price: Optional[float]
    in_stock: bool
    is_active: bool
    category_id: int
    brand_id: Optional[int]
    seller_id: Optional[int]
    images: List[ProductImageOutScheme] = []
    variants: List[ProductVariantsOutScheme] = []
    model_config = ConfigDict(from_attributes=True)


__all__ = (
    "ProductImageCreateScheme",
    "ProductVariantCreateScheme",
    "ProductVariantsOutScheme",
    "ProductImageOutScheme",
    "ProductCreateScheme",
    "ProductUpdateScheme",
    "ProductOutScheme",
)
