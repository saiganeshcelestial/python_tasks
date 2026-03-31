import logging
from sqlalchemy.orm import Session

from models.db_models import Loan, User
from models.enums import LoanStatus, LoanPurpose, EmploymentStatus
from decorators.timer import timer

logger = logging.getLogger(__name__)


class AnalyticsService:
    def __init__(self, db: Session):
        self._db = db

    @timer
    def get_summary(self) -> dict:
        all_loans: list[Loan] = self._db.query(Loan).all()
        total_users: int = self._db.query(User).count()

        # Dict comprehension: status breakdown
        status_counts = {
            status.value: sum(1 for l in all_loans if l.status == status)
            for status in LoanStatus
        }

        # Dict comprehension: loans by purpose
        loans_by_purpose = {
            purpose.value: sum(1 for l in all_loans if l.purpose == purpose)
            for purpose in LoanPurpose
        }

        # Dict comprehension: loans by employment
        loans_by_employment = {
            emp.value: sum(1 for l in all_loans if l.employment_status == emp)
            for emp in EmploymentStatus
        }

        # List comprehension: approved amounts only → total disbursed
        approved_amounts = [l.amount for l in all_loans if l.status == LoanStatus.approved]
        total_disbursed = sum(approved_amounts)

        # List comprehension: average loan amount across all loans
        all_amounts = [l.amount for l in all_loans]
        avg_loan_amount = round(sum(all_amounts) / len(all_amounts), 2) if all_amounts else 0

        return {
            "total_users": total_users,
            "total_loans": len(all_loans),
            "pending_loans": status_counts.get("pending", 0),
            "approved_loans": status_counts.get("approved", 0),
            "rejected_loans": status_counts.get("rejected", 0),
            "total_disbursed_amount": total_disbursed,
            "loans_by_purpose": loans_by_purpose,
            "loans_by_employment": loans_by_employment,
            "avg_loan_amount": avg_loan_amount,
        }
