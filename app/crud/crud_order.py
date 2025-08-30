from sqlalchemy.orm import Session
from app import models, schemas

def create_order(db: Session, user_id: int, total: float):
    db_obj = models.order.Order(user_id=user_id, total=total)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_order(db: Session, order_id: int):
    return db.query(models.order.Order).filter(models.order.Order.id == order_id).first()
