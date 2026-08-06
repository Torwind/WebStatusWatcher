from web_status_watcher.network.response import HttpResponse
from web_status_watcher.services.response_mapper import ResponseMapper

response = HttpResponse(
    url="https://example.com",
    status_code=200,
    text="<html>Hello</html>",
    elapsed=0.15,
    ok=True,
    headers={},
)

result = ResponseMapper.map(response)

print(result.status)
print(result.http_status)
print(result.content_length)
print(result.content_hash)
print(result.ok)