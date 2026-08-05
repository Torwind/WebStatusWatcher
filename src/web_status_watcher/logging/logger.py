from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from ..constants import LOG_DIR, LOG_FILE


_logger: logging.Logger | None = None


def get_logger() -> logging.Logger:
    """
    Return singleton application logger.
    """

    global _logger

    if _logger is not None:
        return _logger

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("WebStatusWatcher")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        _logger = logger
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=1_000_000,
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    _logger = logger

    return logger