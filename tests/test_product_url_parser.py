from web_status_watcher.purchase.url_parser import (
    ProductUrlParser,
)


URL = (
    "https://coins.bank.gov.ua/"
    "arhistratig-mihajil-c-/p-1126.html?cid=14348"
)


product = ProductUrlParser.parse(URL)

assert product.url == URL
assert product.products_id == 1126
assert product.cid == 14348


# Empty URL
try:
    ProductUrlParser.parse("")
except ValueError:
    pass
else:
    raise AssertionError(
        "Empty URL must raise ValueError"
    )


# Wrong host
try:
    ProductUrlParser.parse(
        "https://example.com/p-1126.html?cid=14348"
    )
except ValueError:
    pass
else:
    raise AssertionError(
        "Wrong host must raise ValueError"
    )


# Missing product ID
try:
    ProductUrlParser.parse(
        "https://coins.bank.gov.ua/product.html?cid=14348"
    )
except ValueError:
    pass
else:
    raise AssertionError(
        "Missing products_id must raise ValueError"
    )


# Missing cid
try:
    ProductUrlParser.parse(
        "https://coins.bank.gov.ua/"
        "arhistratig-mihajil-c-/p-1126.html"
    )
except ValueError:
    pass
else:
    raise AssertionError(
        "Missing cid must raise ValueError"
    )


print()
print("PRODUCT URL PARSER TEST PASSED")
print(
    f"products_id={product.products_id}, "
    f"cid={product.cid}"
)