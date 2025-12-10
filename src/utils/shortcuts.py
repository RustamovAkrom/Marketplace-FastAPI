import inspect
from typing import Awaitable, TypeVar, Union

from fastapi import HTTPException, status

T = TypeVar("T")  # универсальный тип


async def get_or_404(obj: Union[T, Awaitable[T]], message: str = "not found") -> T:
    """
    Проверяет объект на None, если передан awaitable — ждёт результат.
    Возвращает объект или кидает HTTPException 404.
    """
    if inspect.isawaitable(obj):
        obj = await obj  # type: ignore

    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    return obj
