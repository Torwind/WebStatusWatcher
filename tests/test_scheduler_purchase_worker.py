from web_status_watcher.scheduler.worker import Worker


calls = []


def purchase_tick():
    calls.append("purchase")


worker = Worker(
    name="purchase",
    interval=1,
    callback=purchase_tick,
)


worker.tick()

assert calls == ["purchase"]

worker.tick()

assert calls == [
    "purchase",
    "purchase",
]


print()
print("SCHEDULER PURCHASE WORKER TEST PASSED")
print("tick 1 -> purchase")
print("tick 2 -> purchase")
print("callback calls -> 2")