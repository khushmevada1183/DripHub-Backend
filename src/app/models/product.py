from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from datetime import datetime
from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True, nullable=False)
    category = Column(String, nullable=True)
    rating = Column(Float, nullable=True)
    people_rated_count = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    img_url = Column(Text, nullable=True)
    real_price = Column(Float, nullable=True)
    current_price = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # compatibility alias
    @property
    def title(self):
        return self.product_name

