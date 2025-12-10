from __future__ import annotations

from typing import List

from fastapi import Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.product import ProductCRUD, ProductImageCRUD, ProductVariantCRUD
from db.dependencies.sessions import get_db_session
from db.models.products import Product, ProductImage, ProductVariant
from schemas.product import (
    ProductCreateScheme,
    ProductUpdateScheme,
    ProductVariantCreateScheme,
    ProductVariantUpdateScheme,
)
from services.file_service import FileService
from utils.shortcuts import get_or_404


class ProductService:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session
        self.crud = ProductCRUD(session)

    # Products
    async def list_products(self, limit: int = 50, offset: int = 0) -> List[Product]:
        return await self.crud.get_all(limit=limit, offset=offset)

    async def get_product(self, product_id: int) -> Product:
        product = await get_or_404(
            await self.crud.get_by_id(product_id), "Product not found"
        )
        return product

    async def get_product_by_slug(self, slug: str) -> Product:
        product = await get_or_404(self.crud.get_by_slug(slug), "Product not found")
        return product

    async def create_product(self, data: ProductCreateScheme) -> Product:
        return await self.crud.create(data)

    async def update_product(
        self, product_id: int, data: ProductUpdateScheme
    ) -> Product:
        product = await self.get_product(product_id)
        return await self.crud.update(product, data)

    async def delete_product(self, product_id: int) -> None:
        product = await self.get_product(product_id)
        return await self.crud.delete(product)


class ProductVariantsService(ProductService):
    def __init__(self, session=Depends(get_db_session)):
        self.variant_crud = ProductVariantCRUD(session)
        super().__init__(session)

    # Product variants
    async def list_variants(self, product_id: int) -> List[ProductVariant]:
        product = await self.get_product(product_id)
        return product.variants

    async def create_variant(
        self, product_id: int, data: ProductVariantCreateScheme
    ) -> ProductVariant:
        # ensure product exists
        await self.get_product(product_id)
        return await self.variant_crud.create(product_id, data)

    async def update_variant(
        self, variant_id: int, data: ProductVariantUpdateScheme
    ) -> ProductVariant:
        variant = await get_or_404(
            await self.variant_crud.get_by_id(variant_id), "Product not found"
        )
        update_data = data.dict(exclude_unset=True)
        return await self.variant_crud.update(variant, update_data)

    async def delete_variant(self, variant_id: int) -> None:
        variant = await get_or_404(
            self.variant_crud.get_by_id(variant_id), "Variant not found"
        )
        return await self.variant_crud.delete(variant)


class ProductImageService(ProductService):
    def __init__(self, session=Depends(get_db_session)):
        self.image_crud = ProductImageCRUD(session)
        super().__init__(session)

    # Product Images
    async def add_image(self, product_id: int, file: UploadFile) -> ProductImage:
        # is product exist
        product = await self.get_product(product_id)

        # save file
        image_url = await FileService.save_image(file, "products")

        # save data in db
        return await self.image_crud.create(product.id, image_url)

    async def delete_image(self, image_id: int) -> None:
        image: ProductImage = await get_or_404(
            await self.image_crud.get_image(image_id), "Image not found"
        )
        await self.image_crud.delete(image.id)

    async def list_images(self, product_id: int):
        return await self.image_crud.get_images(product_id)
