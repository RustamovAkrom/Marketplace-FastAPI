from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PromoCodeBaseScheme(BaseModel):
    code: str = Field(..., min_length=3, max_length=50)
    discount_percent: int = Field(..., ge=0, le=100)
    discount_amount: Optional[float] = Field(None, ge=0)
    is_active: bool = True


class PromoCodeCreateScheme(PromoCodeBaseScheme):
    pass


class PromoCodeUpdateScheme(BaseModel):
    code: Optional[str] = Field(None, min_length=3, max_length=50)
    discount_percent: Optional[int] = Field(None, ge=0, le=100)
    discount_amount: Optional[float] = Field(None, ge=0)
    is_active: Optional[bool] = None


class PromoCodeOutScheme(PromoCodeBaseScheme):
    id: int

    model_config = ConfigDict(from_attributes=True)


__all__ = (
    "PromoCodeBaseScheme",
    "PromoCodeCreateScheme",
    "PromoCodeUpdateScheme",
    "PromoCodeOutScheme",
)
