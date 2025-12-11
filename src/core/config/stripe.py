from pydantic_settings import BaseSettings


class StripeConfig(BaseSettings):
    STRIPE_SECRET_KEY: str = "secret"
    STRIPE_WEBHOOK_SECRET: str = "secret_webhook"
    STRIPE_API_VERSION: str = "2024-11-08"
    STRIPE_SUCCESS_URL: str = "https://yourapp.com/success"
    STRIPE_CANCEL_URL: str = "https://yourapp.com/cancel"
