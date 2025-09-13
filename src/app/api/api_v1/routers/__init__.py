# Compatibility shims for old api_v1.routers imports
from app.api.routes import auth as auth
from app.api.routes import users as users
from app.api.routes import products as products
from app.api.routes import orders as orders
from app.api.routes import cart as cart
from app.api.routes import wishlist as wishlist

__all__ = ["auth", "users", "products", "orders", "cart", "wishlist"]
