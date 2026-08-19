"""
Test purchase availability when product is in stock.
"""

from web_status_watcher.purchase.detector import (
    PurchaseAvailabilityDetector,
)
from web_status_watcher.purchase.status import (
    PurchaseAvailabilityStatus,
)


HTML_IN_STOCK = """
<html>
    <div
        id="r_buy_intovar"
        data-id="1205"
    >
        <button
            type="submit"
            class="btn-primary buy"
        >
            Купити
        </button>
    </div>

    <p>
        На складі залишилося всього
        <span class="pd_qty">1</span>
        шт.
    </p>
</html>
"""


def main() -> None:
    detector = PurchaseAvailabilityDetector()

    status = detector.detect(
        HTML_IN_STOCK,
    )

    assert status == PurchaseAvailabilityStatus.AVAILABLE

    print(
        "PURCHASE AVAILABILITY STOCK AVAILABLE TEST PASSED"
    )
    print("pd_qty=1")
    print(f"status={status.value}")


if __name__ == "__main__":
    main()