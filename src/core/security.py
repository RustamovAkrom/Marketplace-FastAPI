import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Union

from fastapi import HTTPException
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
    return datetime.now(timezone.utc)


def _jti() -> str:
    return str(uuid.uuid4())


# Token factories
def create_access_token(
    subject: Union[str, int, Dict[str, Any]],
    extra: Optional[Dict[str, Any]] = None,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create access token (JWT) with proper iat and exp timestamps.
    """

    if isinstance(subject, dict):
        payload: Dict[str, Any] = subject.copy()
    else:
        payload: Dict[str, Any] = {"sub": str(subject)}  # type: ignore

    payload.setdefault("type", "access")
    payload.setdefault("jti", _jti())

    now_ts = int(_now().timestamp())
    payload["iat"] = now_ts

    if extra:
        payload.update(extra)

    exp_ts = int(
        (
            _now()
            + (
                expires_delta
                or timedelta(minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES)
            )
        ).timestamp()
    )
    payload["exp"] = exp_ts

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(
    subject: Union[str, int, Dict[str, Any]],
    extra: Optional[Dict[str, Any]] = None,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create refresh token (JWT) with proper iat and exp timestamps.
    """

    if isinstance(subject, dict):
        payload: Dict[str, Any] = subject.copy()
    else:
        payload: Dict[str, Any] = {"sub": str(subject)}  # type: ignore

    payload.setdefault("type", "refresh")
    payload.setdefault("jti", _jti())
    payload["iat"] = int(_now().timestamp())

    if extra:
        payload.update(extra)

    exp_ts = int(
        (
            _now()
            + (expires_delta or timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRES_DAYS))
        ).timestamp()
    )
    payload["exp"] = exp_ts

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """
    Decode JWT token. By default, disables exp verification for internal inspection.
    Use jose.decode(token, ..., options={"verify_exp": True}) when verifying token lifetime.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_exp": True},
        )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
