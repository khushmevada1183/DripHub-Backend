"""Utility script to drop and recreate all database tables for a clean local dev database.

USAGE (from project root):
    python -m scripts.reset_db  # DANGEROUS: destroys all data!

You can optionally provide --with-seed to insert a sample user & product.
"""
from argparse import ArgumentParser
from sqlalchemy import text
from app.db.session import engine
from app.db.base import Base  # imports models for registration
from app.core.security import get_password_hash
from sqlalchemy.orm import Session


def reset_database(with_seed: bool = False):
    # Drop all tables (respecting FK constraints order via metadata)
    Base.metadata.drop_all(bind=engine)
    # Recreate all tables
    Base.metadata.create_all(bind=engine)

    if with_seed:
        from app.models.user import User
        from app.models.product import Product
        session = Session(bind=engine)
        try:
            demo_user = User(email="demo@example.com", hashed_password=get_password_hash("demo123"), is_superuser=True)
            session.add(demo_user)
            session.flush()  # assign id
            demo_product = Product(title="Sample Product", description="Seed data product", price=9.99)
            session.add(demo_product)
            session.commit()
            print("Inserted seed user & product.")
        finally:
            session.close()

    print("Database reset complete.")


def main():
    parser = ArgumentParser()
    parser.add_argument("--with-seed", action="store_true", help="Insert seed rows after reset")
    args = parser.parse_args()
    reset_database(with_seed=args.with_seed)

if __name__ == "__main__":
    main()
