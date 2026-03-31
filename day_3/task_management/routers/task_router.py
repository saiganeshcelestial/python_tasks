from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session

from database import get_db
from models.schemas import TaskCreate, TaskUpdate, TaskResponse
from repositories.sqlalchemy_repository import SQLAlchemyTaskRepository
from services.task_service import TaskService
from exceptions.custom_exceptions import TaskNotFoundError

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(SQLAlchemyTaskRepository(db))


# ── Background task helper ─────────────────────────────────────────────────────

def log_notification(title: str, owner_id: int) -> None:
    """Writes a notification entry to notifications.log (runs in background)."""
    ts = datetime.utcnow().isoformat(timespec="seconds")
    line = f"[{ts}] Task '{title}' created by user_id={owner_id} — notification sent\n"
    with open("notifications.log", "a") as f:
        f.write(line)


# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    background_tasks: BackgroundTasks,
    svc: TaskService = Depends(get_service),
):
    task = svc.create(payload)
    # Fire-and-forget: log notification after response is sent
    background_tasks.add_task(log_notification, task.title, task.owner_id)
    return task


@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    status: str | None = None,
    svc: TaskService = Depends(get_service),
):
    if status:
        return svc.get_by_status(status)
    return svc.get_all()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, svc: TaskService = Depends(get_service)):
    try:
        return svc.get_by_id(task_id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    svc: TaskService = Depends(get_service),
):
    try:
        return svc.update(task_id, payload)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{task_id}", response_model=TaskResponse)
def delete_task(task_id: int, svc: TaskService = Depends(get_service)):
    try:
        return svc.delete(task_id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
