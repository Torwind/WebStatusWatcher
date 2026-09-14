from types import SimpleNamespace

from web_status_watcher.purchase.worker_factory import (
    PurchaseWorkerFactory,
)
from web_status_watcher.scheduler.worker import (
    Worker,
)


target = SimpleNamespace(
    enabled=True,
    product_url=(
        "https://coins.bank.gov.ua/"
        "arhistratig-mihajil-c-/p-1126.html?cid=14348"
    ),
    products_id=1126,
    quantity=1,
)


cart_item = SimpleNamespace(
    products_id=1126,
    quantity=1,
    name="Архістратиг Михаїл  (c)",
    price=5087.0,
)


class FakeBrowserClient:
    connect_calls = 0
    availability_calls = 0
    add_calls = 0
    close_calls = 0

    @classmethod
    def connect(cls):
        cls.connect_calls += 1
        return cls()

    def is_available(
        self,
        current_target,
    ) -> bool:
        type(self).availability_calls += 1
        return True

    def add_to_cart(
        self,
        current_target,
    ):
        type(self).add_calls += 1
        return cart_item

    def close(self) -> None:
        type(self).close_calls += 1


module = __import__(
    "web_status_watcher.purchase.worker_factory",
    fromlist=[
        "PurchaseCartClient",
        "PurchaseTargetFactory",
    ],
)

original_cart_client = module.PurchaseCartClient
original_target_factory = module.PurchaseTargetFactory


class FakeTargetFactory:
    @staticmethod
    def create(config):
        return target


module.PurchaseCartClient = FakeBrowserClient
module.PurchaseTargetFactory = FakeTargetFactory


try:
    worker = PurchaseWorkerFactory.create(
        object(),
    )

    assert isinstance(
        worker,
        Worker,
    )

    assert worker.name == "purchase"
    assert worker.interval == 1
    assert worker.running is True

    # Client is created lazily on the first tick.
    assert FakeBrowserClient.connect_calls == 0

    worker.tick()

    assert FakeBrowserClient.connect_calls == 1
    assert FakeBrowserClient.availability_calls == 1
    assert FakeBrowserClient.add_calls == 1
    assert FakeBrowserClient.close_calls == 1

    assert worker.running is False

    # No second purchase attempt after stop.
    worker.tick()

    assert FakeBrowserClient.connect_calls == 1
    assert FakeBrowserClient.availability_calls == 1
    assert FakeBrowserClient.add_calls == 1
    assert FakeBrowserClient.close_calls == 1

finally:
    module.PurchaseCartClient = (
        original_cart_client
    )

    module.PurchaseTargetFactory = (
        original_target_factory
    )


print()
print(
    "PURCHASE WORKER CART INTEGRATION TEST PASSED"
)
print(
    "create() -> no browser connection"
)
print(
    "first tick -> connect() -> 1"
)
print(
    "is_available() -> 1"
)
print(
    "add_to_cart() -> 1"
)
print(
    "close() -> 1"
)
print(
    "worker.stop() -> running=False"
)
print(
    "next tick -> no second purchase"
)