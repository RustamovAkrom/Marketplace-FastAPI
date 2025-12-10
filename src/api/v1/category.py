from fastapi import APIRouter, Depends, status

from db.crud.category import CategoryCRUD
from db.dependencies.auth import ADMIN_ROLE, SELLER_ROLE, require_roles
from schemas.category import (
    CategoryCreateScheme,
    CategoryOutScheme,
    CategoryUpdateScheme,
)
from utils.shortcuts import get_or_404

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[CategoryOutScheme])
async def get_categories(categoryies_crud: CategoryCRUD = Depends(CategoryCRUD)):
    return await categoryies_crud.get_all()


@router.get("/{slug}", response_model=CategoryOutScheme)
async def get_category(
    slug: str, categoryies_crud: CategoryCRUD = Depends(CategoryCRUD)
):
    category = await get_or_404(
        categoryies_crud.get_by_slug(slug), "Category not found"
    )
    return category


@router.post(
    "/",
    response_model=CategoryOutScheme,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(ADMIN_ROLE, SELLER_ROLE))],
)
async def create_category(
    data: CategoryCreateScheme, categoryies_crud: CategoryCRUD = Depends(CategoryCRUD)
):
    return await categoryies_crud.create(data)


@router.put(
    "/{slug}",
    response_model=CategoryOutScheme,
    dependencies=[Depends(require_roles(ADMIN_ROLE, SELLER_ROLE))],
)
async def update_category(
    slug: str,
    data: CategoryUpdateScheme,
    categoryies_crud: CategoryCRUD = Depends(CategoryCRUD),
):
    category = await get_or_404(
        categoryies_crud.get_by_slug(slug), "Category not found"
    )
    return await categoryies_crud.update(category, data)


@router.delete(
    "/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles(ADMIN_ROLE, SELLER_ROLE))],
)
async def delete_category(
    slug: str, categoryies_crud: CategoryCRUD = Depends(CategoryCRUD)
):
    category = await get_or_404(
        categoryies_crud.get_by_slug(slug), "Category not found"
    )
    await categoryies_crud.delete(category)
