from web_status_watcher.scheduler.worker import (
    Worker,
)


calls = 0


def callback() -> None:
    global calls
    calls += 1


worker = Worker(
    name="test",
    interval=1,
    callback=callback,
)

assert worker.running is True

worker.tick()

assert calls == 1

worker.stop()

assert worker.running is False

worker.tick()

assert calls == 1

worker.start()

assert worker.running is True

worker.tick()

assert calls == 2


print()
print("WORKER STOP TEST PASSED")
print("initial tick -> callback called")
print("stop -> callback skipped")
print("start -> callback resumed")