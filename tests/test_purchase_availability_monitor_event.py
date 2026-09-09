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


def make_result(
    status: PurchaseAvailabilityStatus,
) -> AvailabilityResult:
    return AvailabilityResult(
        available=(
            status
            == PurchaseAvailabilityStatus.AVAILABLE
        ),
        products_id=1126,
        cid=14348,
        status_code=200,
        status=status,
    )


monitor = PurchaseAvailabilityMonitor()


# Initial NOT_AVAILABLE.
event = monitor.update_event(
    make_result(
        PurchaseAvailabilityStatus.NOT_AVAILABLE,
    )
)

assert event is None


# Still NOT_AVAILABLE.
event = monitor.update_event(
    make_result(
        PurchaseAvailabilityStatus.NOT_AVAILABLE,
    )
)

assert event is None


# NOT_AVAILABLE -> AVAILABLE.
event = monitor.update_event(
    make_result(
        PurchaseAvailabilityStatus.AVAILABLE,
    )
)

assert isinstance(
    event,
    PurchaseAvailableEvent,
)

assert event.products_id == 1126
assert event.cid == 14348


# AVAILABLE -> AVAILABLE.
event = monitor.update_event(
    make_result(
        PurchaseAvailabilityStatus.AVAILABLE,
    )
)

assert event is None


print()
print(
    "PURCHASE AVAILABILITY MONITOR EVENT TEST PASSED"
)
print("NOT_AVAILABLE -> NOT_AVAILABLE -> None")
print(
    "NOT_AVAILABLE -> AVAILABLE -> PurchaseAvailableEvent"
)
print("AVAILABLE -> AVAILABLE -> None")