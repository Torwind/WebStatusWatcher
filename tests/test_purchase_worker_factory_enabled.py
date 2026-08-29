from pathlib import Path
import yaml

from web_status_watcher.config.config_manager import (
    ConfigManager,
)
from web_status_watcher.purchase.worker_factory import (
    PurchaseWorkerFactory,
)


TEST_CONFIG_DIR = Path("data/test_purchase_worker_config")


TEST_CONFIG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


config_file = TEST_CONFIG_DIR / "config.yaml"


config_data = {
    "application": {
        "name": "WebStatusWatcher",
        "version": "1.0.0",
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
        "enabled": True,
        "product_url": (
            "https://coins.bank.gov.ua/"
            "arhistratig-mihajil-c-/p-1126.html"
            "?cid=14348"
        ),
        "products_id": 1126,
        "quantity": 1,
    },
}


with config_file.open(
    "w",
    encoding="utf-8",
) as file:
    yaml.safe_dump(
        config_data,
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

assert worker is not None
assert worker.name == "purchase"
assert worker.interval == 1
assert callable(worker.callback)


print()
print(
    "PURCHASE WORKER FACTORY ENABLED TEST PASSED"
)
print("purchase.enabled -> True")
print("worker.name -> purchase")
print("worker.interval -> 1")
print("worker.callback -> callable")