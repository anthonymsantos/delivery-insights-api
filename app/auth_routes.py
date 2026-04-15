from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from .auth_models import CurrentUserResponse, TokenResponse, UserRegister
from .db import get_db
from .orm_models import UserORM
from .security import create_access_token, decode_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserORM:
    payload = decode_access_token(token)
    email = payload.get("sub")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = db.scalar(select(UserORM).where(UserORM.email == email))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


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
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenResponse:
    user = db.scalar(select(UserORM).where(UserORM.email == form_data.username))
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(subject=user.email)
    return TokenResponse(access_token=access_token)


@router.get("/me", response_model=CurrentUserResponse)
def read_current_user(
    current_user: UserORM = Depends(get_current_user),
) -> CurrentUserResponse:
    return CurrentUserResponse(
        id=current_user.id,
        email=current_user.email,
    )