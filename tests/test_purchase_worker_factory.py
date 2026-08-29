from pathlib import Path

import yaml

from web_status_watcher.config.config_manager import (
    ConfigManager,
)
from web_status_watcher.purchase.worker_factory import (
    PurchaseWorkerFactory,
)


TEST_CONFIG_DIR = Path(
    "data/test_purchase_worker_factory_disabled"
)

TEST_CONFIG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


CONFIG_DATA = {
    "application": {
        "name": "WebStatusWatcher",
        "version": "0.4.12",
    },
    "watcher": {
        "interval": 30,
        "timeout": 15,
        "user_agent": "WebStatusWatcher/1.0",
    },
    "database": {
        "filename": "webstatuswatcher.db",
    },
    "logging": {
        "level": "INFO",
        "filename": "application.log",
    },
    "notifications": {
        "sound": True,
        "telegram": False,
    },
    "ui": {
        "theme": "light",
    },
    "purchase": {
        "enabled": False,
        "product_url": "",
        "products_id": 0,
        "quantity": 1,
    },
}


with (
    TEST_CONFIG_DIR / "config.yaml"
).open(
    "w",
    encoding="utf-8",
) as file:
    yaml.safe_dump(
        CONFIG_DATA,
        file,
        allow_unicode=True,
        sort_keys=False,
    )


config = ConfigManager(
    TEST_CONFIG_DIR,
)

worker = PurchaseWorkerFactory.create(
    config,
)

assert worker is None

print()
print(
    "PURCHASE WORKER FACTORY DISABLED TEST PASSED"
)
print("purchase.enabled -> False")
print("worker -> None")