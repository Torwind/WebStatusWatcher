"""
Purchase worker factory.
"""

from __future__ import annotations

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

    @staticmethod
    def create(
        config: ConfigManager,
    ) -> Worker | None:
        """
        Create purchase worker from configuration.

        The Playwright client is created lazily inside the
        scheduler thread and remains attached to that thread
        for the lifetime of the worker.
        """

        target = PurchaseTargetFactory.create(
            config,
        )

        if not target.enabled:
            return None

        browser_client: (
            PurchaseCartClient | None
        ) = None

        worker_holder: dict[str, Worker] = {}

        def callback() -> None:
            nonlocal browser_client

            if browser_client is None:

                browser_client = (
                    PurchaseCartClient.connect()
                )

            if not browser_client.is_available(
                target,
            ):
                return

            try:

                item = browser_client.add_to_cart(
                    target,
                )

                print(
                    "Purchase added to cart: "
                    f"products_id={item.products_id}, "
                    f"quantity={item.quantity}"
                )

            finally:

                browser_client.close()
                browser_client = None

            worker_holder["worker"].stop()

        worker = Worker(
            name="purchase",
            interval=1,
            callback=callback,
        )

        worker_holder["worker"] = worker

        return worker