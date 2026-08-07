from web_status_watcher.services.response_mapper import ResponseMapper
from web_status_watcher.network.exceptions import (
    HttpRequestError,
    TimeoutError,
)
from web_status_watcher.status import Status


timeout_result = ResponseMapper.error(
    Status.TIMEOUT,
    "Request timeout",
)

print(timeout_result.status)
print(timeout_result.http_status)
print(timeout_result.message)
print(timeout_result.ok)


network_result = ResponseMapper.error(
    Status.OFFLINE,
    "Connection failed",
)

print(network_result.status)
print(network_result.http_status)
print(network_result.message)
print(network_result.ok)