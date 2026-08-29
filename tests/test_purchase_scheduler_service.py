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
from web_status_watcher.scheduler.scheduler import (
    Scheduler,
)
from web_status_watcher.scheduler.worker import (
    Worker,
)
from web_status_watcher.services.purchase_monitor_service import (
    PurchaseMonitorService,
)


class FakeChecker:
    def __init__(self) -> None:
        self.calls = 0

    def check(self, product) -> AvailabilityResult:
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

purchase_service = PurchaseMonitorService(
    target=target,
    checker=checker,
    monitor=monitor,
)


events = []


def purchase_tick() -> None:
    events.append(
        purchase_service.tick()
    )


scheduler = Scheduler()

scheduler.add_worker(
    Worker(
        name="purchase",
        interval=1,
        callback=purchase_tick,
    )
)


worker = scheduler._workers[0]

worker.tick()
worker.tick()


assert checker.calls == 2

assert events == [
    False,
    True,
]


print()
print(
    "PURCHASE SCHEDULER SERVICE TEST PASSED"
)
print("tick 1 -> False")
print("tick 2 -> True")
print("checker calls -> 2")