import logging
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from config import settings
from routers import task_router, user_router
from middleware.logging_middleware import logging_middleware
from exceptions.custom_exceptions import (
    TaskNotFoundError, UserNotFoundError,
    DuplicateUserError, InvalidCredentialsError
)

# ─── Logging setup ───────────────────────────────────────────
os.makedirs("logs", exist_ok=True)
os.makedirs(settings.JSON_DB_PATH, exist_ok=True)

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL, logging.INFO),
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("main")

# ─── App ─────────────────────────────────────────────────────
app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

# ─── Middleware ───────────────────────────────────────────────
app.middleware("http")(logging_middleware)

# ─── Routers ─────────────────────────────────────────────────
app.include_router(user_router.router)
app.include_router(task_router.router)


# ─── Exception Handlers ──────────────────────────────────────
def error_response(error: str, message: str, status_code: int):
    return JSONResponse(
        status_code=status_code,
        content={"error": error, "message": message, "status_code": status_code}
    )


@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    return error_response("TaskNotFoundError", str(exc), 404)


@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return error_response("UserNotFoundError", str(exc), 404)


@app.exception_handler(DuplicateUserError)
async def duplicate_user_handler(request: Request, exc: DuplicateUserError):
    return error_response("DuplicateUserError", str(exc), 409)


@app.exception_handler(InvalidCredentialsError)
async def invalid_creds_handler(request: Request, exc: InvalidCredentialsError):
    return error_response("InvalidCredentialsError", str(exc), 401)


@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    return error_response("ValidationError", str(exc.errors()), 422)


# ─── Health ───────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy", "app": settings.APP_NAME}


# ─── Startup ──────────────────────────────────────────────────
@app.on_event("startup")
def startup():
    logger.info(
        f"App: {settings.APP_NAME} | Debug: {settings.DEBUG} | DB: {settings.JSON_DB_PATH}"
    )

