import web_status_watcher.scheduler.worker as worker_module
from web_status_watcher.scheduler.worker import Worker


calls = []


def purchase_tick():
    calls.append("purchase")


worker = Worker(
    name="purchase",
    interval=1.25,
    callback=purchase_tick,
)


class FakeClock:
    value = 100.0

    @classmethod
    def monotonic(cls) -> float:
        return cls.value


original_monotonic = worker_module.time.monotonic

worker_module.time.monotonic = (
    FakeClock.monotonic
)

try:

    # First tick runs immediately.
    worker.tick()

    assert calls == [
        "purchase",
    ]

    # 1.0 second later: interval has not elapsed.
    FakeClock.value = 101.0

    worker.tick()

    assert calls == [
        "purchase",
    ]

    # 1.25 seconds later: callback runs again.
    FakeClock.value = 101.25

    worker.tick()

    assert calls == [
        "purchase",
        "purchase",
    ]

    # 0.25 second later: too early for another run.
    FakeClock.value = 101.50

    worker.tick()

    assert calls == [
        "purchase",
        "purchase",
    ]

    # Another 1.25 seconds from previous execution.
    FakeClock.value = 102.50

    worker.tick()

    assert calls == [
        "purchase",
        "purchase",
        "purchase",
    ]

finally:

    worker_module.time.monotonic = (
        original_monotonic
    )


print()
print(
    "SCHEDULER PURCHASE WORKER TEST PASSED"
)
print(
    "first tick -> purchase"
)
print(
    "after 1.00s -> skipped"
)
print(
    "after 1.25s -> purchase"
)
print(
    "after 0.25s -> skipped"
)
print(
    "after next 1.25s -> purchase"
)