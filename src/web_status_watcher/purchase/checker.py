"""
HTTP checker for purchase product availability.
"""

from __future__ import annotations

from typing import Protocol

from web_status_watcher.purchase.availability import (
    AvailabilityResult,
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

    Availability is determined by:
    - HTTP 200 status;
    - presence of the active "Купити" button.
    """

    BUY_BUTTON_MARKER = (
        '<button type="submit" class="btn-primary buy">Купити</button>'
    )

    def __init__(
        self,
        http_client: HttpGetter,
    ) -> None:

        self._http_client = http_client

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

        if response.status_code != 200:

            return AvailabilityResult(
                available=False,
                products_id=product.products_id,
                cid=product.cid,
                status_code=response.status_code,
                message=(
                    f"HTTP status: {response.status_code}"
                ),
            )

        available = self.BUY_BUTTON_MARKER in response.text

        if available:

            message = "Product is available for purchase"

        else:

            message = "Product is not available for purchase"

        return AvailabilityResult(
            available=available,
            products_id=product.products_id,
            cid=product.cid,
            status_code=response.status_code,
            message=message,
        )