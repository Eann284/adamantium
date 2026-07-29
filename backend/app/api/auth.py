from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.models.user import UserManager
from app.schemas.user import UserCreate, UserResponse, Token
from app.utils.auth import (
    verify_password, 
    get_password_hash, 
    create_access_token,
    get_current_user
)
from app.config import settings


router= APIRouter(prefix = "/auth", tags=["Authentication"])


@router.post("/register", response_model = UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserManager).filter(UserManager.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # NEW USER
    hashed_password = get_password_hash(user.password)

    new_user = UserManager(
        Name=user.Name,
        Email=user.Email,
        Password=hashed_password,
        Role=user.Role,
        Area=user.Area,
        Stock=0
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

@router.post("/login", response_model = Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(UserManager).filter(UserManager.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ACCESS TOKEN
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}
    )
    return {"access_token": access_token, "token_type": "bearer"}

     
@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: UserManager = Depends(get_current_user)):
    return current_user