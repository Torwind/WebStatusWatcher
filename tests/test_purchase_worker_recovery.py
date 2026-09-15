from types import SimpleNamespace

import web_status_watcher.purchase.worker_factory as module
import web_status_watcher.scheduler.worker as worker_module

from web_status_watcher.purchase.worker_factory import (
    PurchaseWorkerFactory,
)


target = SimpleNamespace(
    enabled=True,
    product_url="https://example.com/product",
    products_id=1126,
    quantity=1,
)


class FakeConfig:
    @staticmethod
    def get(
        key,
        default=None,
    ):
        if key == "purchase.interval":
            return 1.25

        return default


class FakeBrowserClient:
    connect_calls = 0
    close_calls = 0
    instances = []

    @classmethod
    def connect(cls):
        cls.connect_calls += 1

        client = cls()
        cls.instances.append(client)

        return client

    def __init__(self):
        self.availability_calls = 0

    def is_available(
        self,
        current_target,
    ) -> bool:
        self.availability_calls += 1

        raise RuntimeError(
            "Persistent availability failure"
        )

    def add_to_cart(
        self,
        current_target,
    ):
        raise AssertionError(
            "add_to_cart() must not be called"
        )

    def close(self) -> None:
        type(self).close_calls += 1


class FakeTargetFactory:
    @staticmethod
    def create(
        config,
    ):
        return target


class FakeClock:
    value = 100.0

    @classmethod
    def monotonic(cls) -> float:
        return cls.value


original_cart_client = module.PurchaseCartClient
original_target_factory = module.PurchaseTargetFactory
original_monotonic = worker_module.time.monotonic

module.PurchaseCartClient = FakeBrowserClient
module.PurchaseTargetFactory = FakeTargetFactory
worker_module.time.monotonic = FakeClock.monotonic


try:

    worker = PurchaseWorkerFactory.create(
        FakeConfig(),
    )

    assert worker is not None
    assert worker.running is True
    assert worker.interval == 1.25

    # First tick:
    # initial probe + 3 immediate retries = 4 attempts.
    worker.tick()

    assert (
        FakeBrowserClient.connect_calls
        == 1
    )

    assert (
        FakeBrowserClient.instances[0].availability_calls
        == 4
    )

    assert (
        FakeBrowserClient.close_calls
        == 1
    )

    assert worker.running is True

    # Advance beyond the 1.25 second worker interval.
    FakeClock.value = 101.25

    # Second normal tick must create a fresh browser client.
    worker.tick()

    assert (
        FakeBrowserClient.connect_calls
        == 2
    )

    assert (
        FakeBrowserClient.instances[1].availability_calls
        == 4
    )

    assert (
        FakeBrowserClient.close_calls
        == 2
    )

    assert worker.running is True

finally:

    module.PurchaseCartClient = (
        original_cart_client
    )

    module.PurchaseTargetFactory = (
        original_target_factory
    )

    worker_module.time.monotonic = (
        original_monotonic
    )


print()
print(
    "PURCHASE WORKER RECOVERY TEST PASSED"
)
print(
    "first connect() -> 1"
)
print(
    "first probe attempts -> 4"
)
print(
    "first client close() -> 1"
)
print(
    "second tick after 1.25s -> connect() -> 2"
)
print(
    "second probe attempts -> 4"
)
print(
    "total close() -> 2"
)
print(
    "worker remains running -> True"
)
