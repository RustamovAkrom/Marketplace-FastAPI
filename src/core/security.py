import uuid
from datetime import datetime, timedelta, timezone
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
    return datetime.now(timezone.utc)


def _jti() -> str:
    return str(uuid.uuid4())


def _to_ts(dt: datetime) -> int:
    return int(dt.timestamp())


def create_token(
    subject: Union[str, int, Dict[str, Any]],
    token_type: str = "access",
    extra: Optional[Dict[str, Any]] = None,
    expires_delta: Optional[timedelta] = None,
):
    if isinstance(subject, dict):
        payload = subject.copy()
    else:
        payload = {"sub": str(subject)}

    payload.setdefault("type", token_type)
    payload.setdefault("jti", _jti())
    payload.setdefault("iat", _to_ts(_now()))

    if extra:
        payload.update(extra)

    if expires_delta:
        exp = _now() + expires_delta
    else:
        if token_type == "access":
            exp = _now() + timedelta(
                minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES or 15
            )
        else:
            exp = _now() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRES_DAYS or 30)

    payload["exp"] = _to_ts(exp)
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


# Token factories
def create_access_token(
    subject: Union[str, int, Dict[str, Any]],
    extra: Optional[Dict[str, Any]] = None,
    expires_delta: Optional[timedelta] | None = None,
) -> str:
    """
    Create access token (JWT) with proper iat and exp timestamps.
    """
    return create_token(subject, "access", extra, expires_delta)


def create_refresh_token(
    subject: Union[str, int, Dict[str, Any]],
    extra: Optional[Dict[str, Any]] = None,
    expires_delta: Optional[timedelta] | None = None,
) -> str:
    """
    Create refresh token (JWT) with proper iat and exp timestamps.
    """
    return create_token(subject, "refresh", extra, expires_delta)


def decode_token(token: str) -> Dict[str, Any]:
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
    except ExpiredSignatureError as e:
        raise ExpiredSignatureError("token_expired") from e
    except JWTError as e:
        raise JWTError("invalid_token") from e
