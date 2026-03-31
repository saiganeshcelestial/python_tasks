from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from utils.jwt_handler import decode_access_token
from exceptions.custom_exceptions import ForbiddenError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Decodes the JWT Bearer token and returns the payload dict.
    Raises InvalidCredentialsError (401) if the token is invalid or expired.
    """
    return decode_access_token(token)


def require_role(role: str):
    """Parameterised dependency factory.

    Usage:
        current_user: dict = Depends(require_role("admin"))
    """
    def _check(current_user: dict = Depends(get_current_user)) -> dict:
        if current_user.get("role") != role:
            raise ForbiddenError(f"Access restricted to '{role}' accounts only.")
        return current_user
    return _check
