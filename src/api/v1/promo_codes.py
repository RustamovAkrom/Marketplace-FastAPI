from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies.auth import ADMIN_ROLE, require_roles
from db.dependencies.sessions import get_db_session
from schemas.promo_code import (
    PromoCodeCreateScheme,
    PromoCodeOutScheme,
    PromoCodeUpdateScheme,
)
from services.promo_service import PromoCodeService

router = APIRouter(prefix="/promo-codes", tags=["Promo Codes"])


async def get_promo_service(
    session: AsyncSession = Depends(get_db_session),
) -> PromoCodeService:
    return PromoCodeService(session)


@router.get("/", response_model=List[PromoCodeOutScheme])
async def list_promos(service: PromoCodeService = Depends(get_promo_service)):
    # currently PromoCodeCRUD has no list method — if needed add it.
    return (
        await service.crud.session.execute
    )  # replace with service.crud.list_all() if added


@router.post(
    "/",
    response_model=PromoCodeOutScheme,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(ADMIN_ROLE))],
)
async def create_promo(
    data: PromoCodeCreateScheme, service: PromoCodeService = Depends(get_promo_service)
):
    return await service.create(data)


@router.get("/validate/{code}", response_model=PromoCodeOutScheme)
async def validate_code(
    code: str, service: PromoCodeService = Depends(get_promo_service)
):
    return await service.validate_code(code)


@router.put(
    "/{promo_id}",
    response_model=PromoCodeOutScheme,
    dependencies=[Depends(require_roles(ADMIN_ROLE))],
)
async def update_promo(
    promo_id: int,
    data: PromoCodeUpdateScheme,
    service: PromoCodeService = Depends(get_promo_service),
):
    return await service.update(promo_id, data)


@router.delete(
    "/{promo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles(ADMIN_ROLE))],
)
async def delete_promo(
    promo_id: int, service: PromoCodeService = Depends(get_promo_service)
):
    await service.crud.get_by_id(promo_id)  # will raise if not found
    # you might want to implement delete in CRUD; for now just deactivate
    await service.update(promo_id, PromoCodeUpdateScheme(is_active=False))
