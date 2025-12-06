from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CategoryBaseScheme(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    slug: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = None


class CategoryCreateScheme(CategoryBaseScheme):
    pass


class CategoryUpdateScheme(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None


class CategoryOutScheme(CategoryBaseScheme):
    id: int

    model_config = ConfigDict(from_attributes=True)


__all__ = (
    "CategoryBaseScheme",
    "CategoryCreateScheme",
    "CategoryUpdateScheme",
    "CategoryOutScheme",
)
