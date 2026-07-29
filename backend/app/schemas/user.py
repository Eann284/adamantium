from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = "Admin"
    SUPERVISOR = "Supervisor"
    CUSTODIAN = "Custodian"
    TECHNICIAN = "Technician"

class AreaEnum(str, Enum):
    CAVITE = "Cavite"
    LAGUNA = "Laguna"
    QUEZON = "Quezon"
    RIZAL = "Rizal"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: RoleEnum
    area: AreaEnum

class UserResponse(BaseModel):
    ID: int
    Name: str
    Email: str
    Role: str
    Area: str
    Stock: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None