from functools import lru_cache

from core.config.auth import AuthConfig
from core.config.base import BaseAppConfig
from core.config.database import DatabaseConfig
from core.config.email import EmailConfig
from core.config.redis import RedisConfig
from core.config.social import SocialAuthConfig
from core.config.stripe import StripeConfig


class Settings(
    BaseAppConfig,
    AuthConfig,
    DatabaseConfig,
    StripeConfig,
    RedisConfig,
    EmailConfig,
    SocialAuthConfig,
):
    pass


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
