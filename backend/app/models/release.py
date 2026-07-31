from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class Release(Base):
    __tablename__ = "release"

    sub_id = Column(Integer, primary_key=True, index=True)
    mrf_id = Column(Integer, ForeignKey("material_request.mrf_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer)


    # Relationships

    mrf = relationship("MaterialRequest", back_populates="release")
    product = relationship("Product", back_populates="releases")
    
