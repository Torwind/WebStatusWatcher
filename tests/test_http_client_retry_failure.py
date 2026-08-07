from web_status_watcher.network import HttpClient
from web_status_watcher.network.exceptions import HttpRequestError


client = HttpClient(
    timeout=5.0,
    retry_attempts=3,
    retry_delay=0,
)


calls = 0


def fake_request(*args, **kwargs):
    global calls

    calls += 1

    print(f"HTTP attempt: {calls}")

    raise HttpRequestError(
        "Simulated network failure"
    )


client._client.request = fake_request

try:
    client.get("https://example.com")

except HttpRequestError as exc:
    print(f"Final error: {exc}")

finally:
    client.close()


print(f"Total attempts: {calls}")