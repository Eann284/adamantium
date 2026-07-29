from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    product_name: str
    product_image: str

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    product_name: Optional[str] = None
    product_image: Optional[str] = None

class ProductResponse(ProductBase):
    product_id: int

    class Config:
        from_attributes = True
