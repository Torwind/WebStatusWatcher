from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

from web_status_watcher.network import HttpClient
from web_status_watcher.purchase.detector import PurchaseAvailabilityDetector
from web_status_watcher.purchase.status import PurchaseAvailabilityStatus


PRODUCT_URL = (
    "https://coins.bank.gov.ua/"
    "-30-rokiv-konstituciji-ukrajini-c-/p-1205.html"
)


PRODUCT_HTML = """
<html>
<head>
    <title>"30 років онституції країни" (c) - рхів</title>
</head>
<body>
    <div class="container-product-info">
        <input type="hidden" name="products_id" value="1205">

        <div class="prod_buy_btns">
        </div>

        <p class="p-info-climit">
            ам доступно для придбання ще <span>1</span> шт.
        </p>

        <p>
            іміт продукції на одного користувача становить 1 шт.
        </p>

        <p>
            а складі залишилося всього
            <span class="pd_qty">0</span> шт.
        </p>
    </div>
</body>
</html>
"""


class MockHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        body = PRODUCT_HTML.encode("utf-8")

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8",
        )

        self.send_header(
            "Content-Length",
            str(len(body)),
        )

        self.end_headers()

        self.wfile.write(body)

    def log_message(self, format, *args) -> None:
        pass


class MockHttpClient:
    def __init__(
        self,
        client: HttpClient,
        base_url: str,
    ) -> None:
        self._client = client
        self._base_url = base_url

    def get(self, url: str):
        from urllib.parse import urlparse

        parsed = urlparse(url)

        local_url = self._base_url + parsed.path

        if parsed.query:
            local_url += "?" + parsed.query

        return self._client.get(local_url)


server = HTTPServer(
    ("127.0.0.1", 8766),
    MockHandler,
)

thread = threading.Thread(
    target=server.serve_forever,
    daemon=True,
)

thread.start()

try:
    detector = PurchaseAvailabilityDetector()

    with HttpClient(
        timeout=5.0,
        retry_attempts=1,
    ) as http_client:

        mock_client = MockHttpClient(
            http_client,
            "http://127.0.0.1:8766",
        )

        response = mock_client.get(
            PRODUCT_URL,
        )

        assert response.status_code == 200

        result = detector.detect(
            response.text,
        )

    assert result == PurchaseAvailabilityStatus.NOT_AVAILABLE

    print()
    print("PURCHASE AVAILABILITY STOCK HTTPCLIENT TEST PASSED")
    print("products_id=1205")
    print("status_code=200")
    print("pd_qty=0")
    print(f"status={result.name}")

finally:
    server.shutdown()
    server.server_close()
