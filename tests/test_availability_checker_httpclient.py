from __future__ import annotations

import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from web_status_watcher.network import HttpClient
from web_status_watcher.purchase.checker import AvailabilityChecker
from web_status_watcher.purchase.url_parser import ProductUrlParser


PRODUCT_URL = (
    "https://coins.bank.gov.ua/"
    "arhistratig-mihajil-c-/p-1126.html?cid=14348"
)


class MockHandler(BaseHTTPRequestHandler):

    def do_GET(self) -> None:

        if self.path.startswith(
            "/arhistratig-mihajil-c-/p-1126.html"
        ):

            body = (
                "<html>"
                '<div id="r_buy_intovar" data-id="1126">'
                '<button type="submit" class="btn-primary buy">'
                "Купити"
                "</button>"
                "</div>"
                "</html>"
            ).encode("utf-8")

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

            return

        self.send_response(404)
        self.end_headers()

    def log_message(
        self,
        format: str,
        *args,
    ) -> None:
        pass


class MockHttpClient:
    """
    Adapter that redirects the product request
    to the local mock HTTP server.

    The real WebStatusWatcher HttpClient is used
    internally.
    """

    def __init__(
        self,
        client: HttpClient,
        base_url: str,
    ) -> None:

        self._client = client
        self._base_url = base_url

    def get(self, url: str):

        parsed = urlparse(url)

        local_url = (
            self._base_url
            + parsed.path
        )

        if parsed.query:
            local_url += "?" + parsed.query

        return self._client.get(
            local_url,
        )


server = HTTPServer(
    ("127.0.0.1", 8765),
    MockHandler,
)

thread = threading.Thread(
    target=server.serve_forever,
    daemon=True,
)

thread.start()


try:

    # Parse the real coins.bank.gov.ua URL.
    product = ProductUrlParser.parse(
        PRODUCT_URL,
    )

    assert product.products_id == 1126
    assert product.cid == 14348

    # Use the real WebStatusWatcher HttpClient.
    with HttpClient(
        timeout=5.0,
        retry_attempts=1,
    ) as http_client:

        mock_client = MockHttpClient(
            http_client,
            "http://127.0.0.1:8765",
        )

        checker = AvailabilityChecker(
            mock_client,
        )

        result = checker.check(
            product,
        )

    assert result.available is True
    assert result.products_id == 1126
    assert result.cid == 14348
    assert result.status_code == 200

    print()
    print("AVAILABILITY HTTPCLIENT TEST PASSED")
    print(
        f"products_id={result.products_id}, "
        f"cid={result.cid}"
    )
    print(
        f"status_code={result.status_code}, "
        f"available={result.available}"
    )

finally:

    server.shutdown()
    server.server_close()
