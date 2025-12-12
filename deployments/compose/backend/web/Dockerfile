# syntax=docker/dockerfile:1.2

ARG PYTHON_VERSION=3.12
ARG UV_VERSION=0.7.2

FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv

FROM python:${PYTHON_VERSION}-slim AS builder
COPY --from=uv /uv /uvx /bin/

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --no-dev --frozen --no-install-project --all-groups

FROM python:${PYTHON_VERSION}-slim AS app

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

COPY --from=builder /opt/venv /opt/venv

COPY deployments/compose/backend/web/entrypoint /entrypoint
COPY deployments/compose/backend/web/start /start
RUN chmod +x /entrypoint /start

COPY deployments/compose/backend/celery/worker/start /start-celeryworker
COPY deployments/compose/backend/celery/beat/start /start-celerybeat
COPY deployments/compose/backend/celery/flower/start /start-flower

RUN chmod +x /start-celeryworker /start-celerybeat /start-flower

COPY src/ ./

RUN chgrp -R 0 /app && chmod -R g=u /app

ENTRYPOINT ["/entrypoint"]
