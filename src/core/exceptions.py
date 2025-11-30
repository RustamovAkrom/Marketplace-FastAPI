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


def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    content = {
        "code": exc.code,
        "detail": exc.detail,
        "values": exc.values,
    }
    return JSONResponse(status_code=exc.status_code, content=content)


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(APIException, api_exception_handler)
