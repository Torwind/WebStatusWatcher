"""
Purchase monitoring service.
"""

from __future__ import annotations

from web_status_watcher.purchase.availability import (
    AvailabilityResult,
)
from web_status_watcher.purchase.checker import (
    AvailabilityChecker,
)
from web_status_watcher.purchase.monitor import (
    PurchaseAvailabilityMonitor,
)
from web_status_watcher.purchase.target import (
    PurchaseTarget,
)


class PurchaseMonitorService:
    """
    Service that checks one purchase target.
    """

    def __init__(
        self,
        target: PurchaseTarget,
        checker: AvailabilityChecker,
        monitor: PurchaseAvailabilityMonitor,
    ) -> None:
        self._target = target
        self._checker = checker
        self._monitor = monitor
        self._last_result: (
            AvailabilityResult | None
        ) = None

    @property
    def last_result(
        self,
    ) -> AvailabilityResult | None:
        """
        Return the last availability result.
        """

        return self._last_result

    def tick(self) -> bool:
        """
        Check purchase availability.

        Returns True only on a
        NOT_AVAILABLE -> AVAILABLE transition.
        """

        result = self._monitor.check_result(
            self._target,
            self._checker,
        )

        if result is None:
            self._last_result = None
            return False

        self._last_result = result

        return self._monitor.update(
            result,
        )