"""
HTML detector for purchase availability.
"""

from __future__ import annotations

from web_status_watcher.purchase.status import (
    PurchaseAvailabilityStatus,
)


class PurchaseAvailabilityDetector:
    """
    Detect purchase availability from product page HTML.

    The detector does not perform HTTP requests.
    It only analyses the HTML received from the server.
    """

    LIMIT_REACHED_TEXT = "Ви використали свій ліміт"

    BUY_CONTAINER = 'id="r_buy_intovar"'

    BUY_BUTTON_MARKER = 'class="btn-primary buy"'

    def detect(
        self,
        html: str,
    ) -> PurchaseAvailabilityStatus:
        """
        Detect purchase availability state.
        """

        if not html:
            return PurchaseAvailabilityStatus.NOT_AVAILABLE

        # The account has already reached the purchase limit.
        if self.LIMIT_REACHED_TEXT in html:
            return PurchaseAvailabilityStatus.LIMIT_REACHED

        # Active purchase block/button.
        if (
            self.BUY_CONTAINER in html
            and self.BUY_BUTTON_MARKER in html
        ):
            return PurchaseAvailabilityStatus.AVAILABLE

        # Product page exists, but there is no active
        # purchase control.
        return PurchaseAvailabilityStatus.NOT_AVAILABLE