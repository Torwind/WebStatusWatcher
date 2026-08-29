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
from .logging import get_logger
from .purchase.factory import PurchaseTargetFactory
from .purchase.worker_factory import PurchaseWorkerFactory
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
    # Purchase availability check.
    # --------------------------------------------------

    target = PurchaseTargetFactory.create(
        config,
    )

    if target.enabled:

        logger.info(
            "Purchase monitoring enabled"
        )

        service = (
            PurchaseWorkerFactory.create_service(
                config,
            )
        )

        if service is None:

            logger.error(
                "Purchase monitor service was not created"
            )

        else:

            logger.info(
                "Running purchase availability check"
            )

            try:

                event = service.tick()

                result = service.last_result

                if result is None:

                    logger.warning(
                        "Purchase check returned no result"
                    )

                else:

                    logger.info(
                        "Purchase status: %s",
                        result.status.value,
                    )

                    logger.info(
                        "Purchase product: "
                        "products_id=%d cid=%d",
                        result.products_id,
                        result.cid,
                    )

                    logger.info(
                        "Purchase HTTP status: %d",
                        result.status_code,
                    )

                    if result.message:

                        logger.info(
                            "Purchase message: %s",
                            result.message,
                        )

                    if event:

                        logger.info(
                            "PURCHASE AVAILABLE: "
                            "NOT_AVAILABLE -> AVAILABLE"
                        )

                    else:

                        logger.info(
                            "No purchase availability transition"
                        )

            except Exception as exc:

                logger.exception(
                    "Purchase availability check failed: %s",
                    exc,
                )

    else:

        logger.info(
            "Purchase monitoring disabled"
        )

    logger.info(
        "Initialization completed"
    )

    database.close()


if __name__ == "__main__":
    main()