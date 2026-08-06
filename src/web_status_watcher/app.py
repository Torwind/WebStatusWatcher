from __future__ import annotations

from .constants import (
    CONFIG_DIR,
    DATA_DIR,
    DATABASE_FILE,
    LOG_DIR,
)
from .config import ConfigManager
from .config.schema import validate
from .database import Database
from .database.repository import Repository
from .logging import get_logger
from .version import full_version


def create_directories() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:

    create_directories()

    logger = get_logger()

    logger.info("Application started")

    config = ConfigManager(CONFIG_DIR)

    validate(config.data)

    logger.info("Configuration loaded")

    database = Database(DATABASE_FILE)

    repository = Repository(database)

    logger.info("Database initialized")

    if len(repository.get_sites()) == 0:

        repository.add_site(
            "Example",
            "https://example.com",
        )

        logger.info("Default site created")

    print("=" * 60)
    print(full_version())
    print("=" * 60)

    print(f"Configuration : {CONFIG_DIR}")
    print(f"Database      : {DATABASE_FILE}")
    print(f"Logs          : {LOG_DIR}")
    print()

    print("Registered sites:")

    for site in repository.get_sites():
        print(
            f"  [{site['id']}] "
            f"{site['name']} -> {site['url']}"
        )

    print()

    logger.info("Initialization completed")

    database.close()