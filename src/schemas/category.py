from pydantic import BaseModel


class CategoryBaseScheme(BaseModel):
    name: str
    slug: str
    description: str | None = None


class CategoryCreateScheme(CategoryBaseScheme):
    pass


class CategoryUpdateScheme(CategoryBaseScheme):
    pass


class CategoryOutScheme(CategoryBaseScheme):
    id: int

    class Config:
        from_attributes = True


__all__ = (
    "CategoryBaseScheme",
    "CategoryCreateScheme",
    "CategoryUpdateScheme",
    "CategoryOutScheme",
)
