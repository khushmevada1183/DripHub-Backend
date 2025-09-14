from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FeaturedProduct(BaseModel):
    id: int
    product_name: str
    category: Optional[str] = None
    rating: Optional[float] = None
    people_rated_count: Optional[int] = None
    description: Optional[str] = None
    img_url: Optional[str] = None
    real_price: Optional[float] = None
    current_price: Optional[float] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
