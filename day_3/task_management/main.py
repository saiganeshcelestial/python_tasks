import logging
import logging.config
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import APP_NAME, DEBUG, LOG_LEVEL
from database import verify_connection, engine, Base
from middleware.logging_middleware import logging_middleware
from routers import task_router, user_router
from exceptions.custom_exceptions import TaskNotFoundError, UserNotFoundError, DuplicateUserError

# ── Logging setup ──────────────────────────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/app.log"),
    ],
)
logger = logging.getLogger("task_api")

# ── App ────────────────────────────────────────────────────────────────────────
app = FastAPI(title=APP_NAME, debug=DEBUG)

# ── Middleware ─────────────────────────────────────────────────────────────────
app.middleware("http")(logging_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Global exception handlers ──────────────────────────────────────────────────
@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(DuplicateUserError)
async def duplicate_user_handler(request: Request, exc: DuplicateUserError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


# ── Startup ────────────────────────────────────────────────────────────────────
@app.on_event("startup")
def on_startup():
    logger.info(f"Starting {APP_NAME}…")
    verify_connection()
    # Create tables if they don't exist yet (Alembic handles migrations in production)
    # Base.metadata.create_all(bind=engine)  # uncomment only during dev without Alembic


# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(user_router.router)
app.include_router(task_router.router)


@app.get("/")
def health():
    return {"status": "ok", "app": APP_NAME}
