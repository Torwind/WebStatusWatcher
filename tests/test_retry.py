from web_status_watcher.network import RetryEngine
from web_status_watcher.network.exceptions import HttpRequestError


attempts = 0


def operation():
    global attempts

    attempts += 1

    print(f"Attempt {attempts}")

    if attempts < 3:
        raise HttpRequestError("Temporary failure")

    return "SUCCESS"


retry = RetryEngine(
    attempts=3,
    delay=0,
)

result = retry.execute(operation)

print(result)
print(f"Total attempts: {attempts}")