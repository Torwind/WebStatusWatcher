from web_status_watcher.purchase.availability import (
    AvailabilityResult,
)
from web_status_watcher.purchase.monitor import (
    PurchaseAvailabilityMonitor,
)
from web_status_watcher.purchase.status import (
    PurchaseAvailabilityStatus,
)
from web_status_watcher.purchase.target import (
    PurchaseTarget,
)


PRODUCT_URL = (
    "https://coins.bank.gov.ua/"
    "arhistratig-mihajil-c-/p-1126.html?cid=14348"
)


class MockChecker:
    def __init__(
        self,
        statuses,
    ) -> None:
        self._statuses = list(statuses)
        self._index = 0

    def check(
        self,
        product,
    ) -> AvailabilityResult:
        status = self._statuses[self._index]
        self._index += 1

        return AvailabilityResult(
            available=(
                status
                == PurchaseAvailabilityStatus.AVAILABLE
            ),
            products_id=product.products_id,
            cid=product.cid,
            status_code=200,
            status=status,
        )


target = PurchaseTarget(
    product_url=PRODUCT_URL,
    products_id=1126,
    quantity=1,
    enabled=True,
)


checker = MockChecker(
    [
        PurchaseAvailabilityStatus.NOT_AVAILABLE,
        PurchaseAvailabilityStatus.NOT_AVAILABLE,
        PurchaseAvailabilityStatus.AVAILABLE,
        PurchaseAvailabilityStatus.AVAILABLE,
    ]
)


monitor = PurchaseAvailabilityMonitor()


# First check: NOT_AVAILABLE.
result = monitor.check(
    target,
    checker,
)

assert result is False


# Second check: still NOT_AVAILABLE.
result = monitor.check(
    target,
    checker,
)

assert result is False


# Third check: product became available.
result = monitor.check(
    target,
    checker,
)

assert result is True


# Fourth check: still available.
result = monitor.check(
    target,
    checker,
)

assert result is False


print()
print(
    "PURCHASE AVAILABILITY MONITOR CHECKER TEST PASSED"
)
print(
    "NOT_AVAILABLE -> NOT_AVAILABLE -> False"
)
print(
    "NOT_AVAILABLE -> AVAILABLE -> True"
)
print(
    "AVAILABLE -> AVAILABLE -> False"
)