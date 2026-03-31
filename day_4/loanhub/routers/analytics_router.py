from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from services.analytics_service import AnalyticsService
from decorators.auth import require_role

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary")
def get_summary(
    current_user: dict = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    return AnalyticsService(db).get_summary()
