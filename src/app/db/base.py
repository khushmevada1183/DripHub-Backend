from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

"""Base metadata registry.

We explicitly import model modules here so that any place importing just
`Base` (like the startup event calling `Base.metadata.create_all`) will
have all the model Table objects registered. Without these imports, a
fresh process that never directly imports the model modules would end up
with an empty metadata and no tables would be created.
"""

# Import models to register them with the metadata. Keep inside a try/except
# in case of circular import issues during certain tooling operations.
try:  # pragma: no cover - defensive import block
	from app.models.user import User  # noqa: F401
	from app.models.product import Product  # noqa: F401
	from app.models.order import Order  # noqa: F401
except Exception:
	# We silently ignore import errors here to avoid breaking ancillary
	# tooling (like Alembic autogenerate before dependencies are installed).
	pass

__all__ = ["Base"]
