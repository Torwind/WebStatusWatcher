from web_status_watcher.purchase.events import (
    PurchaseAvailableEvent,
)


event = PurchaseAvailableEvent(
    products_id=1126,
    cid=14348,
)

assert event.products_id == 1126
assert event.cid == 14348


print()
print("PURCHASE EVENTS TEST PASSED")
print("products_id -> 1126")
print("cid -> 14348")