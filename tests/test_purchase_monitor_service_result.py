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
    def check(self, product) -> AvailabilityResult:
        return AvailabilityResult(
            available=False,
            products_id=product.products_id,
            cid=product.cid,
            status_code=200,
            status=PurchaseAvailabilityStatus.NOT_AVAILABLE,
            message="Test result",
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

service = PurchaseMonitorService(
    target=target,
    checker=FakeChecker(),
    monitor=PurchaseAvailabilityMonitor(),
)

assert service.last_result is None

event = service.tick()

assert event is False

assert service.last_result is not None
assert service.last_result.products_id == 1126
assert service.last_result.cid == 14348
assert service.last_result.status == (
    PurchaseAvailabilityStatus.NOT_AVAILABLE
)
assert service.last_result.status_code == 200
assert service.last_result.message == "Test result"


print()
print(
    "PURCHASE MONITOR SERVICE RESULT TEST PASSED"
)
print("status -> NOT_AVAILABLE")
print("products_id -> 1126")
print("cid -> 14348")
print("last_result -> stored")