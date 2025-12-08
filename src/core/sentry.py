# src/core/sentry.py
import logging

from sentry_sdk import init as sentry_init
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from core.config import settings

logger = logging.getLogger(__name__)


def init_sentry() -> None:
    dsn = settings.SENTRY_DSN
    if not dsn:
        logger.info("Sentry DSN not provided — skipping Sentry init")
        return

    sentry_init(
        dsn=dsn,
        environment=settings.ENV,
        integrations=[
            FastApiIntegration(),
            SqlalchemyIntegration(),
            RedisIntegration(),
        ],
        traces_sample_rate=0.1 if settings.ENV == "prod" else 0.5,
        profiles_sample_rate=0.0 if settings.ENV == "dev" else 0.01,
        send_default_pii=False,  # avoid leaking user PII by default
        debug=False,
    )
    logger.info("Sentry initialized")
