from models.db_models import User
from models.schemas import UserCreate
from repositories.base_repository import BaseRepository
from exceptions.custom_exceptions import UserNotFoundError, DuplicateUserError


class UserService:
    """Business logic for users. Depends only on BaseRepository — backend-agnostic."""

    def __init__(self, repo: BaseRepository):
        self.repo = repo

    def create(self, data: UserCreate) -> User:
        # DuplicateUserError is raised by the repository on IntegrityError
        user = User(
            username=data.username,
            email=data.email,
            password=data.password,   # hash in production!
        )
        return self.repo.save(user)

    def get_all(self):
        return self.repo.find_all()

    def get_by_id(self, user_id: int) -> User:
        user = self.repo.find(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user

    def delete(self, user_id: int) -> User:
        user = self.repo.delete(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user
