from fastapi import APIRouter

from api.v1 import (
    admin,
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
    upload,
    users,
)
from api.v1.auth import authorizations, passwords, social, verifications
from api.v1.products import images, products, variants
from core.settings import settings

api_router = APIRouter(
    prefix=f"{settings.API_V1_PREFIX}",
)

# Upload image router
api_router.include_router(upload.router, prefix="/Upload", tags=["Upload"])
# Authorizations router
api_router.include_router(
    authorizations.router, prefix="/auth", tags=["Authorizations"]
)
# Passwords router
api_router.include_router(passwords.router, prefix="/passwords", tags=["Passwords"])
# Verifications router
api_router.include_router(
    verifications.router, prefix="/verifications", tags=["Verifications"]
)
# Social Auth for example (Google, GitHub, ...)
api_router.include_router(social.router, prefix="/social_auth", tags=["Social Auth"])
# User dashboard services (me, dashboard)
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
# User CRUD operations router
api_router.include_router(users.router, prefix="/users", tags=["Users"])
# Admin panel router
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
# Product categories CRUD operations router
api_router.include_router(category.router, prefix="/categories", tags=["Categories"])
# Product brands CRUD operations router
api_router.include_router(brand.router, prefix="/brands", tags=["Brands"])
# Carts services router
api_router.include_router(cart.router, prefix="/carts", tags=["Carts"])
# Product services router
api_router.include_router(products.router, prefix="/products", tags=["Products"])
# Product variant services router
api_router.include_router(variants.router, prefix="/products", tags=["Variants"])
# Product image services router
api_router.include_router(images.router, prefix="/products", tags=["Images"])
# Orders services router
api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])
# Payments services router by (Stripe, ....)
api_router.include_router(payments.router, prefix="/payments", tags=["Payments"])
# Promo codes to discount of products router
api_router.include_router(
    promo_codes.router, prefix="/promo_codes", tags=["Promo Codes"]
)
# Courier services router
api_router.include_router(couriers.router, prefix="/couriers", tags=["Couriers"])
# Delivery addresses services router
api_router.include_router(
    delivery_address.router, prefix="/delivery_addresses", tags=["Delivery Addresses"]
)
# Delivery services router
api_router.include_router(deliveries.router, prefix="/deliveries", tags=["Deliveries"])

__all__ = ("api_router",)
