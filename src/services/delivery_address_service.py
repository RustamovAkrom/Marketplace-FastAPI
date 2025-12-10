from __future__ import annotations

from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.delivery_address import DeliveryAddressCRUD
from db.dependencies.sessions import get_db_session
from db.models.delivery_address import DeliveryAddress
from schemas.delivery_address import (
    DeliveryAddressCreateScheme,
    DeliveryAddressUpdateScheme,
)
from utils.shortcuts import get_or_404


class DeliveryAddressService:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session
        self.crud = DeliveryAddressCRUD(session)

    async def list_user_addresses(self, user_id: int) -> List[DeliveryAddress]:
        return await self.crud.get_user_addresses(user_id)

    async def create_address(
        self, user_id: int, data: DeliveryAddressCreateScheme
    ) -> DeliveryAddress:
        return await self.crud.create(user_id, data)

    async def get_address(self, address_id: int) -> DeliveryAddress:
        return await get_or_404(
            await self.crud.get_by_id(address_id), "Address not found"
        )

    async def update_address(
        self, address_id: int, data: DeliveryAddressUpdateScheme
    ) -> DeliveryAddress:
        return await self.crud.update(address_id, data)

    async def delete_address(self, address_id: int) -> None:
        await self.crud.delete(address_id)
