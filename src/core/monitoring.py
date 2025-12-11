# src/core/monitoring.py
import time
from typing import Annotated

from fastapi import APIRouter, Header, Response
from prometheus_client import CONTENT_TYPE_LATEST, REGISTRY, generate_latest
from pydantic import BaseModel

from core.settings import settings

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


class HealthcheckResponse(BaseModel):
    timestamp: int


class StatusResponse(BaseModel):
    app: str = "ok"


class VersionResponse(BaseModel):
    version: str


@router.get("/healthcheck", summary="Проверить доступность сервиса")
def ping() -> HealthcheckResponse:
    return HealthcheckResponse(timestamp=int(time.time()))


@router.get("/status", summary="Проверить статус используемых сервисов")
async def status() -> StatusResponse:
    # optionally add DB/Redis checks here (non-blocking or with timeout)
    return StatusResponse()


@router.get("/version", summary="Проверить версию приложения")
def get_version() -> VersionResponse:
    # safe fallback if package not installed
    try:
        ver = settings.APP_VERSION
    except Exception:
        ver = "unknown"
    return VersionResponse(version=ver)


@router.get("/metrics", summary="Получить метрики Prometheus", include_in_schema=False)
async def metrics(key: Annotated[str | None, Header()] = None) -> Response:
    """
    Protected exposition of Prometheus metrics.
    By default requires header 'X-Prometheus-Key' == settings.prometheus_metrics_key.
    In debug/local you can allow empty key by setting prometheus_metrics_key to empty string.
    """
    # header name from client is 'X-Prometheus-Key'
    expected = settings.PROMETHEUS_METRICS_KEY or ""
    if expected and key != expected:
        return Response(status_code=403)

    data = generate_latest(REGISTRY)
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
