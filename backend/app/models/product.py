from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(100), nullable=False)
    product_image = Column(String(255), nullable=False)
    stock = Column(Integer, default=0)


    # relationships

    releases = relationship("Release", back_populates="product")
    add_stock = relationship("Stock", back_populates="product")