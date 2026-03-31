from typing import Any, Optional, Type
from sqlalchemy.orm import Session
from repositories.base_repository import BaseRepository


class SQLAlchemyRepository(BaseRepository):
    """Concrete SQLAlchemy implementation — drop-in for any BaseRepository (LSP)."""

    def __init__(self, model: Type[Any], db: Session):
        self._model = model
        self._db = db

    def save(self, entity: Any) -> Any:
        self._db.add(entity)
        self._db.commit()
        self._db.refresh(entity)
        return entity

    def find(self, entity_id: int) -> Optional[Any]:
        return self._db.query(self._model).filter(self._model.id == entity_id).first()

    def find_all(self, **filters) -> list[Any]:
        query = self._db.query(self._model)
        for key, value in filters.items():
            if value is not None and hasattr(self._model, key):
                query = query.filter(getattr(self._model, key) == value)
        return query.all()

    def update(self, entity: Any) -> Any:
        self._db.commit()
        self._db.refresh(entity)
        return entity

    def delete(self, entity_id: int) -> bool:
        entity = self.find(entity_id)
        if not entity:
            return False
        self._db.delete(entity)
        self._db.commit()
        return True
