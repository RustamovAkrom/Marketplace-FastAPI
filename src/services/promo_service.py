from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.promo_codes import PromoCodeCRUD
from db.dependencies.sessions import get_db_session
from db.models.promo_codes import PromoCode
from schemas.promo_code import PromoCodeCreateScheme, PromoCodeUpdateScheme
from utils.shortcuts import get_or_404


class PromoCodeService:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session
        self.crud = PromoCodeCRUD(session)

    async def create(self, data: PromoCodeCreateScheme) -> PromoCode:
        return await self.crud.create(data)

    async def get(self, promo_id: int) -> PromoCode:
        return await get_or_404(
            await self.crud.get_by_id(promo_id), "Promo code not found"
        )

    async def update(self, promo_id: int, data: PromoCodeUpdateScheme) -> PromoCode:
        return await self.crud.update(promo_id, data)

    async def validate_code(self, code: str) -> PromoCode:
        return await self.crud.get_by_code(code)
