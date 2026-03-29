"""Logging configuration for the data pipeline."""

import logging


def configure_logging() -> None:
    """Configure application-wide logging settings."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
