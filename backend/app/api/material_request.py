from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.database import db_dependency

from app.models.user import UserManager
from app.models.product import Product
from app.models.material_request import MaterialRequest, ApprovalStatus, ReleaseStatus

from app.models.release import Release

from app.schemas.material_request import (
    MaterialRequestCreate, MaterialRequestResponse,
    RequestItem, ReleaseResponse
)
from app.utils.auth import get_current_technician, get_current_supervisor, get_current_custodian, get_current_admin

router = APIRouter(prefix="/requests", tags=["Material Requests"])

# Routes for technician

# create request
@router.post("/", response_model=MaterialRequestResponse, status_code=status.HTTP_201_CREATED)
def create_request(request: MaterialRequestCreate, db=db_dependency, current_user = Depends(get_current_technician)):

    for item in request.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        if not product:
           raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {item.product_id} not found"
            ) 


    new_request = MaterialRequest(
        requestor_email = current_user.email,
        date=datetime.now(),
        approval_status=ApprovalStatus.PENDING,
        release_status = ReleaseStatus.PENDING,
        mrf_files = request.mrf_files,
        items=[item.model_dump() for item in request.items],
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request

@router.get("/sent", response_model=List[MaterialRequestResponse])
def my_requests(db:Session = db_dependency, current_user: UserManager = Depends(get_current_technician) ):
    my_requests = db.query(MaterialRequest).filter(
        MaterialRequest.requestor_email == current_user.email
    ).all()

    return my_requests

# Routes for supervisor
# see all pending
@router.get("/pending", response_model=List[MaterialRequestResponse])
def get_pending(db:Session = db_dependency, current_user = Depends(get_current_supervisor)):

    pending_requests = db.query(MaterialRequest).filter(
        MaterialRequest.approval_status == ApprovalStatus.PENDING
    ).all()

    return pending_requests


@router.get("/pending/{mrf_id}", response_model=MaterialRequestResponse, status_code=status.HTTP_200_OK)
def get_request_by_id(mrf_id: int, db=db_dependency, current_user = Depends(get_current_supervisor)):

    request = db.query(MaterialRequest).filter(
        MaterialRequest.mrf_id == mrf_id,
        MaterialRequest.approval_status == ApprovalStatus.PENDING
    ).first()

    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pending request not found"
        )

    return request 

# ROUTES FOR UPDATING STATUS


# APPROVING
@router.put("/{mrf_id}/approve", response_model=MaterialRequestResponse)
def approve_request(mrf_id:int, db=db_dependency, current_user = Depends(get_current_supervisor)):

    # get by id
    request_for_approval = db.query(MaterialRequest).filter(
        MaterialRequest.mrf_id == mrf_id,
        MaterialRequest.approval_status == ApprovalStatus.PENDING
    ).first()


    if not request_for_approval:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found"
        ) 

    # check if products have stock
    for item in request_for_approval.items:
        product = db.query(Product).filter(
            Product.id == item["product_id"]
        ).first()

        if product and product.stock < item["quantity"]:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product '{product.product_name}'. Available: {product.stock}, Requested: {item['quantity']}"
            )


    # update content
    request_for_approval.approval_status = ApprovalStatus.APPROVED
    request_for_approval.approved_by = current_user.email

    db.commit()
    db.refresh(request_for_approval)

    # return
    return request_for_approval

# DISAPPROVING
@router.put("/{mrf_id}/disapprove", response_model=MaterialRequestResponse)
def disapprove_request(mrf_id:int, db=db_dependency, current_user=Depends(get_current_supervisor)):\

    # get by id
    request_for_disapproval = db.query(MaterialRequest).filter(
        MaterialRequest.mrf_id == mrf_id
    ).first()
    
    # error handling
    if not request_for_disapproval:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This Request Does Not Exist."
        )

    # update content

    request_for_disapproval.approval_status = ApprovalStatus.NOT_APPROVED
    request_for_disapproval.approved_by = current_user.email

    db.commit()
    db.refresh(request_for_disapproval)

    # return
    return request_for_disapproval



# EDITING CONTENT
@router.put("/{mrf_id}/edit", response_model=MaterialRequestResponse, status_code=status.HTTP_200_OK)
def edit_content(mrf_id:int, edited_items: List[RequestItem], db=db_dependency, current_user = Depends(get_current_supervisor)):
    # get by id
    request_to_edit = db.query(MaterialRequest).filter(
        MaterialRequest.mrf_id == mrf_id
    ).first()

    # error handling
    if not request_to_edit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found"
        )

    if request_to_edit.approval_status != ApprovalStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot edit request that is already {request_to_edit.APPROVAL_STATUS}"
        )

    for item in edited_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {item.product_id} not found"
            )
    
    # update content
    request_to_edit.items = [item.dict() for item in edited_items]


    db.commit()
    db.refresh(request_to_edit)
    
    # return
    return request_to_edit

@router.get("/approved", response_model=List[MaterialRequestResponse])
def get_approved(db=db_dependency, current_user = Depends(get_current_custodian)):


    approved_requests = db.query(MaterialRequest).filter(
        MaterialRequest.approval_status == ApprovalStatus.APPROVED
    ).all()

    return approved_requests


# custodian routes


# get all pending 
@router.get("/release/pending", response_model=List[MaterialRequestResponse])
def get_pending_releases(db=db_dependency, current_user = Depends(get_current_custodian)):
    pending_releases = db.query(MaterialRequest).filter(
        MaterialRequest.approval_status == ApprovalStatus.APPROVED
    ).all()

    return pending_releases

# get pending by id
@router.get("/release/pending/{mrf_id}", response_model=MaterialRequestResponse)
def get_pending_release_by_id( mrf_id:int, db=db_dependency, current_user=Depends(get_current_custodian)):
    pending_release = db.query(MaterialRequest).filter(
        MaterialRequest.mrf_id == mrf_id
    ).first()

    if not pending_release:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This request does not exist"
        )

    return pending_release

# release
@router.put("/{mrf_id}/release", response_model=MaterialRequestResponse, status_code=status.HTTP_200_OK)
def release_request(mrf_id:int, db=db_dependency, current_user=Depends(get_current_custodian)):

    # get by id
    request_to_release = db.query(MaterialRequest).filter(
        MaterialRequest.mrf_id == mrf_id
    ).first()

    if not request_to_release:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This request does not exist"
            )

     # Check if already released
    if request_to_release.release_status == ReleaseStatus.RELEASED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This request has already been released"
        )
    
    # Check if approved
    if request_to_release.approval_status != ApprovalStatus.APPROVED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only approved requests can be released"
        )


    # update content

    request_to_release.release_status = ReleaseStatus.RELEASED
    request_to_release.released_by = current_user.email


    # add to release table ???

    for item in request_to_release.items:
        release = Release(
            mrf_id = request_to_release.mrf_id,
            product_id = item["product_id"],
            quantity = item["quantity"]
        )
        db.add(release)


    db.commit()
    db.refresh(request_to_release)

    # return


    return request_to_release


    
# reject
@router.put("/{mrf_id}/reject", response_model=MaterialRequestResponse, status_code=status.HTTP_200_OK)
def reject_request(mrf_id:int, db=db_dependency, current_user=Depends(get_current_custodian)):

    # get by id
    request_to_reject = db.query(MaterialRequest).filter(
        MaterialRequest.mrf_id == mrf_id
    ).first()

    if not request_to_reject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This request does not exist"
            )

     # Check if already released
    if request_to_reject.release_status == ReleaseStatus.RELEASED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This request has already been released"
        )
    
    # Check if approved
    if request_to_reject.approval_status != ApprovalStatus.APPROVED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only approved requests can be released"
        )

    # update content

    request_to_reject.release_status = ReleaseStatus.PENDING



    db.commit()
    db.refresh(request_to_reject)

    # return
    return request_to_reject


# Admin route

@router.get("/all", response_model=List[MaterialRequestResponse], status_code=status.HTTP_200_OK)
def get_all_requests(db=db_dependency, current_user = Depends(get_current_admin), skip: int = 0, limit: int = 100):
    requests = db.query(MaterialRequest).order_by(MaterialRequest.date.desc()).offset(skip).limit(limit).all()
    return requests