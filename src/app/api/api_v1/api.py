from fastapi import APIRouter
from app.api.api_v1.routers import auth, users, products
from app.api.api_v1.routers import orders
from .routers import cart as cart_router
from .routers import wishlist as wishlist_router

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(cart_router.router, prefix="/cart", tags=["cart"])
api_router.include_router(wishlist_router.router, prefix="/wishlist", tags=["wishlist"])
"""Compatibility shim: old `app.api.api_v1.api` now re-exports the new
router aggregator in `app.api.routes.api`.
"""

from app.api.routes.api import api_router

# Expose `api_router` so existing imports continue to work
__all__ = ["api_router"]
