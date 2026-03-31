from datetime import datetime, timedelta, timezone
from jose import JWTError, ExpiredSignatureError, jwt
from config import settings
from exceptions.custom_exceptions import InvalidCredentialsError, TokenExpiredError


def create_access_token(data: dict) -> str:
    """Creates a signed JWT access token with an expiry claim."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> dict:
    """Decodes and validates the JWT. Returns the payload dict.

    Raises:
        TokenExpiredError: if the token has passed its expiry time.
        InvalidCredentialsError: if the token is malformed or signature is invalid.
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except ExpiredSignatureError:
        raise TokenExpiredError("Your session has expired. Please log in again.")
    except JWTError:
        raise InvalidCredentialsError("Invalid or malformed token.")
