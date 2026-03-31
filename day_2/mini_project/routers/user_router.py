from fastapi import APIRouter, Depends, status
from models.schemas import UserCreate, UserLogin, UserResponse
from services.user_service import UserService
from repositories.json_repository import JSONRepository
from config import settings

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service() -> UserService:
    repo = JSONRepository(
        filepath=f"{settings.JSON_DB_PATH}/users.json",
        collection_key="users"
    )
    return UserService(repo)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, svc: UserService = Depends(get_user_service)):
    return svc.register(payload.model_dump())


@router.post("/login")
def login(payload: UserLogin, svc: UserService = Depends(get_user_service)):
    user = svc.login(payload.username, payload.password)
    return {"message": f"Welcome, {user['username']}!", "username": user["username"]}


@router.get("", response_model=list[UserResponse])
def list_users(svc: UserService = Depends(get_user_service)):
    users = svc.get_all_users()
    return [
        {"id": u["id"], "username": u["username"],
         "email": u["email"], "created_at": u["created_at"]}
        for u in users
    ]


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, svc: UserService = Depends(get_user_service)):
    svc.delete_user(user_id)
    return {"message": f"User {user_id} deleted successfully"}
