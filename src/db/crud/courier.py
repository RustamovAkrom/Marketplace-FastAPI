from __future__ import annotations

from typing import Optional, Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.couriers import Courier
from schemas.courier import CourierCreateScheme, CourierUpdateScheme
from utils.shortcuts import get_or_404


class CourierCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_all(self) -> Sequence[Courier]:
        res = await self.session.execute(select(Courier))
        return res.scalars().all()

    async def get_by_id(self, courier_id: int) -> Optional[Courier]:
        obj = await get_or_404(
            self.session.get(Courier, courier_id), "Courier not found"
        )
        return obj

    async def create(self, data: CourierCreateScheme) -> Optional[Courier]:
        exists = await self.session.execute(
            select(Courier).where(Courier.user_id == data.user_id)
        )
        if exists.scalar_one_or_none():
            raise HTTPException(400, "Courier for this user already exists")

        courier = Courier(**data.dict())
        self.session.add(courier)
        await self.session.commit()
        await self.session.refresh(courier)
        return courier

    async def update(self, courier_id: int, data: CourierUpdateScheme) -> Courier:
        obj = await self.get_by_id(courier_id)

        payload = data.dict(exclude_unset=True)

        if "rating" in payload and payload["rating"]:
            if not (1 <= payload["rating"] <= 5):
                raise HTTPException(400, "Rating must be between 1 and 5")

        for k, v in payload.items():
            setattr(obj, k, v)

        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def all_available(self) -> Sequence[Courier]:
        res = await self.session.execute(
            select(Courier).where(
                Courier.is_available,
                Courier.is_verified,
            )
        )
        return res.scalars().all()

    async def update_location(
        self, courier: Courier, lat: float, lon: float
    ) -> Courier:
        courier.latitude = lat
        courier.longitude = lon
        await self.session.commit()
        return courier

    async def set_availability(self, courier: Courier, available: bool) -> Courier:
        courier.is_available = available
        await self.session.commit()
        return courier
