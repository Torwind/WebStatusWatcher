"""
Purchase worker factory.
"""

from __future__ import annotations

from web_status_watcher.config.config_manager import ConfigManager
from web_status_watcher.network import HttpClient
from web_status_watcher.purchase.cart_client import (
    PurchaseCartClient,
)
from web_status_watcher.purchase.checker import (
    AvailabilityChecker,
)
from web_status_watcher.purchase.factory import (
    PurchaseTargetFactory,
)
from web_status_watcher.purchase.monitor import (
    PurchaseAvailabilityMonitor,
)
from web_status_watcher.scheduler.worker import (
    Worker,
)
from web_status_watcher.services.purchase_monitor_service import (
    PurchaseMonitorService,
)


class PurchaseWorkerFactory:
    """
    Creates components for purchase monitoring.
    """

    @staticmethod
    def create_service(
        config: ConfigManager,
    ) -> PurchaseMonitorService | None:
        """
        Create purchase monitoring service.

        Returns None when purchase monitoring is disabled.
        """

        target = PurchaseTargetFactory.create(
            config,
        )

        if not target.enabled:
            return None

        client = HttpClient()

        checker = AvailabilityChecker(
            client,
        )

        monitor = PurchaseAvailabilityMonitor()

        return PurchaseMonitorService(
            target=target,
            checker=checker,
            monitor=monitor,
        )

    @staticmethod
    def create(
        config: ConfigManager,
    ) -> Worker | None:
        """
        Create purchase worker from configuration.

        The worker monitors availability and, when the target
        becomes available, adds it to the authenticated Chrome
        cart and stops itself after successful confirmation.
        """

        service = PurchaseWorkerFactory.create_service(
            config,
        )

        if service is None:
            return None

        worker_holder: dict[str, Worker] = {}

        def callback() -> None:
            event = service.check_event()

            if event is None:
                return

            cart_client = PurchaseCartClient.connect()

            try:
                item = cart_client.add_to_cart(
                    service.target,
                )
            finally:
                cart_client.close()

            print(
                "Purchase added to cart: "
                f"products_id={item.products_id}, "
                f"quantity={item.quantity}"
            )

            worker_holder["worker"].stop()

        worker = Worker(
            name="purchase",
            interval=1,
            callback=callback,
        )

        worker_holder["worker"] = worker

        return worker