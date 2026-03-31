from abc import ABC, abstractmethod
from typing import Any, List, Optional


class BaseRepository(ABC):
    """Abstract repository interface.
    Any storage backend (JSON, SQLAlchemy, Redis, …) must implement these five methods.
    Services depend ONLY on this interface — swapping backends requires zero service changes.
    """

    @abstractmethod
    def save(self, entity: Any) -> Any:
        """Persist a new entity and return it (with generated id populated)."""
        ...

    @abstractmethod
    def find(self, entity_id: int) -> Optional[Any]:
        """Return the entity with the given id, or None if not found."""
        ...

    @abstractmethod
    def find_all(self) -> List[Any]:
        """Return all entities."""
        ...

    @abstractmethod
    def update(self, entity_id: int, data: dict) -> Optional[Any]:
        """Apply `data` dict as field updates; return updated entity or None."""
        ...

    @abstractmethod
    def delete(self, entity_id: int) -> Optional[Any]:
        """Delete entity by id; return the deleted entity or None."""
        ...
