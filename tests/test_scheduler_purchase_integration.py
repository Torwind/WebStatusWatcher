from web_status_watcher.scheduler.scheduler import Scheduler
from web_status_watcher.scheduler.worker import Worker


calls = []


def purchase_tick():
    calls.append("purchase")


scheduler = Scheduler()

scheduler.add_worker(
    Worker(
        name="purchase",
        interval=1,
        callback=purchase_tick,
    )
)


worker = scheduler._workers[0]

worker.tick()
worker.tick()
worker.tick()

assert calls == [
    "purchase",
    "purchase",
    "purchase",
]

print()
print("SCHEDULER PURCHASE INTEGRATION TEST PASSED")
print("purchase worker ticks -> 3")
print("purchase callback calls -> 3")