from datetime import datetime

from pydantic import BaseModel
from typing import Optional
import enum 



class AreaEnum(str, enum.Enum):
    CAVITE = "Cavite"
    LAGUNA = "Laguna"
    QUEZON = "Quezon"
    RIZAL = "Rizal"


class InventoryCreate(BaseModel):
    id: int
    area: AreaEnum
    quantity: int
    wh_proof: Optional[str] = None

class InventoryUpdate(BaseModel):
    stock: Optional[int] = None
    area: Optional[AreaEnum] = None


class InventoryResponse(BaseModel):
    id: int
    product_id: int
    product_name: int
    area: AreaEnum
    stock: int

    class Config:
        from_attributes=True


class InventoryStockPerArea(BaseModel):
    product_id: int
    product_name: int
    areas: list[dict]

class TotalStockResponse(BaseModel):
    product_id: int
    product_name: int
    total_stock: int


class AddStockResponse(BaseModel):
    add_id: int
    product_id: int
    area: str
    quantity: int
    wh_id: str
    new_stock: int

    class Config:
        from_attributes = True


class AreaSummary(BaseModel):
    area: str
    total_stock: int
    product_count: int

class InventorySummaryResponse(BaseModel):
    grand_total: int
    per_area: list[AreaSummary]

class StockHistoryResponse(BaseModel):
    add_id: int
    product_name: str
    area: str
    quantity: int
    wh_id: str
    date: datetime
    wh_proof: Optional[str]

    class Config:
        from_attributes = True
