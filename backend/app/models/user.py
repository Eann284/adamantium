from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class RoleEnum(str, enum.Enum):
    ADMIN = "Admin"
    SUPERVISOR = "Supervisor"
    CUSTODIAN = "Custodian"
    TECHNICIAN = "Technician"

class AreaEnum(str, enum.Enum):
    CAVITE = "Cavite"
    LAGUNA = "Laguna"
    QUEZON = "Quezon"
    RIZAL = "Rizal"


class UserManager(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    area = Column(Enum(AreaEnum), nullable=False)
    stock = Column(Integer, default=0)