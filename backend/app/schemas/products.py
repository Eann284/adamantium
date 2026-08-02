from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    product_name: str
    product_image: Optional[str] = None
    stock: Optional[int] = 0


class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    product_image: Optional[str] = None
    stock: int

class ProductResponse(BaseModel):
    id: int
    product_name: str
    product_image: Optional[str] = None
    stock: int

    class Config:
        from_attributes = True