from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.promo_codes import PromoCode
from schemas.promo_code import PromoCodeCreateScheme, PromoCodeUpdateScheme
from utils.shortcuts import get_or_404


class PromoCodeCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: PromoCodeCreateScheme) -> PromoCode:
        exists = await self.session.execute(
            select(PromoCode).where(PromoCode.code == data.code)
        )
        if exists.scalar_one_or_none():
            raise HTTPException(400, "Promo code already exists")

        promo = PromoCode(**data.dict())
        self.session.add(promo)
        await self.session.commit()
        await self.session.refresh(promo)
        return promo

    async def get_by_id(self, promo_id: int) -> Optional[PromoCode]:
        obj = await get_or_404(
            self.session.get(PromoCode, promo_id), "Promo code not found"
        )
        return obj

    async def validate(self, promo: PromoCode) -> Optional[bool]:
        if not promo.is_active:
            raise HTTPException(400, "Promo code is inactive")

        now = datetime.utcnow()

        if promo.valid_from and now < promo.valid_from:
            raise HTTPException(400, "Promo code not valid yet")

        if promo.valid_to and now > promo.valid_to:
            raise HTTPException(400, "Promo code expired")

        return True

    async def get_by_code(self, code: str) -> Optional[PromoCode]:
        res = await self.session.execute(
            select(PromoCode).where(PromoCode.code == code)
        )
        promo = await get_or_404(res.scalar_one_or_none(), "Promo code not found")
        await self.validate(promo)
        return promo

    async def update(
        self, promo_id: int, data: PromoCodeUpdateScheme
    ) -> Optional[PromoCode]:
        obj = await self.get_by_id(promo_id)
        for k, v in data.dict(exclude_unset=True).items():
            setattr(obj, k, v)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
