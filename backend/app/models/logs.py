from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base
import datetime


class Log(Base):

    __tablename__ = "logs"

    wh_logs = Column(Integer, primary_key=True, index=True)
    wh_email = Column(String(50), ForeignKey("users.email"))
    date = DateTime(default=datetime.now())
    wh_proof = Column(String(100), nullable=True)


    # relationships
    admin = relationship("UserManager", back_populates="wh_admin_logs")
    stock = relationship("StockManager", back_populates="wh_logs")
    
    
    


