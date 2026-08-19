"""
Integration test for purchase availability detection.

Checks:
    1. Product in stock      -> AVAILABLE
    2. Product out of stock  -> NOT_AVAILABLE
    3. Purchase limit reached -> LIMIT_REACHED
"""

from web_status_watcher.purchase.detector import (
    PurchaseAvailabilityDetector,
)
from web_status_watcher.purchase.status import (
    PurchaseAvailabilityStatus,
)


HTML_AVAILABLE = """
<html>
    <div id="r_buy_intovar" data-id="1205">
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


HTML_NOT_AVAILABLE = """
<html>
    <div id="r_buy_intovar" data-id="1205">
    </div>

    <p>
        На складі залишилося всього
        <span class="pd_qty">0</span>
        шт.
    </p>
</html>
"""


HTML_LIMIT_REACHED = """
<html>
    <div id="r_buy_intovar" data-id="1205">
    </div>

    <p>
        Ви використали свій ліміт
    </p>

    <p>
        Ліміт продукції на одного користувача
        становить 1 шт.
    </p>
</html>
"""


def main() -> None:
    detector = PurchaseAvailabilityDetector()

    status_available = detector.detect(
        HTML_AVAILABLE,
    )

    status_not_available = detector.detect(
        HTML_NOT_AVAILABLE,
    )

    status_limit_reached = detector.detect(
        HTML_LIMIT_REACHED,
    )

    assert (
        status_available
        == PurchaseAvailabilityStatus.AVAILABLE
    )

    assert (
        status_not_available
        == PurchaseAvailabilityStatus.NOT_AVAILABLE
    )

    assert (
        status_limit_reached
        == PurchaseAvailabilityStatus.LIMIT_REACHED
    )

    print(
        "PURCHASE AVAILABILITY DETECTOR "
        "INTEGRATION TEST PASSED"
    )

    print(
        "AVAILABLE      -> "
        f"{status_available.value}"
    )

    print(
        "NOT_AVAILABLE  -> "
        f"{status_not_available.value}"
    )

    print(
        "LIMIT_REACHED  -> "
        f"{status_limit_reached.value}"
    )


if __name__ == "__main__":
    main()