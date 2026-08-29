from pathlib import Path

from web_status_watcher.config.config_manager import ConfigManager
from web_status_watcher.purchase.factory import (
    PurchaseTargetFactory,
)
from web_status_watcher.purchase.monitor import (
    PurchaseAvailabilityMonitor,
)
from web_status_watcher.services.purchase_monitor_service import (
    PurchaseMonitorService,
)


class FailingChecker:
    def check(self, product):
        raise AssertionError(
            "Checker must not be called when "
            "purchase.enabled is False"
        )


config = ConfigManager(
    Path("config"),
)

target = PurchaseTargetFactory.create(
    config,
)

assert target.enabled is False
assert target.product_url == ""
assert target.products_id == 0
assert target.quantity == 1


monitor = PurchaseAvailabilityMonitor()

service = PurchaseMonitorService(
    target=target,
    checker=FailingChecker(),
    monitor=monitor,
)

result = service.tick()

assert result is False


print()
print(
    "PURCHASE MONITOR SERVICE CONFIG TEST PASSED"
)
print("purchase.enabled -> False")
print("checker -> not called")
print("tick -> False")