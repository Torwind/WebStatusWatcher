from web_status_watcher.purchase.availability import (
    AvailabilityResult,
)
from web_status_watcher.purchase.events import (
    PurchaseAvailableEvent,
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
    def __init__(self) -> None:
        self.calls = 0

    def check(
        self,
        product,
    ) -> AvailabilityResult:

        self.calls += 1

        status = (
            PurchaseAvailabilityStatus.NOT_AVAILABLE
            if self.calls == 1
            else PurchaseAvailabilityStatus.AVAILABLE
        )

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


checker = FakeChecker()

monitor = PurchaseAvailabilityMonitor()

service = PurchaseMonitorService(
    target=target,
    checker=checker,
    monitor=monitor,
)


event = service.check_event()

assert event is None


event = service.check_event()

assert isinstance(
    event,
    PurchaseAvailableEvent,
)

assert event.products_id == 1126
assert event.cid == 14348

assert checker.calls == 2


print()
print(
    "PURCHASE MONITOR SERVICE EVENT TEST PASSED"
)
print("tick 1 -> None")
print(
    "tick 2 -> PurchaseAvailableEvent"
)
print("products_id -> 1126")
print("cid -> 14348")