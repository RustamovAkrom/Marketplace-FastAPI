from fastapi import APIRouter, Depends, status

from db.crud.brand import BrandCRUD
from db.dependencies.auth import ADMIN_ROLE, SELLER_ROLE, require_roles
from schemas.brand import (
    BrandCreateScheme,
    BrandOutScheme,
    BrandUpdateScheme,
)
from utils.shortcuts import get_or_404

router = APIRouter(prefix="/brands", tags=["Brands"])


@router.get("/", response_model=list[BrandOutScheme])
async def get_brands(brands_crud: BrandCRUD = Depends(BrandCRUD)):
    return await brands_crud.get_all()


@router.get("/{slug}", response_model=BrandOutScheme)
async def get_brand(slug: str, brands_crud: BrandCRUD = Depends(BrandCRUD)):
    brand = await get_or_404(brands_crud.get_by_slug(slug), "Brand not found")
    return brand


@router.post(
    "/",
    response_model=BrandOutScheme,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(ADMIN_ROLE, SELLER_ROLE))],
)
async def create_brand(
    data: BrandCreateScheme, brands_crud: BrandCRUD = Depends(BrandCRUD)
):
    return await brands_crud.create(data)


@router.put(
    "/{slug}",
    response_model=BrandOutScheme,
    dependencies=[Depends(require_roles(ADMIN_ROLE, SELLER_ROLE))],
)
async def update_brand(
    slug: str, data: BrandUpdateScheme, brands_crud: BrandCRUD = Depends(BrandCRUD)
):
    brand = await get_or_404(brands_crud.get_by_slug(slug), "Brand not found")
    return await brands_crud.update(brand, data)


@router.delete(
    "/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles(ADMIN_ROLE, SELLER_ROLE))],
)
async def delete_brand(slug: str, brands_crud: BrandCRUD = Depends(BrandCRUD)):
    brand = await get_or_404(brands_crud.get_by_slug(slug), "Brand not found")
    await brands_crud.delete(brand)
