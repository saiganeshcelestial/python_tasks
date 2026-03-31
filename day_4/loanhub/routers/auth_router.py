from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from models.schemas import UserCreate, UserResponse, UserLogin, TokenResponse
from services.user_service import UserService
from utils.jwt_handler import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.register(data)
    return user


@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.authenticate(credentials)
    token = create_access_token({
        "sub": user.username,
        "user_id": user.id,
        "role": user.role.value,
    })
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        username=user.username,
        role=user.role.value,
    )
