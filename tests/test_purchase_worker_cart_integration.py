from types import SimpleNamespace

from web_status_watcher.purchase.events import PurchaseAvailableEvent
from web_status_watcher.purchase.worker_factory import PurchaseWorkerFactory
from web_status_watcher.scheduler.worker import Worker


target = SimpleNamespace(
    enabled=True,
    product_url="https://coins.bank.gov.ua/arhistratig-mihajil-c-/p-1126.html?cid=14348",
    products_id=1126,
    quantity=1,
)

service = SimpleNamespace(
    target=target,
    check_calls=0,
)

service.check_event = lambda: (
    setattr(service, "check_calls", service.check_calls + 1)
    or PurchaseAvailableEvent(
        products_id=1126,
        cid=14348,
    )
)

cart_item = SimpleNamespace(
    products_id=1126,
    quantity=1,
    name="Архістратиг Михаїл (c)",
    price=5121.0,
)

cart_client = SimpleNamespace(
    add_to_cart=lambda current_target: cart_item,
    close=lambda: None,
)

cart_factory = SimpleNamespace(
    connect=lambda: cart_client,
)

worker_module = __import__(
    "web_status_watcher.purchase.worker_factory",
    fromlist=["PurchaseCartClient"],
)

original_create_service = PurchaseWorkerFactory.create_service
original_cart_client = worker_module.PurchaseCartClient

PurchaseWorkerFactory.create_service = staticmethod(
    lambda config: service
)

worker_module.PurchaseCartClient = cart_factory

worker = PurchaseWorkerFactory.create(object())

assert isinstance(worker, Worker)
assert worker.name == "purchase"
assert worker.running is True

worker.tick()

assert service.check_calls == 1
assert worker.running is False

worker.tick()

assert service.check_calls == 1

PurchaseWorkerFactory.create_service = original_create_service
worker_module.PurchaseCartClient = original_cart_client

print()
print("PURCHASE WORKER CART INTEGRATION TEST PASSED")
print("AVAILABLE event -> add_to_cart()")
print("add_to_cart() -> worker.stop()")
print("next tick -> no second availability check")