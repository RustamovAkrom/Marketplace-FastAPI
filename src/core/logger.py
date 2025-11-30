import sys

from loguru import logger

from core.config import settings


def configure_logger() -> None:
    """Configure the Loguru logger based on settings."""

    logger.remove()  # Remove default logger

    log_level = settings.LOG_LEVEL.upper()
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    logger.add(
        sys.stdout,
        level=log_level,
        format=log_format,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )
