from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from datetime import datetime
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    # the actual database column is `name` in the existing DB; keep the
    # attribute called `title` for compatibility with existing code and
    # schemas by explicitly naming the column in the Column() call.
    title = Column('name', String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
