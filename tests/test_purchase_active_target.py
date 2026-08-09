from pathlib import Path

from web_status_watcher.config.config_manager import ConfigManager
from web_status_watcher.purchase.factory import (
    PurchaseTargetFactory,
)


config = ConfigManager(
    Path("config")
)

config.set(
    "purchase.enabled",
    True,
    autosave=False,
)

config.set(
    "purchase.product_url",
    "https://coins.bank.gov.ua/",
    autosave=False,
)

config.set(
    "purchase.products_id",
    1126,
    autosave=False,
)

config.set(
    "purchase.quantity",
    1,
    autosave=False,
)

target = PurchaseTargetFactory.create(
    config
)

assert target.enabled is True
assert target.products_id == 1126
assert target.quantity == 1
assert target.product_url == (
    "https://coins.bank.gov.ua/"
)

print()
print("ACTIVE PURCHASE TARGET TEST PASSED")
print(
    f"products_id={target.products_id}, "
    f"quantity={target.quantity}, "
    f"enabled={target.enabled}"
)