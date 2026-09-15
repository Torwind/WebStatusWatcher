from pathlib import Path

from web_status_watcher.config.config_manager import (
    ConfigManager,
)
from web_status_watcher.purchase.worker_factory import (
    PurchaseWorkerFactory,
)


config_dir = Path("tests") / "tmp_purchase_config"
config_dir.mkdir(
    parents=True,
    exist_ok=True,
)

config_file = config_dir / "config.yaml"

config_file.write_text(
    """
purchase:
  enabled: true
  product_url: "https://coins.bank.gov.ua/arhistratig-mihajil-c-/p-1126.html?cid=14348"
  products_id: 1126
  quantity: 1
""".strip(),
    encoding="utf-8",
)

config = ConfigManager(
    config_dir,
)

worker = PurchaseWorkerFactory.create(
    config,
)

assert worker is not None
assert worker.name == "purchase"
assert worker.interval == 1.25
assert worker.running is True
assert callable(worker.callback)


worker.stop()

assert worker.running is False

print()
print(
    "PURCHASE WORKER ENABLED TEST PASSED"
)
print(
    f"name -> {worker.name}"
)
print(
    f"interval -> {worker.interval}"
)
print(
    f"running -> {worker.running}"
)
print(
    f"interval -> {worker.interval}"
)