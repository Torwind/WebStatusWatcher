from web_status_watcher.purchase.monitor import (
    PurchaseAvailabilityMonitor,
)
from web_status_watcher.purchase.target import (
    PurchaseTarget,
)


class FailingChecker:
    def check(self, product):
        raise AssertionError(
            "Checker must not be called for disabled target"
        )


target = PurchaseTarget(
    product_url=(
        "https://coins.bank.gov.ua/"
        "arhistratig-mihajil-c-/p-1126.html?cid=14348"
    ),
    products_id=1126,
    quantity=1,
    enabled=False,
)

monitor = PurchaseAvailabilityMonitor()

result = monitor.check(
    target,
    FailingChecker(),
)

assert result is False

print()
print(
    "PURCHASE AVAILABILITY MONITOR DISABLED TEST PASSED"
)
print("enabled=False -> checker not called")
print("result=False")