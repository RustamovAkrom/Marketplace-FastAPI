from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ReviewBaseScheme(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    user_id: int
    product_id: int


class ReviewCreateScheme(ReviewBaseScheme):
    pass


class ReviewUpdateScheme(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None


class ReviewOutScheme(ReviewBaseScheme):
    id: int

    model_config = ConfigDict(from_attributes=True)


__all__ = (
    "ReviewBaseScheme",
    "ReviewCreateScheme",
    "ReviewUpdateScheme",
    "ReviewOutScheme",
)
