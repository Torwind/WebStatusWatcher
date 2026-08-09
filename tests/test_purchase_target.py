from web_status_watcher.purchase.target import PurchaseTarget


# ---------------------------------------------------------
# Valid target
# ---------------------------------------------------------

target = PurchaseTarget(
    product_url="https://coins.bank.gov.ua/test-product.html",
    products_id=1126,
    quantity=1,
    enabled=True,
)

assert target.product_url == (
    "https://coins.bank.gov.ua/test-product.html"
)

assert target.products_id == 1126
assert target.quantity == 1
assert target.enabled is True


# ---------------------------------------------------------
# Invalid product ID
# ---------------------------------------------------------

try:
    PurchaseTarget(
        product_url="https://coins.bank.gov.ua/test-product.html",
        products_id=0,
    )

    raise AssertionError(
        "products_id=0 should raise ValueError"
    )

except ValueError:
    pass


# ---------------------------------------------------------
# Invalid quantity
# ---------------------------------------------------------

try:
    PurchaseTarget(
        product_url="https://coins.bank.gov.ua/test-product.html",
        products_id=1126,
        quantity=0,
    )

    raise AssertionError(
        "quantity=0 should raise ValueError"
    )

except ValueError:
    pass


# ---------------------------------------------------------
# Empty URL
# ---------------------------------------------------------

try:
    PurchaseTarget(
        product_url="",
        products_id=1126,
    )

    raise AssertionError(
        "Empty product_url should raise ValueError"
    )

except ValueError:
    pass


print()
print("PURCHASE TARGET TEST PASSED")