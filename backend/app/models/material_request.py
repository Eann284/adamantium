import enum

from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base



class ApprovalStatus(str,enum.Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    NOT_APPROVED = "Not Approved"


class ReleaseStatus(str,enum.Enum):
    PENDING = "Pending"
    RELEASED = "Released"
    NOT_RELEASED = "Not Released"


class MaterialRequest(Base):
    __tablename__ = "material_request"

    mrf_id = Column(Integer, primary_key=True, index=True)
    requestor_email = Column(String(50), ForeignKey("users.email")) # fk to user.email
    date = Column(DateTime)
    approval_status = Column(Enum(ApprovalStatus), default=ApprovalStatus.PENDING)
    approved_by = Column(String(50), ForeignKey("users.email"))
    release_status = Column(Enum(ApprovalStatus), default = ReleaseStatus.PENDING)
    released_by = Column(String(50), ForeignKey("users.email"))
    mrf_files = Column(String(500), nullable=True)

    items = Column(JSON, nullable=False)


    # RELATIONSHIPS
    requestor = relationship("UserManager", foreign_keys=[requestor_email], back_populates="material_request")

    approver = relationship("UserManager", foreign_keys=[approved_by], back_populates="material_request")

    releaser = relationship("UserManager", foreign_keys=[released_by], back_populates="material_request")

    releases = relationship("Release", back_populates="material_request")




