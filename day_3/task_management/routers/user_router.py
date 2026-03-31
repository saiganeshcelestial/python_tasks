from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.schemas import UserCreate, UserResponse
from repositories.sqlalchemy_repository import SQLAlchemyUserRepository
from services.user_service import UserService
from exceptions.custom_exceptions import UserNotFoundError, DuplicateUserError

router = APIRouter(prefix="/users", tags=["Users"])


def get_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(SQLAlchemyUserRepository(db))


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, svc: UserService = Depends(get_service)):
    try:
        return svc.create(payload)
    except DuplicateUserError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/", response_model=list[UserResponse])
def list_users(svc: UserService = Depends(get_service)):
    return svc.get_all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, svc: UserService = Depends(get_service)):
    try:
        return svc.get_by_id(user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, svc: UserService = Depends(get_service)):
    try:
        return svc.delete(user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
