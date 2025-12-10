from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies.auth import get_current_user
from db.dependencies.sessions import get_db_session
from db.models.users import User
from schemas.delivery_address import (
    DeliveryAddressCreateScheme,
    DeliveryAddressOutScheme,
    DeliveryAddressUpdateScheme,
)
from services.delivery_address_service import DeliveryAddressService

router = APIRouter(prefix="/delivery-addresses", tags=["Delivery Addresses"])


async def get_delivery_address_service(
    session: AsyncSession = Depends(get_db_session),
) -> DeliveryAddressService:
    return DeliveryAddressService(session)


@router.get("/", response_model=List[DeliveryAddressOutScheme])
async def list_addresses(
    current_user: User = Depends(get_current_user),
    service: DeliveryAddressService = Depends(get_delivery_address_service),
):
    return await service.list_user_addresses(current_user.id)


@router.post(
    "/", response_model=DeliveryAddressOutScheme, status_code=status.HTTP_201_CREATED
)
async def create_address(
    data: DeliveryAddressCreateScheme,
    current_user: User = Depends(get_current_user),
    service: DeliveryAddressService = Depends(get_delivery_address_service),
):
    return await service.create_address(current_user.id, data)


@router.get("/{address_id}", response_model=DeliveryAddressOutScheme)
async def get_address(
    address_id: int,
    current_user: User = Depends(get_current_user),
    service: DeliveryAddressService = Depends(get_delivery_address_service),
):
    addr = await service.get_address(address_id)
    # ensure owner
    if addr.user_id != current_user.id:
        return {"detail": "Not found"}, 404
    return addr


@router.put("/{address_id}", response_model=DeliveryAddressOutScheme)
async def update_address(
    address_id: int,
    data: DeliveryAddressUpdateScheme,
    current_user: User = Depends(get_current_user),
    service: DeliveryAddressService = Depends(get_delivery_address_service),
):
    addr = await service.get_address(address_id)
    if addr.user_id != current_user.id:
        return {"detail": "Not found"}, 404
    return await service.update_address(address_id, data)


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(
    address_id: int,
    current_user: User = Depends(get_current_user),
    service: DeliveryAddressService = Depends(get_delivery_address_service),
):
    addr = await service.get_address(address_id)
    if addr.user_id != current_user.id:
        return {"detail": "Not found"}, 404
    await service.delete_address(address_id)
