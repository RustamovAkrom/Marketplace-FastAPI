from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.delivery_address import DeliveryAddress
from schemas.delivery_address import (
    DeliveryAddressCreateScheme,
    DeliveryAddressUpdateScheme,
)
from utils.shortcuts import get_or_404


class DeliveryAddressCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self, user_id: int, data: DeliveryAddressCreateScheme
    ) -> DeliveryAddress:
        obj = DeliveryAddress(user_id=user_id, **data.dict())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_user_addresses(self, user_id: int) -> Sequence[DeliveryAddress]:
        result = await self.session.execute(
            select(DeliveryAddress).where(DeliveryAddress.user_id == user_id)
        )
        return result.scalars().all()

    async def get_by_id(self, address_id: int) -> DeliveryAddress:
        obj = await get_or_404(
            self.session.get(DeliveryAddress, address_id), "Address not found"
        )
        return obj

    async def update(
        self, address_id: int, data: DeliveryAddressUpdateScheme
    ) -> DeliveryAddress:
        obj = await self.get_by_id(address_id)
        for key, value in data.dict(exclude_unset=True).items():
            setattr(obj, key, value)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, address_id: int) -> bool:
        obj = await self.get_by_id(address_id)
        await self.session.delete(obj)
        await self.session.commit()
        return True
