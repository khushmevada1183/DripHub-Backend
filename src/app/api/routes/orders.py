from fastapi import APIRouter, Depends
from app.core.exceptions import HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.schemas.order import OrderCreate, OrderRead
from app.db.repositories.crud_order import create_order as crud_create_order, get_order as crud_get_order
from app.core.supabase_auth import get_current_user

router = APIRouter()

@router.post("/", response_model=OrderRead)
def create_order(order_in: OrderCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
	# naive total calculation for demo
	total = sum([1.0 * item.quantity for item in order_in.items])
	# use the authenticated local user's id
	user_id = current_user.id
	db_order = crud_create_order(db, user_id=user_id, total=total)
	return db_order

@router.get("/{order_id}", response_model=OrderRead)
def read_order(order_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
	db_order = crud_get_order(db, order_id)
	if not db_order:
		raise HTTPException(status_code=404, detail="Order not found")
	return db_order
