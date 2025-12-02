from typing import Any, Optional

from pydantic import BaseModel


class ErrorResponseScheme(BaseModel):
    success: bool = False
    code: str
    detail: str
    trace_id: Optional[str] = None
    values: Optional[dict[str, Any]] = None


__all__ = ("ErrorResponseScheme",)
