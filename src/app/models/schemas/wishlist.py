from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class WishlistItemCreate(BaseModel):
    product_id: int
    note: Optional[str] = None


class WishlistItemResponse(BaseModel):
    item_id: int
    product_id: int
    added_at: datetime
    note: Optional[str]
