import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# allow imports from src/
ROOT = os.path.dirname(os.path.dirname(__file__))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# If DATABASE_URL is set in the environment, use it. Otherwise rely on ini.
database_url = os.getenv("DATABASE_URL")
if database_url:
    # configparser (used by alembic.Config) treats '%' as interpolation
    # markers which will raise ValueError for percent-encoded passwords
    # (for example 'pass%40word'). Escape percent signs by doubling
    # them so the URL can be safely stored in the config.
    safe_database_url = database_url.replace('%', '%%')
    config.set_main_option("sqlalchemy.url", safe_database_url)

# Import your models' MetaData object here for 'autogenerate' support
try:
    from app.db.base import Base
    target_metadata = Base.metadata
except Exception:  # pragma: no cover - safety in case imports fail
    target_metadata = None


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
