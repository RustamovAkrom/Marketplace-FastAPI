from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, status

from db.dependencies.auth import ADMIN_ROLE, SELLER_ROLE, require_roles
from schemas.product import (
    ProductCreateScheme,
    ProductOutScheme,
    ProductUpdateScheme,
)
from services.product_service import ProductService, get_product_service

router = APIRouter(prefix="/products", tags=['Products'])


@router.get("/", response_model=List[ProductOutScheme])
async def list_products(
    limit: int = 50,
    offset: int = 0,
    product_service: ProductService = Depends(get_product_service),
):
    return await product_service.list_products(limit=limit, offset=offset)


@router.post(
    "/",
    response_model=ProductOutScheme,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(ADMIN_ROLE, SELLER_ROLE))],
)
async def create_product(
    data: ProductCreateScheme,
    product_service: ProductService = Depends(get_product_service),
):
    return await product_service.create_product(data)


@router.get("/{product_id}", response_model=ProductOutScheme)
async def retrieve_product(
    product_id: int, service: ProductService = Depends(get_product_service)
):
    return await service.get_product(product_id)


@router.get("/slug/{slug}", response_model=ProductOutScheme)
async def retrieve_product_by_slug(
    slug: str, service: ProductService = Depends(get_product_service)
):
    return await service.get_product_by_slug(slug)


@router.put(
    "/{product_id}",
    response_model=ProductOutScheme,
    dependencies=[Depends(require_roles(ADMIN_ROLE, SELLER_ROLE))],
)
async def update_product(
    product_id: int,
    data: ProductUpdateScheme,
    service: ProductService = Depends(get_product_service),
):
    return await service.update_product(product_id, data)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles(ADMIN_ROLE, SELLER_ROLE))],
)
async def delete_product(
    product_id: int, service: ProductService = Depends(get_product_service)
):
    await service.delete_product(product_id)
