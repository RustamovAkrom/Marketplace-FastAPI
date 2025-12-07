from typing import Any

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    code: str
    detail: str
    values: dict[str, Any] = {}


class APIException(Exception):
    """
    Base application exception use in services.
    message/detail and numeric status_code stored here.
    code - machine-readable error code (eg. 'user_exists').
    """

    def __init__(
        self,
        detail: str | None = None,
        *,
        status_code: int = 500,
        code: str | None = None,
        values: dict[str, Any] | None = None,
    ):
        self.detail = detail or "Internal server error"
        self.status_code = status_code
        self.code = code or "error"
        self.values = values or {}
        super().__init__(self.detail)


def register_error_handler(app: FastAPI) -> None:

    @app.exception_handler(APIException)
    async def api_exception_handler(_, exc: APIException):
        if isinstance(exc, APIException):
            payload = {"code": exc.code, "detail": exc.detail, "values": exc.values}
            return JSONResponse(status_code=exc.status_code, content=payload)

        # Fallback: unexpected exception -> 500 but not leak internals
        return JSONResponse(
            status_code=500,
            content={
                "code": "internal_server_error",
                "detail": "Internal server error",
            },
        )
