from typing import Optional
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from database import get_db
from models.schemas import LoanReview, LoanResponse
from services.loan_service import LoanService
from decorators.auth import require_role
from utils.notifications import notify_loan_reviewed

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/loans", response_model=list[LoanResponse])
def list_all_loans(
    status: Optional[str] = None,
    user_id: Optional[int] = None,
    purpose: Optional[str] = None,
    employment_status: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "applied_at",
    order: str = "desc",
    current_user: dict = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    service = LoanService(db)
    return service.get_all_loans(
        status=status,
        user_id=user_id,
        purpose=purpose,
        employment_status=employment_status,
        page=page,
        limit=limit,
        sort_by=sort_by,
        order=order,
    )


@router.get("/loans/{loan_id}", response_model=LoanResponse)
def get_loan(
    loan_id: int,
    current_user: dict = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    return LoanService(db).get_loan_by_id(loan_id)


@router.patch("/loans/{loan_id}/review", response_model=LoanResponse)
def review_loan(
    loan_id: int,
    data: LoanReview,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    service = LoanService(db)
    loan = service.review(loan_id, data, admin_username=current_user["sub"])
    background_tasks.add_task(
        notify_loan_reviewed, loan.id, loan.applicant.username, loan.status.value
    )
    return loan
