import logging
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from models.db_models import User
from models.schemas import UserCreate, UserLogin
from models.enums import UserRole
from repositories.sqlalchemy_repository import SQLAlchemyRepository
from exceptions.custom_exceptions import (
    DuplicateUserError,
    InvalidCredentialsError,
    UserNotFoundError,
)
from decorators.timer import timer

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, db: Session):
        self._repo = SQLAlchemyRepository(User, db)
        self._db = db

    @timer
    def register(self, data: UserCreate) -> User:
        existing_username = self._db.query(User).filter(User.username == data.username).first()
        if existing_username:
            logger.warning(f"Duplicate username attempt: {data.username}")
            raise DuplicateUserError(f"Username '{data.username}' is already taken.")

        existing_email = self._db.query(User).filter(User.email == data.email).first()
        if existing_email:
            logger.warning(f"Duplicate email attempt: {data.email}")
            raise DuplicateUserError(f"Email '{data.email}' is already registered.")

        hashed_pw = pwd_context.hash(data.password)
        user = User(
            username=data.username,
            email=data.email,
            password=hashed_pw,
            phone=data.phone,
            monthly_income=data.monthly_income,
            role=UserRole.user,
        )
        created = self._repo.save(user)
        logger.info(f"User registered: {created.username}")
        return created

    @timer
    def authenticate(self, data: UserLogin) -> User:
        user = self._db.query(User).filter(User.username == data.username).first()
        if not user:
            logger.error(f"Login attempt for non-existent user: {data.username}")
            raise InvalidCredentialsError("Invalid username or password.")
        if not pwd_context.verify(data.password, user.password):
            logger.warning(f"Wrong password for user: {data.username}")
            raise InvalidCredentialsError("Invalid username or password.")
        logger.info(f"User logged in: {user.username} (role={user.role})")
        return user

    def get_by_id(self, user_id: int) -> User:
        user = self._repo.find(user_id)
        if not user:
            raise UserNotFoundError(f"User with id={user_id} not found.")
        return user

    def seed_admin(self, username: str, email: str, password: str) -> None:
        existing = self._db.query(User).filter(User.username == username).first()
        if existing:
            logger.info("Admin user already exists.")
            return
        hashed_pw = pwd_context.hash(password)
        admin = User(
            username=username,
            email=email,
            password=hashed_pw,
            phone="0000000000",
            monthly_income=0,
            role=UserRole.admin,
        )
        self._repo.save(admin)
        logger.info("Admin user seeded successfully.")
