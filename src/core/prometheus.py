import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from functools import cache

from fastapi import Request, Response
from prometheus_client import Counter, Gauge, Histogram
from starlette.middleware.base import BaseHTTPMiddleware

from core.config import settings


@dataclass
class Metrics:
    request_count: Counter
    request_latency: Histogram
    inprogress_requests: Gauge


@cache
def get_metrics() -> Metrics:
    prefix = settings.APP_NAME.replace("-", "_")
    # Use a didicated registry via default REGISTRY, okay for most setups.
    return Metrics(
        request_count=Counter(
            f"{prefix}_http_requests_total",
            "Total number of HTTP requests",
            ["method", "endpoint", "status_code"],
        ),
        request_latency=Histogram(
            f"{prefix}_http_request_duration_seconds",
            "HTTP request latency (seconds)",
            ["method", "endpoint", "status_code"],
            buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
        ),
        inprogress_requests=Gauge(
            f"{prefix}_inprogress_requests",
            "Number of in-progress requests",
            ["endpoint"],
        ),
    )


def _get_route_path(request: Request) -> str:
    """
    Return the route template path if available (e.g. "/api/users/{user_id}"),
    otherwise fallback to raw path (but avoid querystring).
    """
    route = request.scope.get("route")
    try:
        # Starlette/fastapi Route has .path attribute
        if hasattr(route, "path"):
            return route.path  # type: ignore
    except Exception:
        pass
    # Fallback: use the raw path but strip any high-cardinality parts carefully
    return request.url.path


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:

        # Do not collect for non-api or static endpoints (configurable)
        path = request.url.path
        if not path.startswith("/api"):
            return await call_next(request)

        metrics = get_metrics()
        endpoint = _get_route_path(request)

        # inprogress gauge
        metrics.inprogress_requests.labels(endpoint=endpoint).inc()
        start_time = time.time()

        try:
            response = await call_next(request)
        finally:
            # always decrement even on exceptions
            metrics.inprogress_requests.labels(endpoint=endpoint).dec()

        process_time = time.time() - start_time
        status = getattr(response, "status_code", 500)

        labels = {
            "method": request.method,
            "endpoint": endpoint,
            "status_code": str(status),
        }
        metrics.request_count.labels(**labels).inc()
        metrics.request_latency.labels(**labels).observe(process_time)

        return response
