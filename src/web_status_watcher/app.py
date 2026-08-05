from __future__ import annotations

from .constants import CONFIG_DIR, DATA_DIR, LOG_DIR
from .config import ConfigManager
from .config.schema import validate
from .version import full_version
from .logging import get_logger


def create_directories() -> None:
    """
    Create required application directories.
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    create_directories()

    config = ConfigManager(CONFIG_DIR)

    validate(config.data)

    logger = get_logger()

    logger.info("Application started")
    logger.info("Configuration loaded successfully")

    print("=" * 60)
    print(full_version())
    print("=" * 60)

    print(f"Configuration : {CONFIG_DIR}")
    print(f"Database      : {DATA_DIR}")
    print(f"Logs          : {LOG_DIR}")
    print()

    print("Watcher interval :", config.get("watcher.interval"))
    print("Timeout         :", config.get("watcher.timeout"))
    print("Log level       :", config.get("logging.level"))
    print()

    logger.info("Initialization completed")
    print("Initialization completed successfully.")