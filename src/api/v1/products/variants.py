from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies.auth import ADMIN_ROLE, SELLER_ROLE, require_roles
from db.dependencies.sessions import get_db_session
from schemas.product import (
    ProductVariantCreateScheme,
    ProductVariantsOutScheme,
    ProductVariantUpdateScheme,
)
from services.product_service import ProductVariantsService

router = APIRouter(prefix="/products", tags=["Product Variants"])


async def get_product_variants_service(
    session: AsyncSession = Depends(get_db_session),
) -> ProductVariantsService:
    return ProductVariantsService(session)


# Product Variants endpoints
@router.get("/{product_id}/variants", response_model=List[ProductVariantsOutScheme])
async def list_variants(
    product_id: int,
    service: ProductVariantsService = Depends(get_product_variants_service),
):
    return await service.list_variants(product_id)


@router.post(
    "/{product_id}/variants",
    response_model=ProductVariantsOutScheme,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(ADMIN_ROLE, SELLER_ROLE))],
)
async def create_variant(
    product_id: int,
    data: ProductVariantCreateScheme,
    service: ProductVariantsService = Depends(get_product_variants_service),
):
    return await service.create_variant(product_id, data)


@router.put(
    "/variants/{variant_id}",
    response_model=ProductVariantsOutScheme,
    dependencies=[Depends(require_roles(ADMIN_ROLE, SELLER_ROLE))],
)
async def update_variant(
    variant_id: int,
    data: ProductVariantUpdateScheme,
    service: ProductVariantsService = Depends(get_product_variants_service),
):
    return await service.update_variant(variant_id, data)


@router.delete(
    "/variants/{variant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles(ADMIN_ROLE, SELLER_ROLE))],
)
async def delete_variant(
    variant_id: int,
    service: ProductVariantsService = Depends(get_product_variants_service),
):
    await service.delete_variant(variant_id)
