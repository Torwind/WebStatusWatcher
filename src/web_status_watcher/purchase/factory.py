"""
Purchase target factory.
"""

from __future__ import annotations

from typing import Any

from web_status_watcher.config.config_manager import ConfigManager
from web_status_watcher.purchase.target import PurchaseTarget


class PurchaseTargetFactory:
    """
    Creates PurchaseTarget from application configuration.
    """

    @staticmethod
    def create(
        config: ConfigManager,
    ) -> PurchaseTarget:
        """
        Build purchase target from configuration.
        """

        enabled = bool(
            config.get(
                "purchase.enabled",
                False,
            )
        )

        product_url = str(
            config.get(
                "purchase.product_url",
                "",
            )
        )

        products_id = int(
            config.get(
                "purchase.products_id",
                0,
            )
        )

        quantity = int(
            config.get(
                "purchase.quantity",
                1,
            )
        )

        return PurchaseTarget(
            product_url=product_url,
            products_id=products_id,
            quantity=quantity,
            enabled=enabled,
        )