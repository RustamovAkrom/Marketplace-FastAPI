from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SellerBaseScheme(BaseModel):
    user_id: int
    shop_name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = Field(None, max_length=500)


class SellerCreateScheme(SellerBaseScheme):
    pass


class SellerUpdateScheme(BaseModel):
    shop_name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = Field(None, max_length=500)


class SellerOutScheme(SellerBaseScheme):
    id: int

    model_config = ConfigDict(from_attributes=True)


__all__ = (
    "SellerBaseScheme",
    "SellerCreateScheme",
    "SellerUpdateScheme",
    "SellerOutScheme",
)
