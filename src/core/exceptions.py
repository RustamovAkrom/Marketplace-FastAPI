from fastapi import FastAPI, status
from fastapi.responses import JSONResponse


class APIException(Exception):
    def __init__(
        self,
        message: str,
        *,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: dict | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}

    def to_dict(self):
        return {"message": self.message, "details": self.details}


def register_error_handler(app: FastAPI):

    @app.exception_handler(APIException)
    async def api_exception_handler(_, exc: APIException):
        return JSONResponse(status_code=exc.status_code, content=exc.to_dict())
