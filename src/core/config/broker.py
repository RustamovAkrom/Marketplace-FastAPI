from pydantic_settings import BaseSettings


class BrokerConfig(BaseSettings):
    BROKER: str = "rabbitmq"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    RABBITMQ_USER: str | None = None
    RABBITMQ_PASSWORD: str | None = None
    RABBITMQ_HOST: str | None = None
    RABBITMQ_PORT: int | None = None
    RABBITMQ_VHOST: str = "/"

    @property
    def CELERY_BROKER_URL(self):
        if self.BROKER == "redis":
            return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

        return (
            f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}"
            f"@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/{self.RABBITMQ_VHOST}"
        )

    @property
    def CELERY_RESULT_BACKEND(self):
        return self.CELERY_BROKER_URL
