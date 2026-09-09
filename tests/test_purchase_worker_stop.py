from web_status_watcher.scheduler.worker import (
    Worker,
)


calls = 0


def callback() -> None:
    global calls

    calls += 1


worker = Worker(
    name="purchase",
    interval=1,
    callback=callback,
)

worker.tick()

assert calls == 1
assert worker.running is True

worker.stop()

worker.tick()

assert calls == 1
assert worker.running is False

print()
print("PURCHASE WORKER STOP TEST PASSED")
print("callback before stop -> 1")
print("callback after stop -> still 1")
print("worker.running -> False")