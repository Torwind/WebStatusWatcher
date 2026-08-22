"""
Purchase availability state monitor.
"""

from __future__ import annotations

from web_status_watcher.purchase.availability import (
    AvailabilityResult,
)
from web_status_watcher.purchase.checker import (
    AvailabilityChecker,
)
from web_status_watcher.purchase.status import (
    PurchaseAvailabilityStatus,
)
from web_status_watcher.purchase.target import (
    PurchaseTarget,
)
from web_status_watcher.purchase.url_parser import (
    ProductUrlParser,
)


class PurchaseAvailabilityMonitor:
    """
    Monitor changes in product purchase availability.
    """

    def __init__(self) -> None:
        self._previous_status: (
            PurchaseAvailabilityStatus | None
        ) = None

    def update(
        self,
        result: AvailabilityResult,
    ) -> bool:
        """
        Update availability state.

        Returns True only when the product changes
        from NOT_AVAILABLE to AVAILABLE.
        """

        current_status = result.status

        became_available = (
            self._previous_status
            == PurchaseAvailabilityStatus.NOT_AVAILABLE
            and current_status
            == PurchaseAvailabilityStatus.AVAILABLE
        )

        self._previous_status = current_status

        return became_available

    def check(
        self,
        target: PurchaseTarget,
        checker: AvailabilityChecker,
    ) -> bool:
        """
        Check a purchase target and update monitor state.

        Returns True only when the target changes from
        NOT_AVAILABLE to AVAILABLE.

        Disabled targets are ignored and do not invoke
        the availability checker.
        """

        if not target.enabled:
            return False

        product = ProductUrlParser.parse(
            target.product_url,
        )

        if product.products_id != target.products_id:
            raise ValueError(
                "Product URL products_id does not match "
                "PurchaseTarget products_id"
            )

        result = checker.check(
            product,
        )

        return self.update(
            result,
        )