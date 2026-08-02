from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class StockCreate(BaseModel):
    id: int
    quantity: int
    wh_proof: Optional[str] = None

class StockResponse(BaseModel):
    id: int
    wh_id: int
    wh_logs: str
    date: datetime
    product_id: int
    quantity: int

    class Config:
        from_attribute = True

