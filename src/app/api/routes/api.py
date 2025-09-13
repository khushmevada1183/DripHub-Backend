from fastapi import APIRouter

# Import routers (moved from app.api.api_v1.routers)
from app.api.routes import auth, users, products, orders, cart, wishlist

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(cart.router, prefix="/cart", tags=["cart"])
api_router.include_router(wishlist.router, prefix="/wishlist", tags=["wishlist"])
