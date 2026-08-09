from pathlib import Path

from web_status_watcher.config.config_manager import ConfigManager
from web_status_watcher.purchase.factory import (
    PurchaseTargetFactory,
)


config = ConfigManager(
    Path("config")
)

target = PurchaseTargetFactory.create(
    config
)

assert target.enabled is False
assert target.product_url == ""
assert target.products_id == 0
assert target.quantity == 1


print()
print("PURCHASE FACTORY TEST PASSED")