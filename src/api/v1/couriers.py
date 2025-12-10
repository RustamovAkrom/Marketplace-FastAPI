from typing import List

from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies.auth import ADMIN_ROLE, require_roles
from db.dependencies.sessions import get_db_session
from schemas.courier import (
    CourierCreateScheme,
    CourierLocationUpdateScheme,
    CourierOutScheme,
    CourierUpdateScheme,
)
from services.courier_service import CourierService

router = APIRouter(prefix="/couriers", tags=["Couriers"])


async def get_courier_service(
    session: AsyncSession = Depends(get_db_session),
) -> CourierService:
    return CourierService(session)


@router.get(
    "/",
    response_model=List[CourierOutScheme],
    dependencies=[Depends(require_roles(ADMIN_ROLE))],
)
async def list_all_couriers(service: CourierService = Depends(get_courier_service)):
    # admin-only listing: CourierCRUD should expose list_all
    return (
        await service.crud.session.execute
    )  # <-- replace with service.crud.list_all() if implemented


@router.post("/", response_model=CourierOutScheme, status_code=status.HTTP_201_CREATED)
async def register_courier(
    data: CourierCreateScheme, service: CourierService = Depends(get_courier_service)
):
    return await service.create_courier(data)


@router.put(
    "/{courier_id}",
    response_model=CourierOutScheme,
    dependencies=[Depends(require_roles(ADMIN_ROLE))],
)
async def update_courier(
    courier_id: int,
    data: CourierUpdateScheme,
    service: CourierService = Depends(get_courier_service),
):
    return await service.update_courier(courier_id, data)


@router.post("/{courier_id}/location", response_model=CourierOutScheme)
async def update_location(
    courier_id: int,
    data: CourierLocationUpdateScheme,
    service: CourierService = Depends(get_courier_service),
):
    return await service.update_location(courier_id, data.lat, data.lon)


@router.post("/{courier_id}/availability", response_model=CourierOutScheme)
async def set_availability(
    courier_id: int,
    available: bool = Body(..., embed=True),
    service: CourierService = Depends(get_courier_service),
):
    return await service.set_availability(courier_id, available)


@router.get("/available", response_model=List[CourierOutScheme])
async def list_available(service: CourierService = Depends(get_courier_service)):
    return await service.all_available()
