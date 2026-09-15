from types import SimpleNamespace

import web_status_watcher.purchase.worker_factory as module
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
    availability_calls = 0
    add_calls = 0
    close_calls = 0

    failures_before_success = 2

    @classmethod
    def connect(cls):
        cls.connect_calls += 1
        return cls()

    def is_available(
        self,
        current_target,
    ) -> bool:
        type(self).availability_calls += 1

        if (
            type(self).availability_calls
            <= type(self).failures_before_success
        ):
            raise RuntimeError(
                "Temporary availability failure"
            )

        return True

    def add_to_cart(
        self,
        current_target,
    ):
        type(self).add_calls += 1

        return SimpleNamespace(
            products_id=1126,
            quantity=1,
        )

    def close(
        self,
    ) -> None:
        type(self).close_calls += 1


class FakeTargetFactory:
    @staticmethod
    def create(
        config,
    ):
        return target


original_cart_client = module.PurchaseCartClient
original_target_factory = module.PurchaseTargetFactory


module.PurchaseCartClient = FakeBrowserClient
module.PurchaseTargetFactory = FakeTargetFactory


try:

    worker = PurchaseWorkerFactory.create(
        FakeConfig(),
    )

    assert worker is not None

    worker.tick()

    assert (
        FakeBrowserClient.connect_calls
        == 1
    )

    assert (
        FakeBrowserClient.availability_calls
        == 3
    )

    assert (
        FakeBrowserClient.add_calls
        == 1
    )

    assert (
        FakeBrowserClient.close_calls
        == 1
    )

    assert worker.running is False

finally:

    module.PurchaseCartClient = (
        original_cart_client
    )

    module.PurchaseTargetFactory = (
        original_target_factory
    )


print()
print(
    "PURCHASE WORKER IMMEDIATE RETRY TEST PASSED"
)
print(
    "connect() -> 1"
)
print(
    "availability attempts -> 3"
)
print(
    "failures -> 2"
)
print(
    "successful retry -> immediate"
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
