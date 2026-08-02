from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LogCreate(BaseModel):
    wh_proof: Optional[str] = None

class LogResponse(BaseModel):
    id: int 
    wh_email: str 
    date: datetime
    wh_proof: Optional[str]

    class Config:
        from_attributes = True
