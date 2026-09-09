from web_status_watcher.purchase.availability import (
    AvailabilityResult,
)
from web_status_watcher.purchase.status import (
    PurchaseAvailabilityStatus,
)


result = AvailabilityResult(
    available=True,
    products_id=1126,
    cid=14348,
    status_code=200,
    status=PurchaseAvailabilityStatus.AVAILABLE,
    message="Product is available",
)


assert result.available is True
assert result.products_id == 1126
assert result.cid == 14348
assert result.status == (
    PurchaseAvailabilityStatus.AVAILABLE
)
assert result.message == (
    "Product is available"
)


print()
print(
    "AVAILABILITY RESULT TEST PASSED"
)
print(
    f"products_id={result.products_id}, "
    f"cid={result.cid}, "
    f"available={result.available}, "
    f"status={result.status.value}"
)