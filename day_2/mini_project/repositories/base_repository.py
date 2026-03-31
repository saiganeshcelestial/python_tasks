from abc import ABC, abstractmethod
from typing import Optional


class BaseRepository(ABC):
    """Abstract interface for data access — ISP: only data ops, no logging or validation."""

    @abstractmethod
    def find_all(self) -> list:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[dict]:
        pass

    @abstractmethod
    def save(self, record: dict) -> dict:
        pass

    @abstractmethod
    def update(self, id: int, updates: dict) -> Optional[dict]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    def next_id(self) -> int:
        pass
