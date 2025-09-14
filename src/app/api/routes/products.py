from fastapi import APIRouter, Depends
from app.core.exceptions import HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.schemas.product import ProductCreate, ProductRead
from app.core.supabase_auth import get_current_user
from app.db.repositories.crud_product import create_product, list_products as repo_list_products

router = APIRouter()

@router.post("/", response_model=ProductRead)
def create(product_in: ProductCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return create_product(db, product_in)

@router.get("/", response_model=List[ProductRead])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return repo_list_products(db, skip=skip, limit=limit)
