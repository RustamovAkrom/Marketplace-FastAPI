from typing import Optional, Sequence

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies.sessions import get_db_session
from db.models.categories import Category
from schemas.category import CategoryCreateScheme, CategoryUpdateScheme


class CategoryCRUD:
    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def get_all(self) -> Sequence[Category]:
        result = await self.session.execute(select(Category))
        return result.scalars().all()

    async def get_by_id(self, category_id: int) -> Optional[Category]:
        result = await self.session.execute(
            select(Category).where(Category.id == category_id)
        )
        return result.scalars().first()

    async def get_by_slug(self, slug: str) -> Optional[Category]:
        result = await self.session.execute(
            select(Category).where(Category.slug == slug)
        )
        return result.scalars().first()

    async def create(self, data: CategoryCreateScheme) -> Category:
        new_category = Category(**data.dict())
        self.session.add(new_category)
        try:
            await self.session.commit()
            await self.session.refresh(new_category)
            return new_category
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail="Category already exists")

    async def update(self, category: Category, data: CategoryUpdateScheme) -> Category:
        for field, value in data.dict(exclude_unset=True).items():
            setattr(category, field, value)
        try:
            self.session.add(category)
            await self.session.commit()
            await self.session.refresh(category)
            return category
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=400, detail="Update would violate constraints"
            )

    async def delete(self, category: Category) -> None:
        await self.session.delete(category)
        await self.session.commit()
