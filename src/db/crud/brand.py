from typing import Optional, Sequence

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies.sessions import get_db_session
from db.models.brands import Brand
from schemas.brand import BrandCreateScheme, BrandUpdateScheme


class BrandCRUD:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def get_all(self) -> Sequence[Brand]:
        result = await self.session.execute(select(Brand))
        return result.scalars().all()

    async def get_by_id(self, brand_id: int) -> Optional[Brand]:
        result = await self.session.execute(select(Brand).where(Brand.id == brand_id))
        return result.scalars().first()

    async def get_by_slug(self, brand_slug: int) -> Optional[Brand]:
        result = await self.session.execute(
            select(Brand).where(Brand.slug == brand_slug)
        )
        return result.scalars().first()

    async def create(self, data: BrandCreateScheme) -> Brand:
        new_brand = Brand(**data.dict())
        self.session.add(new_brand)
        try:
            await self.session.commit()
            await self.session.refresh(new_brand)
            return new_brand
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail="Brand already exists")

    async def update(self, brand: Brand, data: BrandUpdateScheme) -> Brand:
        for field, value in data.dict(exclude_unset=True).items():
            setattr(brand, field, value)

        try:
            self.session.add(brand)
            await self.session.commit()
            await self.session.refresh(brand)
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=400, detail="Update would violate constraints"
            )

    async def delete(self, brand: Brand) -> None:
        await self.session.delete(brand)
        await self.session.commit()
