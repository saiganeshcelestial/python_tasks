import logging
import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from config import settings
from database import engine, SessionLocal
from models import db_models  # noqa: F401 — ensures models are registered with Base
from middleware.logging_middleware import LoggingMiddleware
from routers import auth_router, loan_router, admin_router, analytics_router
from exceptions.custom_exceptions import register_exception_handlers
from services.user_service import UserService

# ─── Logging setup ────────────────────────────────────────────────────────────

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s - %(levelname)s - %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "standard"},
        "app_file": {
            "class": "logging.FileHandler",
            "filename": "logs/app.log",
            "formatter": "standard",
        },
        "notification_file": {
            "class": "logging.FileHandler",
            "filename": "logs/notifications.log",
            "formatter": "standard",
        },
    },
    "loggers": {
        "": {"handlers": ["console", "app_file"], "level": settings.log_level},
        "notifications": {
            "handlers": ["notification_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
})

logger = logging.getLogger(__name__)


# ─── Lifespan: seed admin on startup ─────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        service = UserService(db)
        service.seed_admin(
            username=settings.admin_username,
            email=settings.admin_email,
            password=settings.admin_password,
        )
    finally:
        db.close()
    yield


# ─── App factory ─────────────────────────────────────────────────────────────

app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

app.add_middleware(LoggingMiddleware)

register_exception_handlers(app)

app.include_router(auth_router.router)
app.include_router(loan_router.router)
app.include_router(admin_router.router)
app.include_router(analytics_router.router)


# ─── Health check ─────────────────────────────────────────────────────────────

@app.get("/health", tags=["Utility"])
def health_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as exc:
        logger.error(f"Health check failed: {exc}")
        return {"status": "error", "database": str(exc)}
