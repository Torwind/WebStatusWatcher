from pathlib import Path

from web_status_watcher.config.config_manager import ConfigManager


config = ConfigManager(
    Path("config")
)

assert config.get(
    "purchase.enabled"
) is False

assert config.get(
    "purchase.product_url"
) == ""

assert config.get(
    "purchase.products_id"
) == 0

assert config.get(
    "purchase.quantity"
) == 1


print()
print("PURCHASE CONFIG TEST PASSED")