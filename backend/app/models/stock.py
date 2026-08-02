from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func



class Stock(Base):
    __tablename__ = "add_stock"

    id = Column(Integer, primary_key=True, index=True)
    wh_id = Column(String(255), ForeignKey("users.email"), nullable=False)
    wh_logs = Column(Integer, ForeignKey("logs.id"), nullable=False)
    date = Column(DateTime, server_default=func.now())
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=0)


    # relationships
    warehouse = relationship("UserManager", foreign_keys=[wh_id], back_populates="add_stock")
    log_entry = relationship("Log", back_populates="stock")
    product = relationship("Product", back_populates="add_stock") 