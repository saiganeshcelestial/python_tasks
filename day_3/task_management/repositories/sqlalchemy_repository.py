from typing import Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from repositories.base_repository import BaseRepository
from models.db_models import Task, User
from exceptions.custom_exceptions import DuplicateUserError, UserNotFoundError, TaskNotFoundError


# ── Task Repository ────────────────────────────────────────────────────────────

class SQLAlchemyTaskRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, entity: Task) -> Task:
        try:
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except IntegrityError as e:
            self.session.rollback()
            raise ValueError(f"Could not save task: {e.orig}") from e

    def find(self, entity_id: int) -> Optional[Task]:
        return self.session.query(Task).filter_by(id=entity_id).first()

    def find_all(self) -> List[Task]:
        return self.session.query(Task).all()

    def find_by_status(self, status: str) -> List[Task]:
        return self.session.query(Task).filter_by(status=status).all()

    def find_by_owner(self, owner_id: int) -> List[Task]:
        return self.session.query(Task).filter_by(owner_id=owner_id).all()

    def update(self, entity_id: int, data: dict) -> Optional[Task]:
        task = self.find(entity_id)
        if not task:
            return None
        for field, value in data.items():
            if value is not None:
                setattr(task, field, value)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, entity_id: int) -> Optional[Task]:
        task = self.find(entity_id)
        if task:
            self.session.delete(task)
            self.session.commit()
        return task


# ── User Repository ────────────────────────────────────────────────────────────

class SQLAlchemyUserRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, entity: User) -> User:
        try:
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except IntegrityError:
            self.session.rollback()
            raise DuplicateUserError(entity.username)

    def find(self, entity_id: int) -> Optional[User]:
        return self.session.query(User).filter_by(id=entity_id).first()

    def find_by_username(self, username: str) -> Optional[User]:
        return self.session.query(User).filter_by(username=username).first()

    def find_all(self) -> List[User]:
        return self.session.query(User).all()

    def update(self, entity_id: int, data: dict) -> Optional[User]:
        user = self.find(entity_id)
        if not user:
            return None
        for field, value in data.items():
            if value is not None:
                setattr(user, field, value)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, entity_id: int) -> Optional[User]:
        user = self.find(entity_id)
        if user:
            self.session.delete(user)
            self.session.commit()
        return user
