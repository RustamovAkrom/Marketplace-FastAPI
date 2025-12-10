from __future__ import annotations

from typing import Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.courier import CourierCRUD
from db.dependencies.sessions import get_db_session
from db.models.couriers import Courier
from schemas.courier import CourierCreateScheme, CourierUpdateScheme
from utils.shortcuts import get_or_404


class CourierService:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session
        self.crud = CourierCRUD(session)

    async def get_by_id(self, courier_id: int) -> Courier:
        return await get_or_404(
            await self.crud.get_by_id(courier_id), "Courier not found"
        )

    async def create_courier(self, data: CourierCreateScheme) -> Courier:
        return await self.crud.create(data)

    async def update_courier(
        self, courier_id: int, data: CourierUpdateScheme
    ) -> Courier:
        return await self.crud.update(courier_id, data)

    async def all_available(self) -> Sequence[Courier]:
        return await self.crud.all_available()

    async def update_location(self, courier_id: int, lat: float, lon: float) -> Courier:
        courier = await self.get_by_id(courier_id)
        return await self.crud.update_location(courier, lat, lon)

    async def set_availability(self, courier_id: int, available: bool) -> Courier:
        courier = await self.get_by_id(courier_id)
        return await self.crud.set_availability(courier, available)
