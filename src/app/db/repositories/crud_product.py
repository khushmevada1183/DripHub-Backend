from sqlalchemy.orm import Session
from app import models, schemas

def create_product(db: Session, product_in: schemas.product.ProductCreate):
    db_obj = models.product.Product(title=product_in.title, description=product_in.description, price=product_in.price)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_product(db: Session, product_id: int):
    return db.query(models.product.Product).filter(models.product.Product.id == product_id).first()

def list_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.product.Product).offset(skip).limit(limit).all()
