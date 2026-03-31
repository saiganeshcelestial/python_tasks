from datetime import datetime
from typing import Optional
from repositories.base_repository import BaseRepository
from exceptions.custom_exceptions import TaskNotFoundError
import logging

logger = logging.getLogger("task_service")


class TaskService:
    """Business logic for tasks. Depends on abstraction (BaseRepository), not concrete class."""

    def __init__(self, repo: BaseRepository):
        self._repo = repo

    def _now(self):
        return datetime.now().isoformat(timespec="seconds")

    def create_task(self, data: dict) -> dict:
        task = {
            "id": self._repo.next_id(),
            "title": data["title"],
            "description": data.get("description"),
            "status": data.get("status", "pending"),
            "priority": data.get("priority", "medium"),
            "owner": data["owner"],
            "created_at": self._now(),
            "updated_at": self._now(),
        }
        result = self._repo.save(task)
        logger.info(f"Task created: id={result['id']} title='{result['title']}'")
        return result

    def get_all_tasks(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        owner: Optional[str] = None,
        page: int = 1,
        limit: int = 10,
    ) -> list:
        tasks = self._repo.find_all()
        if status:
            tasks = [t for t in tasks if t["status"] == status]
        if priority:
            tasks = [t for t in tasks if t["priority"] == priority]
        if owner:
            tasks = [t for t in tasks if t["owner"] == owner]
        start = (page - 1) * limit
        return tasks[start: start + limit]

    def get_task(self, task_id: int) -> dict:
        task = self._repo.find_by_id(task_id)
        if not task:
            logger.error(f"Task ID {task_id} not found")
            raise TaskNotFoundError(task_id)
        return task

    def update_task(self, task_id: int, updates: dict) -> dict:
        self.get_task(task_id)  # raises if not found
        updates["updated_at"] = self._now()
        clean = {k: v for k, v in updates.items() if v is not None}
        result = self._repo.update(task_id, clean)
        logger.info(f"Task id={task_id} updated")
        return result

    def delete_task(self, task_id: int) -> bool:
        self.get_task(task_id)  # raises if not found
        self._repo.delete(task_id)
        logger.info(f"Task id={task_id} deleted")
        return True
