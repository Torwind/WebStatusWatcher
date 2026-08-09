from web_status_watcher.purchase.checker import AvailabilityChecker
from web_status_watcher.purchase.url_parser import ProductUrlParser


PRODUCT_URL = (
    "https://coins.bank.gov.ua/"
    "arhistratig-mihajil-c-/p-1126.html?cid=14348"
)


class MockResponse:
    def __init__(self, status_code: int, text: str) -> None:
        self.status_code = status_code
        self.text = text


class MockHttpClient:
    def __init__(self, response: MockResponse) -> None:
        self._response = response

    def get(self, url: str) -> MockResponse:
        return self._response


product = ProductUrlParser.parse(PRODUCT_URL)


# 1. HTTP 200 + active "Купити" button
client = MockHttpClient(
    MockResponse(
        200,
        '<button type="submit" class="btn-primary buy">Купити</button>',
    )
)

checker = AvailabilityChecker(client)
result = checker.check(product)

assert result.available is True
assert result.products_id == 1126
assert result.cid == 14348
assert result.status_code == 200


# 2. HTTP 200 without "Купити" button
client = MockHttpClient(
    MockResponse(
        200,
        "<html><body>Очікується надходження</body></html>",
    )
)

checker = AvailabilityChecker(client)
result = checker.check(product)

assert result.available is False
assert result.products_id == 1126
assert result.cid == 14348
assert result.status_code == 200


# 3. HTTP 404
client = MockHttpClient(
    MockResponse(
        404,
        "<html>Not Found</html>",
    )
)

checker = AvailabilityChecker(client)
result = checker.check(product)

assert result.available is False
assert result.products_id == 1126
assert result.cid == 14348
assert result.status_code == 404


print()
print("AVAILABILITY CHECKER V2 TEST PASSED")
print("200 + Купити -> available=True")
print("200 без Купити -> available=False")
print("404 -> available=False")
