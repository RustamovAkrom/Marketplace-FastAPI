from typing import List

from fastapi import APIRouter, Depends, status

from db.dependencies.auth import ADMIN_ROLE, require_roles
from schemas.promo_code import (
    PromoCodeCreateScheme,
    PromoCodeOutScheme,
    PromoCodeUpdateScheme,
)
from services.promo_service import PromoCodeService, get_promo_service

router = APIRouter(prefix="/promo-codes", tags=["Promo Codes"])


@router.get("/", response_model=List[PromoCodeOutScheme])
async def list_promos(service: PromoCodeService = Depends(get_promo_service)):
    return await service.crud.list_all()


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
