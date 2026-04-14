from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .auth_models import CurrentUserResponse, TokenResponse, UserLogin, UserRegister
from .db import get_db
from .orm_models import UserORM
from .security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=CurrentUserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    payload: UserRegister,
    db: Session = Depends(get_db),
) -> CurrentUserResponse:
    existing_user = db.scalar(select(UserORM).where(UserORM.email == payload.email))
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = UserORM(
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return CurrentUserResponse(id=user.id, email=user.email)


@router.post("/login", response_model=TokenResponse)
def login_user(
    payload: UserLogin,
    db: Session = Depends(get_db),
) -> TokenResponse:
    user = db.scalar(select(UserORM).where(UserORM.email == payload.email))
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(subject=user.email)
    return TokenResponse(access_token=access_token)