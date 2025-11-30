from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.dependencies import get_db_session
from src.db.models.category import Category
from src.schemas.category import CategoryCreateScheme, CategoryUpdateScheme


class CategoryCRUD:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def get_all(self) -> list[Category]:
        stmt = select(Category)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, category_id: int) -> Category | None:
        stmt = select(Category).where(Category.id == category_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_slug(self, slug: str) -> Category | None:
        stmt = select(Category).where(Category.slug == slug)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create(self, category_data: CategoryCreateScheme) -> Category:
        new_category = Category(**category_data.dict())
        self.session.add(new_category)
        await self.session.commit()
        await self.session.refresh(new_category)
        return new_category

    async def update(
        self, category: Category, category_data: CategoryUpdateScheme
    ) -> Category:
        for field, value in category_data.dict(exclude_unset=True).items():
            setattr(category, field, value)
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def delete(self, category: Category) -> None:
        await self.session.delete(category)
        await self.session.commit()
