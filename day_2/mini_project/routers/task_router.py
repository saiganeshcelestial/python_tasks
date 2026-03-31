from fastapi import APIRouter, Depends, status
from typing import Optional
from models.schemas import TaskCreate, TaskUpdate, TaskResponse
from services.task_service import TaskService
from repositories.json_repository import JSONRepository
from config import settings

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_task_service() -> TaskService:
    repo = JSONRepository(
        filepath=f"{settings.JSON_DB_PATH}/tasks.json",
        collection_key="tasks"
    )
    return TaskService(repo)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, svc: TaskService = Depends(get_task_service)):
    return svc.create_task(payload.model_dump())


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    task_status: Optional[str] = None,
    priority: Optional[str] = None,
    owner: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    svc: TaskService = Depends(get_task_service),
):
    return svc.get_all_tasks(
        status=task_status, priority=priority,
        owner=owner, page=page, limit=limit
    )


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, svc: TaskService = Depends(get_task_service)):
    return svc.get_task(task_id)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, payload: TaskUpdate, svc: TaskService = Depends(get_task_service)):
    return svc.update_task(task_id, payload.model_dump())


@router.patch("/{task_id}", response_model=TaskResponse)
def partial_update_task(task_id: int, payload: TaskUpdate, svc: TaskService = Depends(get_task_service)):
    return svc.update_task(task_id, payload.model_dump(exclude_none=True))


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, svc: TaskService = Depends(get_task_service)):
    svc.delete_task(task_id)
    return {"message": f"Task {task_id} deleted successfully"}
