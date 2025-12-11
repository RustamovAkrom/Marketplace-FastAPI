from fastapi import APIRouter

from api.v1 import (
    admin,
    auth,
    brand,
    cart,
    category,
    couriers,
    dashboard,
    deliveries,
    delivery_address,
    orders,
    payments,
    promo_codes,
    social_auth,
    upload,
    users,
)
from api.v1.products import images, products, variants
from core.settings import settings

api_router = APIRouter(
    prefix=f"{settings.API_V1_PREFIX}",
)


api_router.include_router(upload.router, prefix="/Upload", tags=["Upload"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(
    social_auth.router, prefix="/social_auth", tags=["Social Auth"]
)
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(category.router, prefix="/categories", tags=["Categories"])
api_router.include_router(brand.router, prefix="/brands", tags=["Brands"])
api_router.include_router(cart.router, prefix="/carts", tags=["Carts"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(variants.router, prefix="/products", tags=["Variants"])
api_router.include_router(images.router, prefix="/products", tags=["Images"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])
api_router.include_router(payments.router, prefix="/payments", tags=["Payments"])
api_router.include_router(
    promo_codes.router, prefix="/promo_codes", tags=["Promo Codes"]
)
api_router.include_router(couriers.router, prefix="/couriers", tags=["Couriers"])
api_router.include_router(
    delivery_address.router, prefix="/delivery_addresses", tags=["Delivery Addresses"]
)
api_router.include_router(deliveries.router, prefix="/deliveries", tags=["Deliveries"])

__all__ = ("api_router",)
