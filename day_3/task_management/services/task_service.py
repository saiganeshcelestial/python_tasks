from models.db_models import Task
from models.schemas import TaskCreate, TaskUpdate
from repositories.base_repository import BaseRepository
from exceptions.custom_exceptions import TaskNotFoundError


class TaskService:
    """Business logic for tasks. Depends only on BaseRepository — backend-agnostic."""

    def __init__(self, repo: BaseRepository):
        self.repo = repo

    def create(self, data: TaskCreate) -> Task:
        task = Task(
            title=data.title,
            description=data.description,
            status=data.status.value,
            priority=data.priority.value,
            owner_id=data.owner_id,
        )
        return self.repo.save(task)

    def get_all(self):
        return self.repo.find_all()

    def get_by_id(self, task_id: int) -> Task:
        task = self.repo.find(task_id)
        if not task:
            raise TaskNotFoundError(task_id)
        return task

    def get_by_status(self, status: str):
        if hasattr(self.repo, "find_by_status"):
            return self.repo.find_by_status(status)
        return [t for t in self.repo.find_all() if t.status == status]

    def update(self, task_id: int, data: TaskUpdate) -> Task:
        updates = {k: v for k, v in data.model_dump().items() if v is not None}
        task = self.repo.update(task_id, updates)
        if not task:
            raise TaskNotFoundError(task_id)
        return task

    def delete(self, task_id: int) -> Task:
        task = self.repo.delete(task_id)
        if not task:
            raise TaskNotFoundError(task_id)
        return task
