from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseRepository(ABC):
    """Abstract base repository — defines only CRUD methods (ISP)."""

    @abstractmethod
    def save(self, entity: Any) -> Any:
        pass

    @abstractmethod
    def find(self, entity_id: int) -> Optional[Any]:
        pass

    @abstractmethod
    def find_all(self, **filters) -> list[Any]:
        pass

    @abstractmethod
    def update(self, entity: Any) -> Any:
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        pass
