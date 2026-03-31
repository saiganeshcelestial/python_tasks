import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from models.db_models import Loan, User
from models.schemas import LoanCreate, LoanReview
from models.enums import LoanStatus
from repositories.sqlalchemy_repository import SQLAlchemyRepository
from exceptions.custom_exceptions import (
    LoanNotFoundError,
    MaxPendingLoansError,
    InvalidLoanReviewError,
    ForbiddenError,
)
from decorators.timer import timer

logger = logging.getLogger(__name__)

MAX_PENDING_LOANS = 3


class LoanService:
    def __init__(self, db: Session):
        self._repo = SQLAlchemyRepository(Loan, db)
        self._db = db

    @timer
    def apply(self, data: LoanCreate, user: User) -> Loan:
        if user.role.value == "admin":
            raise ForbiddenError("Admins cannot apply for loans.")

        pending_count = (
            self._db.query(Loan)
            .filter(Loan.user_id == user.id, Loan.status == LoanStatus.pending)
            .count()
        )
        if pending_count >= MAX_PENDING_LOANS:
            logger.warning(f"User {user.username} hit max pending loans limit.")
            raise MaxPendingLoansError()

        loan = Loan(
            user_id=user.id,
            amount=data.amount,
            purpose=data.purpose,
            tenure_months=data.tenure_months,
            employment_status=data.employment_status,
        )
        created = self._repo.save(loan)
        logger.info(f"Loan #{created.id} applied by {user.username} — ₹{data.amount} for {data.purpose}")
        return created

    @timer
    def review(self, loan_id: int, data: LoanReview, admin_username: str) -> Loan:
        loan = self._repo.find(loan_id)
        if not loan:
            raise LoanNotFoundError(f"Loan #{loan_id} not found.")
        if loan.status != LoanStatus.pending:
            logger.warning(f"Re-review attempt on loan #{loan_id} by {admin_username}.")
            raise InvalidLoanReviewError(f"Loan #{loan_id} has already been reviewed.")

        try:
            loan.status = data.status
            loan.admin_remarks = data.admin_remarks
            loan.reviewed_by = admin_username
            loan.reviewed_at = datetime.now(timezone.utc)
            updated = self._repo.update(loan)
        except Exception as exc:
            self._db.rollback()
            logger.error(f"Transaction failed for loan #{loan_id}: {exc}")
            raise

        logger.info(f"Loan #{loan_id} {data.status.value} by {admin_username}.")
        return updated

    def get_my_loan(self, loan_id: int, user_id: int) -> Loan:
        loan = self._repo.find(loan_id)
        if not loan or loan.user_id != user_id:
            raise LoanNotFoundError(f"Loan #{loan_id} not found.")
        return loan

    def get_my_loans(
        self, user_id: int, status: str = None, page: int = 1, limit: int = 10
    ) -> list[Loan]:
        query = self._db.query(Loan).filter(Loan.user_id == user_id)
        if status:
            query = query.filter(Loan.status == status)
        offset = (page - 1) * limit
        return query.offset(offset).limit(limit).all()

    def get_all_loans(
        self,
        status: str = None,
        user_id: int = None,
        purpose: str = None,
        employment_status: str = None,
        page: int = 1,
        limit: int = 10,
        sort_by: str = "applied_at",
        order: str = "desc",
    ) -> list[Loan]:
        query = self._db.query(Loan)
        if status:
            query = query.filter(Loan.status == status)
        if user_id:
            query = query.filter(Loan.user_id == user_id)
        if purpose:
            query = query.filter(Loan.purpose == purpose)
        if employment_status:
            query = query.filter(Loan.employment_status == employment_status)

        sort_col = getattr(Loan, sort_by, Loan.applied_at)
        query = query.order_by(sort_col.desc() if order == "desc" else sort_col.asc())
        offset = (page - 1) * limit
        return query.offset(offset).limit(limit).all()

    def get_loan_by_id(self, loan_id: int) -> Loan:
        loan = self._repo.find(loan_id)
        if not loan:
            raise LoanNotFoundError(f"Loan #{loan_id} not found.")
        return loan
