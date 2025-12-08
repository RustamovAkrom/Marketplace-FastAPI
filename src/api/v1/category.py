from fastapi import APIRouter, Depends, HTTPException, status

from db.crud.category import CategoryCRUD
from db.dependencies.auth import ADMIN_ROLE, SELLER_ROLE, require_roles
from schemas.category import (
    CategoryCreateScheme,
    CategoryOutScheme,
    CategoryUpdateScheme,
)

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[CategoryOutScheme])
async def get_categories(categoryies_crud: CategoryCRUD = Depends(CategoryCRUD)):
    return await categoryies_crud.get_all()


@router.get("/{slug}", response_model=CategoryOutScheme)
async def get_category(
    slug: str, categoryies_crud: CategoryCRUD = Depends(CategoryCRUD)
):
    category = await categoryies_crud.get_by_slug(slug)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
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
    category = await categoryies_crud.get_by_slug(slug)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return await categoryies_crud.update(category, data)


@router.delete(
    "/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles(ADMIN_ROLE, SELLER_ROLE))],
)
async def delete_category(
    slug: str, categoryies_crud: CategoryCRUD = Depends(CategoryCRUD)
):
    category = await categoryies_crud.get_by_slug(slug)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    await categoryies_crud.delete(category)
