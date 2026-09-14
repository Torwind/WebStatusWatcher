from __future__ import annotations

import time

from .constants import (
    CONFIG_DIR,
    DATA_DIR,
    DATABASE_FILE,
    LOG_DIR,
)
from .config import ConfigManager
from .config.schema import validate
from .database import Database
from .logging import get_logger
from .purchase.factory import PurchaseTargetFactory
from .purchase.worker_factory import PurchaseWorkerFactory
from .scheduler import Scheduler
from .version import full_version


def create_directories() -> None:
    CONFIG_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    LOG_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def main() -> None:
    create_directories()

    logger = get_logger()

    logger.info(
        "Application started"
    )

    config = ConfigManager(
        CONFIG_DIR,
    )

    validate(
        config.data,
    )

    logger.info(
        "Configuration loaded"
    )

    database = Database(
        DATABASE_FILE,
    )

    database.connect()

    logger.info(
        "Database initialized"
    )

    assert database.sites is not None

    if len(
        database.sites.get_all()
    ) == 0:

        database.execute(
            """
            INSERT INTO sites
            (
                name,
                url,
                interval_seconds
            )
            VALUES
            (
                ?,
                ?,
                ?
            )
            """,
            (
                "Example",
                "https://example.com",
                30,
            ),
        )

        logger.info(
            "Default site created"
        )

    print("=" * 60)
    print(full_version())
    print("=" * 60)

    print(
        f"Configuration : {CONFIG_DIR}"
    )

    print(
        f"Database      : {DATABASE_FILE}"
    )

    print(
        f"Logs          : {LOG_DIR}"
    )

    print()

    print("Registered sites:")

    for site in database.sites.get_all():
        print(
            f"  [{site['id']}] "
            f"{site['name']} -> {site['url']}"
        )

    print()

    # --------------------------------------------------
    # Purchase monitoring.
    # --------------------------------------------------

    target = PurchaseTargetFactory.create(
        config,
    )

    if not target.enabled:

        logger.info(
            "Purchase monitoring disabled"
        )

    else:

        logger.info(
            "Purchase monitoring enabled"
        )

        worker = PurchaseWorkerFactory.create(
            config,
        )

        if worker is None:

            logger.error(
                "Purchase worker was not created"
            )

        else:

            scheduler = Scheduler()

            scheduler.add_worker(
                worker,
            )

            logger.info(
                "Purchase worker registered"
            )

            logger.info(
                "Starting purchase scheduler"
            )

            scheduler.start()

            logger.info(
                "Purchase scheduler started"
            )

            try:

                while worker.running:

                    time.sleep(
                        0.5
                    )

            except KeyboardInterrupt:

                logger.info(
                    "Purchase monitoring interrupted"
                )

            finally:

                scheduler.stop()

                logger.info(
                    "Purchase scheduler stopped"
                )

    logger.info(
        "Initialization completed"
    )

    database.close()


if __name__ == "__main__":
    main()
