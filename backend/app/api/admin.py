from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.utils.database import db_dependency
from app.models.user import UserManager
from app.models.product import Product
from app.models.material_request import MaterialRequest, ApprovalStatus
from app.utils.auth import get_current_admin
from app.schemas.user import UserResponse
from typing import List

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dash")
def get_dash(db: Session = db_dependency, current_user = Depends(get_current_admin)):

    total_users = db.query(func.count(UserManager.id)).scalar()
    total_products = db.query(func.count(Product.id)).scalar()

    pending_requests = db.query(func.count(MaterialRequest.mrf_id)).filter(
        MaterialRequest.approval_status == ApprovalStatus.PENDING
    ).scalar()

    return {
        "totalUsers": total_users or 0,
        "totalProducts": total_products or 0,
        "pendingRequests": pending_requests or 0,
    }

@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    db: Session = db_dependency,
    skip: int = 0, limit:int = 10,
    current_user = Depends(get_current_admin)
):
    users = db.query(UserManager).offset(skip).limit(limit).all()
    return users
