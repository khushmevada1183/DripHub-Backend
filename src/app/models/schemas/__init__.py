"""app.models.schemas package

Expose submodules as attributes so code can use `app.models.schemas.user` etc.
"""
from . import user as user  # noqa: F401
from . import product as product  # noqa: F401
from . import order as order  # noqa: F401
from . import cart as cart  # noqa: F401
from . import wishlist as wishlist  # noqa: F401

__all__ = ["user", "product", "order", "cart", "wishlist"]
