from web_status_watcher.purchase.checker import (
    AvailabilityChecker,
)
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

    def get(
        self,
        url: str,
    ) -> MockResponse:
        return self._response


product = ProductUrlParser.parse(PRODUCT_URL)


# 1. Product is available for purchase.
client = MockHttpClient(
    MockResponse(
        200,
        '''
        <div id="r_buy_intovar">
            <button
                type="submit"
                class="btn-primary buy"
            >
                Купити
            </button>
        </div>
        ''',
    )
)

checker = AvailabilityChecker(client)
result = checker.check(product)

assert result.available is True
assert (
    result.status
    == PurchaseAvailabilityStatus.AVAILABLE
)
assert result.products_id == 1126
assert result.cid == 14348
assert result.status_code == 200


# 2. Product is not available.
client = MockHttpClient(
    MockResponse(
        200,
        '''
        <html>
            <body>
                Очікується надходження
            </body>
        </html>
        ''',
    )
)

checker = AvailabilityChecker(client)
result = checker.check(product)

assert result.available is False
assert (
    result.status
    == PurchaseAvailabilityStatus.NOT_AVAILABLE
)
assert result.products_id == 1126
assert result.cid == 14348
assert result.status_code == 200


# 3. Purchase limit has been reached.
client = MockHttpClient(
    MockResponse(
        200,
        '''
        <html>
            <body>
                Ви використали свій ліміт
            </body>
        </html>
        ''',
    )
)

checker = AvailabilityChecker(client)
result = checker.check(product)

assert result.available is False
assert (
    result.status
    == PurchaseAvailabilityStatus.LIMIT_REACHED
)
assert result.products_id == 1126
assert result.cid == 14348
assert result.status_code == 200


# 4. Product page was not found.
client = MockHttpClient(
    MockResponse(
        404,
        "<html>Not Found</html>",
    )
)

checker = AvailabilityChecker(client)
result = checker.check(product)

assert result.available is False
assert (
    result.status
    == PurchaseAvailabilityStatus.NOT_AVAILABLE
)
assert result.products_id == 1126
assert result.cid == 14348
assert result.status_code == 404


print()
print("AVAILABILITY CHECKER TEST PASSED")
print("AVAILABLE -> available=True")
print("NOT_AVAILABLE -> available=False")
print("LIMIT_REACHED -> available=False")
print("HTTP 404 -> not_available")