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
from web_status_watcher.purchase.events import (
    PurchaseAvailableEvent,
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

        return (
            self.update_event(result)
            is not None
        )

    def update_event(
        self,
        result: AvailabilityResult,
    ) -> PurchaseAvailableEvent | None:
        """
        Update availability state.

        Returns a PurchaseAvailableEvent only when the
        product changes from NOT_AVAILABLE to AVAILABLE.
        """

        current_status = result.status

        became_available = (
            self._previous_status
            == PurchaseAvailabilityStatus.NOT_AVAILABLE
            and current_status
            == PurchaseAvailabilityStatus.AVAILABLE
        )

        self._previous_status = current_status

        if not became_available:
            return None

        return PurchaseAvailableEvent(
            products_id=result.products_id,
            cid=result.cid,
        )

    def check(
        self,
        target: PurchaseTarget,
        checker: AvailabilityChecker,
    ) -> bool:
        """
        Check a purchase target and update monitor state.

        Returns True only when the target changes from
        NOT_AVAILABLE to AVAILABLE.

        Disabled targets are ignored.
        """

        if not target.enabled:
            return False

        result = self.check_result(
            target,
            checker,
        )

        return self.update(
            result,
        )

    def check_event(
        self,
        target: PurchaseTarget,
        checker: AvailabilityChecker,
    ) -> PurchaseAvailableEvent | None:
        """
        Check a purchase target and return an availability
        event when the target becomes available.

        Returns None when there is no transition or the
        target is disabled.
        """

        if not target.enabled:
            return None

        result = self.check_result(
            target,
            checker,
        )

        return self.update_event(
            result,
        )

    def check_result(
        self,
        target: PurchaseTarget,
        checker: AvailabilityChecker,
    ) -> AvailabilityResult | None:
        """
        Check a purchase target and return the result.

        Returns None when the target is disabled.
        """

        if not target.enabled:
            return None

        product = ProductUrlParser.parse(
            target.product_url,
        )

        if product.products_id != target.products_id:
            raise ValueError(
                "Product URL products_id does not match "
                "PurchaseTarget products_id"
            )

        return checker.check(
            product,
        )