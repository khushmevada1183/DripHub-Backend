from pydantic import BaseModel
from typing import List

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItem]

class OrderRead(BaseModel):
    id: int
    user_id: int
    total: float

    model_config = {"from_attributes": True}
