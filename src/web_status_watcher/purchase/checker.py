"""
HTTP checker for purchase product availability.
"""

from __future__ import annotations

from typing import Protocol

from web_status_watcher.purchase.availability import (
    AvailabilityResult,
)
from web_status_watcher.purchase.detector import (
    PurchaseAvailabilityDetector,
)
from web_status_watcher.purchase.status import (
    PurchaseAvailabilityStatus,
)
from web_status_watcher.purchase.url_parser import (
    ProductUrl,
)


class HttpResponse(Protocol):
    """
    Minimal HTTP response interface required by the checker.
    """

    status_code: int
    text: str


class HttpGetter(Protocol):
    """
    Minimal HTTP client interface required by the checker.
    """

    def get(self, url: str) -> HttpResponse:
        ...


class AvailabilityChecker:
    """
    Check whether a purchase product page is available.
    """

    def __init__(
        self,
        http_client: HttpGetter,
    ) -> None:

        self._http_client = http_client
        self._detector = PurchaseAvailabilityDetector()

    def check(
        self,
        product: ProductUrl,
    ) -> AvailabilityResult:
        """
        Check product page availability.
        """

        response = self._http_client.get(
            product.url,
        )

        # HTTP error: the product page itself could not
        # be obtained successfully.
        if response.status_code != 200:

            status = (
                PurchaseAvailabilityStatus.NOT_AVAILABLE
            )

            return AvailabilityResult(
                available=False,
                products_id=product.products_id,
                cid=product.cid,
                status_code=response.status_code,
                status=status,
                message=(
                    f"HTTP status: "
                    f"{response.status_code}"
                ),
            )

        # Analyse the actual HTML returned by the server.
        status = self._detector.detect(
            response.text,
        )

        return AvailabilityResult(
            available=(
                status
                == PurchaseAvailabilityStatus.AVAILABLE
            ),
            products_id=product.products_id,
            cid=product.cid,
            status_code=response.status_code,
            status=status,
            message=self._message_for(status),
        )

    @staticmethod
    def _message_for(
        status: PurchaseAvailabilityStatus,
    ) -> str:

        if (
            status
            == PurchaseAvailabilityStatus.AVAILABLE
        ):
            return "Product is available for purchase"

        if (
            status
            == PurchaseAvailabilityStatus.LIMIT_REACHED
        ):
            return "Purchase limit has been reached"

        return "Product is not available for purchase"