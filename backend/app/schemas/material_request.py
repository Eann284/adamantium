from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum



class ApprovalStatusEnum(str, Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    NOT_APPROVED = "Not Approved"

class ReleaseStatusEnum(str, Enum):
    PENDING = "Pending"
    RELEASED = "Released"
    NOT_RELEASED = "Not Released"


class RequestItem(BaseModel):
    product_id: int
    quantity: int

class MaterialRequestCreate(BaseModel):
    items: List[RequestItem]
    mrf_files: Optional[str] = None

class MaterialRequestResponse(BaseModel):
    mrf_id: int
    requestor_email: str
    date: datetime 
    approval_status: ApprovalStatusEnum
    approved_by: Optional[str]
    release_status: ReleaseStatusEnum
    released_by: Optional[str]
    mrf_files: str
    items: List[dict]

    class Config:
        from_attributes = True
        extra = "allow"

class ReleaseResponse(BaseModel):
    sub_id: int
    mrf_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True
        extra = "allow"


