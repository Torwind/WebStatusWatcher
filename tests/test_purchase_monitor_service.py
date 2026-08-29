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
from web_status_watcher.services.purchase_monitor_service import (
    PurchaseMonitorService,
)


class FakeChecker:
    def __init__(
        self,
        statuses,
    ) -> None:
        self._statuses = list(statuses)
        self._index = 0
        self.calls = 0

    def check(
        self,
        product,
    ) -> AvailabilityResult:
        self.calls += 1

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
    product_url=(
        "https://coins.bank.gov.ua/"
        "arhistratig-mihajil-c-/p-1126.html?cid=14348"
    ),
    products_id=1126,
    quantity=1,
    enabled=True,
)


checker = FakeChecker(
    [
        PurchaseAvailabilityStatus.NOT_AVAILABLE,
        PurchaseAvailabilityStatus.AVAILABLE,
    ]
)

monitor = PurchaseAvailabilityMonitor()

service = PurchaseMonitorService(
    target=target,
    checker=checker,
    monitor=monitor,
)


result = service.tick()

assert result is False
assert checker.calls == 1


result = service.tick()

assert result is True
assert checker.calls == 2


print()
print("PURCHASE MONITOR SERVICE TEST PASSED")
print("tick 1 -> False")
print("tick 2 -> True")
print("checker calls -> 2")