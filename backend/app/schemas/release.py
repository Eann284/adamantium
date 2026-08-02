from pydantic import BaseModel

class ReleaseResponse(BaseModel):
    sub_id: int
    mrf_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True