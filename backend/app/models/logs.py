from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class Log(Base):

    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    wh_email = Column(String(255), ForeignKey("users.email"), nullable=False)
    date = Column(DateTime, server_default=func.now())
    wh_proof = Column(String(100), nullable=True)


    # relationships
    user = relationship("UserManager", back_populates="wh_logs")
    stock = relationship("Stock", back_populates="log_entry")
    
    
    


