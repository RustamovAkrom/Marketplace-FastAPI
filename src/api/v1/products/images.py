from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, UploadFile, status

from db.dependencies.auth import ADMIN_ROLE, SELLER_ROLE, require_roles
from schemas.product import (
    ProductImageOutScheme,
)
from services.product_service import ProductImageService, get_product_images_service

router = APIRouter(prefix="/products", tags=["Product Images"])


# Product Image endpoints
@router.get("/{product_id}/images", response_model=List[ProductImageOutScheme])
async def list_images(
    product_id: int,
    product_service: ProductImageService = Depends(get_product_images_service),
):
    return await product_service.list_images(product_id)


@router.post(
    "/{product_id}/images",
    response_model=ProductImageOutScheme,
    dependencies=[Depends(require_roles(ADMIN_ROLE, SELLER_ROLE))],
)
async def upload_image(
    product_id: int,
    file: UploadFile,
    product_service: ProductImageService = Depends(get_product_images_service),
):
    return await product_service.add_image(product_id, file)


@router.delete(
    "/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles(ADMIN_ROLE, SELLER_ROLE))],
)
async def delete_image(
    image_id: int,
    product_service: ProductImageService = Depends(get_product_images_service),
):
    await product_service.delete_image(image_id)
