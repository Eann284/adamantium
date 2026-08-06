from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class AreaEnum(str, enum.Enum):
    CAVITE = "Cavite"
    LAGUNA = "Laguna"
    QUEZON = "Quezon"
    RIZAL = "Rizal"

class ProductsInventory(Base):

    __tablename__ = "products_inventory"

    id = Column(Integer, primary_key=True, index= True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    area = Column(Enum(AreaEnum), default=AreaEnum.CAVITE)
    stock = Column(Integer, default=0)


    # relationship
    product = relationship("Product", back_populates="inventory")
    add_stocks = relationship("Stock", back_populates="inventory", cascade="all, delete-orphan")