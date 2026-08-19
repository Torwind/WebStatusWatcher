from web_status_watcher.purchase.checker import AvailabilityChecker
from web_status_watcher.purchase.status import (
    PurchaseAvailabilityStatus,
)
from web_status_watcher.purchase.url_parser import (
    ProductUrlParser,
)


PRODUCT_URL = (
    "https://coins.bank.gov.ua/"
    "arhistratig-mihajil-c-/p-1126.html?cid=14348"
)


class MockResponse:
    def __init__(
        self,
        status_code: int,
        text: str,
    ) -> None:
        self.status_code = status_code
        self.text = text


class MockHttpClient:
    def __init__(
        self,
        response: MockResponse,
    ) -> None:
        self._response = response

    def get(self, url: str) -> MockResponse:
        return self._response


LIMIT_HTML = """
<html>
<body>

<p style="font-weight: bold;">
    Ви використали свій ліміт
</p>

<p>
    Ліміт продукції на одного користувача становить 1 шт.
</p>

</body>
</html>
"""


product = ProductUrlParser.parse(
    PRODUCT_URL,
)

client = MockHttpClient(
    MockResponse(
        status_code=200,
        text=LIMIT_HTML,
    ),
)

checker = AvailabilityChecker(
    client,
)

result = checker.check(
    product,
)

assert result.available is False

assert (
    result.status
    == PurchaseAvailabilityStatus.LIMIT_REACHED
)

assert result.products_id == 1126
assert result.cid == 14348
assert result.status_code == 200

print("PURCHASE LIMIT CHECKER TEST PASSED")
print(
    f"products_id={result.products_id}, "
    f"cid={result.cid}"
)
print(
    f"status_code={result.status_code}, "
    f"available={result.available}"
)
print(
    f"status={result.status.value}"
)