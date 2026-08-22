from web_status_watcher.purchase.monitor import (
    PurchaseAvailabilityMonitor,
)
from web_status_watcher.purchase.target import (
    PurchaseTarget,
)


class FailingChecker:
    def check(self, product):
        raise AssertionError(
            "Checker must not be called when product IDs do not match"
        )


target = PurchaseTarget(
    product_url=(
        "https://coins.bank.gov.ua/"
        "30-rokiv-konstituciji-ukrajini-c-/p-1205.html"
        "?cid=14348"
    ),
    products_id=1126,
    quantity=1,
    enabled=True,
)

monitor = PurchaseAvailabilityMonitor()

try:
    monitor.check(
        target,
        FailingChecker(),
    )

    raise AssertionError(
        "products_id mismatch should raise ValueError"
    )

except ValueError as exc:
    assert (
        str(exc)
        == (
            "Product URL products_id does not match "
            "PurchaseTarget products_id"
        )
    )


print()
print(
    "PURCHASE AVAILABILITY MONITOR "
    "TARGET MISMATCH TEST PASSED"
)
print("target.products_id=1126")
print("url.products_id=1205")
print("ValueError raised correctly")