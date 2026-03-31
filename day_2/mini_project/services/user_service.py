from datetime import datetime
from repositories.base_repository import BaseRepository
from exceptions.custom_exceptions import (
    UserNotFoundError, DuplicateUserError, InvalidCredentialsError
)
import logging

logger = logging.getLogger("user_service")


class UserService:
    def __init__(self, repo: BaseRepository):
        self._repo = repo

    def _now(self):
        return datetime.now().isoformat(timespec="seconds")

    def register(self, data: dict) -> dict:
        existing = [u for u in self._repo.find_all() if u["username"] == data["username"]]
        if existing:
            logger.warning(f"Duplicate username: '{data['username']}'")
            raise DuplicateUserError(data["username"])

        user = {
            "id": self._repo.next_id(),
            "username": data["username"],
            "email": data["email"],
            "password": data["password"],   # hash in production
            "created_at": self._now(),
        }
        result = self._repo.save(user)
        logger.info(f"User '{result['username']}' registered")
        return result

    def login(self, username: str, password: str) -> dict:
        users = self._repo.find_all()
        user = next((u for u in users if u["username"] == username), None)
        if not user or user["password"] != password:
            logger.warning(f"Failed login for '{username}'")
            raise InvalidCredentialsError()
        logger.info(f"User '{username}' logged in")
        return user

    def get_all_users(self) -> list:
        logger.info("User list accessed")
        return self._repo.find_all()

    def delete_user(self, user_id: int) -> bool:
        user = self._repo.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        self._repo.delete(user_id)
        logger.info(f"User id={user_id} deleted")
        return True
