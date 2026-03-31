from fastapi import Request
from fastapi.responses import JSONResponse


class UserNotFoundError(Exception):
    pass


class DuplicateUserError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class ForbiddenError(Exception):
    pass


class LoanNotFoundError(Exception):
    pass


class MaxPendingLoansError(Exception):
    pass


class InvalidLoanReviewError(Exception):
    pass


class TokenExpiredError(Exception):
    pass


class RateLimitError(Exception):
    pass


def _response(error: str, message: str, status_code: int) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": error, "message": message, "status_code": status_code},
    )


def register_exception_handlers(app):
    @app.exception_handler(UserNotFoundError)
    async def user_not_found(request: Request, exc: UserNotFoundError):
        return _response("UserNotFoundError", str(exc) or "User not found.", 404)

    @app.exception_handler(DuplicateUserError)
    async def duplicate_user(request: Request, exc: DuplicateUserError):
        return _response("DuplicateUserError", str(exc) or "Username or email already exists.", 409)

    @app.exception_handler(InvalidCredentialsError)
    async def invalid_credentials(request: Request, exc: InvalidCredentialsError):
        return _response("InvalidCredentialsError", str(exc) or "Invalid username or password.", 401)

    @app.exception_handler(ForbiddenError)
    async def forbidden(request: Request, exc: ForbiddenError):
        return _response("ForbiddenError", str(exc) or "Access forbidden.", 403)

    @app.exception_handler(LoanNotFoundError)
    async def loan_not_found(request: Request, exc: LoanNotFoundError):
        return _response("LoanNotFoundError", str(exc) or "Loan not found.", 404)

    @app.exception_handler(MaxPendingLoansError)
    async def max_pending(request: Request, exc: MaxPendingLoansError):
        return _response(
            "MaxPendingLoansError",
            "You already have 3 pending loans. Wait for review before applying again.",
            422,
        )

    @app.exception_handler(InvalidLoanReviewError)
    async def invalid_review(request: Request, exc: InvalidLoanReviewError):
        return _response(
            "InvalidLoanReviewError",
            str(exc) or "This loan has already been reviewed.",
            422,
        )

    @app.exception_handler(TokenExpiredError)
    async def token_expired(request: Request, exc: TokenExpiredError):
        return _response("TokenExpiredError", "Your session has expired. Please log in again.", 401)

    @app.exception_handler(RateLimitError)
    async def rate_limit(request: Request, exc: RateLimitError):
        return _response("RateLimitError", str(exc) or "Too many requests. Please slow down.", 429)
