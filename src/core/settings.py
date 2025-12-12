from functools import lru_cache

from core.config.auth import AuthConfig
from core.config.base import BaseAppConfig
from core.config.broker import BrokerConfig
from core.config.database import DatabaseConfig
from core.config.email import EmailConfig
from core.config.social import SocialAuthConfig
from core.config.stripe import StripeConfig


class Settings(
    BaseAppConfig,
    AuthConfig,
    DatabaseConfig,
    StripeConfig,
    BrokerConfig,
    EmailConfig,
    SocialAuthConfig,
):
    pass


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
