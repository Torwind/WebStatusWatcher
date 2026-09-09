from web_status_watcher.purchase.cart import (
    CartItem,
    parse_cart_response,
)


response = {
    "success": True,
    "status": 1,
    "id": "1126",
    "name": "Архістратиг Михаїл  (c)",
    "price": 4993,
    "quantity": 1,
    "cart": {
        "cart_count": 1,
    },
}


item = parse_cart_response(
    response,
)

assert isinstance(
    item,
    CartItem,
)

assert item.products_id == 1126
assert item.quantity == 1
assert item.name == (
    "Архістратиг Михаїл  (c)"
)
assert item.price == 4993


empty_response = {
    "success": True,
    "status": 0,
}


assert parse_cart_response(
    empty_response,
) is None


print()
print("PURCHASE CART TEST PASSED")
print("products_id -> 1126")
print("quantity -> 1")
print("price -> 4993")
print("empty cart response -> None")