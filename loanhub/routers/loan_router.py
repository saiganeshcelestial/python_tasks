from typing import Optional
from fastapi import APIRouter, Depends, BackgroundTasks, status
from sqlalchemy.orm import Session

from database import get_db
from models.schemas import LoanCreate, LoanResponse
from models.db_models import User
from services.loan_service import LoanService
from services.user_service import UserService
from decorators.auth import get_current_user
from utils.notifications import notify_loan_applied

router = APIRouter(prefix="/loans", tags=["Loans (User)"])


def _get_user(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)) -> User:
    return UserService(db).get_by_id(current_user["user_id"])


@router.post("", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
def apply_for_loan(
    data: LoanCreate,
    background_tasks: BackgroundTasks,
    user: User = Depends(_get_user),
    db: Session = Depends(get_db),
):
    service = LoanService(db)
    loan = service.apply(data, user)
    background_tasks.add_task(
        notify_loan_applied, loan.id, user.username, loan.purpose.value, loan.amount
    )
    return loan


@router.get("/my", response_model=list[LoanResponse])
def list_my_loans(
    status: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    user: User = Depends(_get_user),
    db: Session = Depends(get_db),
):
    service = LoanService(db)
    return service.get_my_loans(user.id, status=status, page=page, limit=limit)


@router.get("/my/{loan_id}", response_model=LoanResponse)
def get_my_loan(
    loan_id: int,
    user: User = Depends(_get_user),
    db: Session = Depends(get_db),
):
    service = LoanService(db)
    return service.get_my_loan(loan_id, user.id)
