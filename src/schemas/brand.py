from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BrandBaseScheme(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    logo_url: Optional[str] = Field(None, max_length=255)
    website_url: Optional[str] = Field(None, max_length=255)
    parent_brand_id: Optional[int] = None


class BrandCreateScheme(BrandBaseScheme):
    pass


class BrandUpdateScheme(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    logo_url: Optional[str] = Field(None, max_length=255)
    website_url: Optional[str] = Field(None, max_length=255)
    parent_brand_id: Optional[int] = None


class BrandOutScheme(BrandBaseScheme):
    id: int

    model_config = ConfigDict(from_attributes=True)


__all__ = (
    "BrandBaseScheme",
    "BrandCreateScheme",
    "BrandUpdateScheme",
    "BrandOutScheme",
)
