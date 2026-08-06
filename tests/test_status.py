from web_status_watcher.status import (
    Status,
    CheckResult,
)

result = CheckResult(
    status=Status.ONLINE,
    http_status=200,
    elapsed=0.185,
    content_length=559,
)

print(result)

print(result.ok)