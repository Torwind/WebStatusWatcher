"""
Purchase worker factory.
"""

from __future__ import annotations

import time

from web_status_watcher.config.config_manager import (
    ConfigManager,
)
from web_status_watcher.purchase.cart_client import (
    PurchaseCartClient,
)
from web_status_watcher.purchase.factory import (
    PurchaseTargetFactory,
)
from web_status_watcher.scheduler.worker import (
    Worker,
)


class PurchaseWorkerFactory:
    """
    Creates components for purchase monitoring.
    """

    MAX_IMMEDIATE_RETRIES = 3

    @staticmethod
    def create(
        config: ConfigManager,
    ) -> Worker | None:
        """
        Create purchase worker from configuration.

        The Playwright client is created lazily inside the
        scheduler thread and remains attached to that thread
        for the lifetime of the worker.

        Normal availability checks are controlled by the
        worker interval. Technical probe errors are retried
        immediately up to MAX_IMMEDIATE_RETRIES times.

        When all immediate retries are exhausted, the current
        browser client is closed and discarded so that the next
        normal tick can create a fresh browser connection.
        """

        target = PurchaseTargetFactory.create(
            config,
        )

        if not target.enabled:
            return None

        interval = float(
            config.get(
                "purchase.interval",
                1.25,
            )
        )

        browser_client: (
            PurchaseCartClient | None
        ) = None

        last_availability: bool | None = None

        worker_holder: dict[str, Worker] = {}

        def log_availability(
            available: bool,
            elapsed_ms: float,
        ) -> None:
            nonlocal last_availability

            if available == last_availability:
                return

            last_availability = available

            if available:
                print(
                    "Purchase availability changed: "
                    "AVAILABLE "
                    f"probe={elapsed_ms:.0f}ms"
                )
                return

            print(
                "Purchase availability changed: "
                "NOT_AVAILABLE "
                f"next_probe={interval:.2f}s "
                f"probe={elapsed_ms:.0f}ms"
            )

        def callback() -> None:
            nonlocal browser_client
            nonlocal last_availability

            if browser_client is None:

                browser_client = (
                    PurchaseCartClient.connect()
                )

                last_availability = None

                print(
                    "Purchase browser client connected"
                )

            retry_count = 0

            while True:

                started = time.monotonic()

                try:

                    available = (
                        browser_client.is_available(
                            target,
                        )
                    )

                    elapsed_ms = (
                        time.monotonic()
                        - started
                    ) * 1000

                    log_availability(
                        available,
                        elapsed_ms,
                    )

                    break

                except Exception as exc:

                    elapsed_ms = (
                        time.monotonic()
                        - started
                    ) * 1000

                    retry_count += 1

                    print(
                        "Purchase availability probe failed: "
                        f"{exc}"
                    )

                    print(
                        "Probe elapsed="
                        f"{elapsed_ms:.0f}ms"
                    )

                    if (
                        retry_count
                        > PurchaseWorkerFactory.MAX_IMMEDIATE_RETRIES
                    ):
                        print(
                            "Purchase availability probe retries "
                            "exhausted"
                        )

                        try:
                            browser_client.close()
                        finally:
                            browser_client = None
                            last_availability = None

                        print(
                            "Purchase browser client reset"
                        )

                        return

                    print(
                        "Immediate purchase availability retry "
                        f"{retry_count}/"
                        f"{PurchaseWorkerFactory.MAX_IMMEDIATE_RETRIES}"
                    )

            if not available:
                return

            print(
                "Purchase action: ADD_TO_CART"
            )

            try:

                item = browser_client.add_to_cart(
                    target,
                )

                print(
                    "Purchase added to cart: "
                    f"products_id={item.products_id}, "
                    f"quantity={item.quantity}"
                )

            except Exception:

                try:
                    browser_client.close()
                finally:
                    browser_client = None
                    last_availability = None

                print(
                    "Purchase browser client reset "
                    "after purchase error"
                )

                raise

            else:

                try:
                    browser_client.close()
                finally:
                    browser_client = None
                    last_availability = None

            worker_holder["worker"].stop()

        worker = Worker(
            name="purchase",
            interval=interval,
            callback=callback,
        )

        worker_holder["worker"] = worker

        return worker
