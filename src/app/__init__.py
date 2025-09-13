"""
app package

Compatibility shim: re-export `schemas` from `app.models.schemas` so older
imports like `from app import schemas` continue to work while migration is
in progress.
"""
import warnings

warnings.warn("Importing 'schemas' via 'from app import schemas' is deprecated; use 'app.models.schemas'", DeprecationWarning)

from app.models import schemas as schemas

