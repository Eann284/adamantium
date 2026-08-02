from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import datetime


class Stock(Base):
    __tablename__ = "add_stock"

    id = Column(Integer, primary_key=True, index=True)
    wh_id = Column(String(50), ForeignKey("users.email"), nullable=False)
    wh_logs = Column(String(100), ForeignKey("logs.wh_id"), nullable=False)
    date = Column(DateTime, default=datetime.now())
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=0)


    # relationships
    warehouse = relationship("UserManager", foreign_keys=[wh_id], back_populates="add_stocks")
    wh_log = relationship("WHLogs", back_populates="add_stocks")
    product = relationship("Product", back_populates="add_stocks") 