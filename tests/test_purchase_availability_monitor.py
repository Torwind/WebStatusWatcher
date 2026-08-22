from web_status_watcher.purchase.availability import (
    AvailabilityResult,
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


# --------------------------------------------------
# 1. First status is AVAILABLE.
#    There is no previous state, so this is NOT
#    a NOT_AVAILABLE -> AVAILABLE transition.
# --------------------------------------------------

monitor = PurchaseAvailabilityMonitor()

result = monitor.update(
    make_result(
        PurchaseAvailabilityStatus.AVAILABLE,
    )
)

assert result is False


# --------------------------------------------------
# 2. AVAILABLE -> AVAILABLE
# --------------------------------------------------

result = monitor.update(
    make_result(
        PurchaseAvailabilityStatus.AVAILABLE,
    )
)

assert result is False


# --------------------------------------------------
# 3. AVAILABLE -> NOT_AVAILABLE
# --------------------------------------------------

result = monitor.update(
    make_result(
        PurchaseAvailabilityStatus.NOT_AVAILABLE,
    )
)

assert result is False


# --------------------------------------------------
# 4. NOT_AVAILABLE -> NOT_AVAILABLE
# --------------------------------------------------

result = monitor.update(
    make_result(
        PurchaseAvailabilityStatus.NOT_AVAILABLE,
    )
)

assert result is False


# --------------------------------------------------
# 5. NOT_AVAILABLE -> AVAILABLE
#    This is the transition we are looking for.
# --------------------------------------------------

result = monitor.update(
    make_result(
        PurchaseAvailabilityStatus.AVAILABLE,
    )
)

assert result is True


# --------------------------------------------------
# 6. AVAILABLE -> LIMIT_REACHED
# --------------------------------------------------

result = monitor.update(
    make_result(
        PurchaseAvailabilityStatus.LIMIT_REACHED,
    )
)

assert result is False


# --------------------------------------------------
# 7. LIMIT_REACHED -> AVAILABLE
#    Not a NOT_AVAILABLE -> AVAILABLE transition.
# --------------------------------------------------

result = monitor.update(
    make_result(
        PurchaseAvailabilityStatus.AVAILABLE,
    )
)

assert result is False


print()
print("PURCHASE AVAILABILITY MONITOR TEST PASSED")
print("INITIAL AVAILABLE -> False")
print("AVAILABLE -> AVAILABLE -> False")
print("AVAILABLE -> NOT_AVAILABLE -> False")
print("NOT_AVAILABLE -> NOT_AVAILABLE -> False")
print("NOT_AVAILABLE -> AVAILABLE -> True")
print("AVAILABLE -> LIMIT_REACHED -> False")
print("LIMIT_REACHED -> AVAILABLE -> False")