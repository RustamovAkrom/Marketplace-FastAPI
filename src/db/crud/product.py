# src/db/crud/product.py
from typing import Optional, Sequence

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies.sessions import get_db_session
from db.models.products import Product, ProductImage, ProductVariant
from schemas.product import (
    ProductCreateScheme,
    ProductUpdateScheme,
    ProductVariantCreateScheme,
)


class ProductCRUD:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def get_all(self, limit: int = 100, offset: int = 0) -> Sequence[Product]:
        result = await self.session.execute(select(Product).limit(limit).offset(offset))
        return result.scalars().all()

    async def get_by_id(self, product_id: int) -> Product:
        return await self.session.get(Product, product_id)

    async def get_by_slug(self, slug: str) -> Product:
        res = await self.session.execute(select(Product).where(Product.slug == slug))
        return res.scalars().first()

    async def create(self, data: ProductCreateScheme) -> Product:
        new_product = Product(**data.dict(exclude={"images", "variants"}))
        self.session.add(new_product)

        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(400, "Product already exists")

        await self.session.refresh(new_product)

        # images
        if data.images:
            for url in data.images:
                self.session.add(ProductImage(url=url, product_id=new_product.id))

        # variants
        if data.variants:
            for v in data.variants:
                self.session.add(
                    ProductVariant(
                        product_id=new_product.id,
                        sku=v.sku,
                        attributes=v.attributes,
                        price=v.price,
                        stock=v.stock,
                        is_active=v.is_active,
                    )
                )

        await self.session.commit()
        await self.session.refresh(new_product)
        return new_product

    async def update(self, product: Product, data: ProductUpdateScheme) -> Product:
        for field, value in data.dict(exclude_unset=True).items():
            setattr(product, field, value)

        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete(self, product: Product) -> None:
        await self.session.delete(product)
        await self.session.commit()


class ProductVariantCRUD:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def get_by_id(self, variant_id: int) -> Optional[ProductVariant]:
        return await self.session.get(ProductVariant, variant_id)

    async def create(
        self, product_id: int, data: ProductVariantCreateScheme
    ) -> ProductVariant:
        variant = ProductVariant(
            product_id=product_id,
            sku=data.sku,
            attributes=data.attributes,
            price=data.price,
            stock=data.stock,
            is_active=data.is_active,
        )
        self.session.add(variant)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=400, detail="Variant already exists or integrity error"
            )
        await self.session.refresh(variant)
        return variant

    async def update(self, variant: ProductVariant, data: dict) -> ProductVariant:
        for field, value in data.items():
            setattr(variant, field, value)
        self.session.add(variant)
        await self.session.commit()
        await self.session.refresh(variant)
        return variant

    async def delete(self, variant: ProductVariant) -> None:
        await self.session.delete(variant)
        await self.session.commit()


class ProductImageCRUD:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def get_image(self, image_id: int) -> ProductImage | None:
        return await self.session.get(ProductImage, image_id)

    async def create(self, product_id: int, url: str, is_main: bool) -> ProductImage:
        obj = ProductImage(product_id=product_id, url=url, is_main=is_main)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_images(self, product_id: int) -> Sequence[ProductImage]:
        q = select(ProductImage).where(ProductImage.product_id == product_id)
        result = await self.session.execute(q)
        return result.scalars().all()

    async def delete(self, image_id: int) -> bool:
        q = select(ProductImage).where(ProductImage.id == image_id)
        result = await self.session.execute(q)
        image = result.scalar_one_or_none()
        if not image:
            return False
        await self.session.delete(image)
        await self.session.commit()
        return True
