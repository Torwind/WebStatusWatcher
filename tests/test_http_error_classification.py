from __future__ import annotations

from web_status_watcher.network.response import HttpResponse
from web_status_watcher.services.response_mapper import ResponseMapper
from web_status_watcher.status import Status


def make_response(status_code: int) -> HttpResponse:
    return HttpResponse(
        url="https://example.com",
        status_code=status_code,
        text="TEST",
        elapsed=0.1,
        ok=200 <= status_code < 300,
        headers={},
    )


# ---------------------------------------------------------
# 200 OK
# ---------------------------------------------------------

result = ResponseMapper.map(
    make_response(200)
)

print(
    "200:",
    result.status.value,
    result.http_status,
)

assert result.status == Status.ONLINE
assert result.http_status == 200


# ---------------------------------------------------------
# 301 Redirect
# ---------------------------------------------------------

result = ResponseMapper.map(
    make_response(301)
)

print(
    "301:",
    result.status.value,
    result.http_status,
)

assert result.status == Status.HTTP_ERROR
assert result.http_status == 301


# ---------------------------------------------------------
# 404 Not Found
# ---------------------------------------------------------

result = ResponseMapper.map(
    make_response(404)
)

print(
    "404:",
    result.status.value,
    result.http_status,
)

assert result.status == Status.HTTP_ERROR
assert result.http_status == 404


# ---------------------------------------------------------
# 500 Internal Server Error
# ---------------------------------------------------------

result = ResponseMapper.map(
    make_response(500)
)

print(
    "500:",
    result.status.value,
    result.http_status,
)

assert result.status == Status.HTTP_ERROR
assert result.http_status == 500


print()
print("HTTP ERROR CLASSIFICATION TEST PASSED")