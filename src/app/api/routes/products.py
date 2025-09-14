from fastapi import APIRouter, Depends
from app.core.exceptions import HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.schemas.product import ProductCreate, ProductRead
from app.schemas.featured_product import FeaturedProduct
from app.core.supabase_auth import get_current_user
from app.db.repositories.crud_product import create_product, list_products as repo_list_products
from app.db.repositories.crud_product import list_featured_products

router = APIRouter()

@router.post("/", response_model=ProductRead)
def create(product_in: ProductCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return create_product(db, product_in)

@router.get("/", response_model=List[ProductRead])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return repo_list_products(db, skip=skip, limit=limit)


@router.get("/features", response_model=List[FeaturedProduct])
def list_featured(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    rows = list_featured_products(db, skip=skip, limit=limit)
    # rows are SQLAlchemy Row objects; convert to dict-like mappings that
    # Pydantic can parse via from_attributes=True
    results = []
    for r in rows:
        results.append({
            "id": r[0],
            "product_name": r[1],
            "category": r[2],
            "rating": float(r[3]) if r[3] is not None else None,
            "people_rated_count": int(r[4]) if r[4] is not None else None,
            "description": r[5],
            "img_url": r[6],
            "real_price": float(r[7]) if r[7] is not None else None,
            "current_price": float(r[8]) if r[8] is not None else None,
            "created_at": r[9],
        })
    return results
