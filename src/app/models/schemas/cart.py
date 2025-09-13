from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime
from app.models.schemas.product import ProductRead


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1
    metadata: Optional[Any] = None


class CartItemResponse(BaseModel):
    item_id: int
    product_id: int
    quantity: int
    price_at_add: float
    metadata: Optional[Any]
    product: Optional[ProductRead]


class Cart(BaseModel):
    cart_id: int
    owner_user_id: int
    items: List[CartItemResponse]
