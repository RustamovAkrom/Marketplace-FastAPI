from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class APIException(Exception):
    status_code: int = 500
    default_code: str = "error"
    default_detail: str = "Something went wrong."

    def __init__(
        self,
        detail: str | None = None,
        code: str | None = None,
        values: dict[str, Any] | None = None,
        status_code: int | None = None,
    ):
        self.detail = detail or self.default_detail
        self.code = code or self.default_code
        self.values = values or {}
        self.status_code = status_code or self.status_code

        super().__init__(self.detail)


async def api_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Обработчик для FastAPI, принимает Exception (требование Starlette),
    проверяет на APIException и возвращает JSONResponse.
    """
    if isinstance(exc, APIException):
        content = {
            "code": exc.code,
            "detail": exc.detail,
            "values": exc.values,
        }
        return JSONResponse(status_code=exc.status_code, content=content)

    # fallback для остальных исключений
    return JSONResponse(status_code=500, content={"code": "error", "detail": str(exc)})


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(Exception, api_exception_handler)
