import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from core.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# Hashing helpers
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Verifying helpers
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# helpers
def _now() -> datetime:
    return datetime.utcnow()


def _jti() -> str:
    return str(uuid.uuid4())


# Token factories
def create_access_token(
    subject: Union[str, int, Dict[str, Any]],
    extra: Optional[Dict[str, Any]] = None,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create access token.
    """

    if isinstance(subject, dict):
        payload_access: Dict[str, Any] = subject.copy()
    else:
        payload_access: Dict[str, Any] = {"sub": str(subject)}  # type: ignore

    payload_access.setdefault("type", "access")
    payload_access.setdefault("jti", _jti())
    payload_access.setdefault("iat", int(_now().timestamp()))

    if extra:
        payload_access.update(extra)

    if expires_delta:
        exp = _now() + expires_delta
    else:
        exp = _now() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES or 15)

    payload_access["exp"] = int(exp.timestamp())

    return jwt.encode(
        payload_access, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


def create_refresh_token(
    subject: Union[str, int, Dict[str, Any]],
    extra: Optional[Dict[str, Any]] = None,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create refresh token.
    """

    if isinstance(subject, dict):
        payload_refresh: Dict[str, Any] = subject.copy()
    else:
        payload_refresh: Dict[str, Any] = {"sub": str(subject)}  # type: ignore

    payload_refresh.setdefault("type", "refresh")
    payload_refresh.setdefault("jti", _jti())
    payload_refresh.setdefault("iat", int(_now().timestamp()))

    if extra:
        payload_refresh.update(extra)

    if expires_delta:
        exp = _now() + expires_delta
    else:
        exp = _now() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRES_DAYS or 30)

    payload_refresh["exp"] = int(exp.timestamp())

    return jwt.encode(
        payload_refresh, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except ExpiredSignatureError:
        raise ExpiredSignatureError("Token has expired")

    except JWTError:
        raise JWTError("Invalid token")
