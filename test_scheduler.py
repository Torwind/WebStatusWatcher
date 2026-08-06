import time

from web_status_watcher.scheduler.scheduler import Scheduler
from web_status_watcher.scheduler.worker import Worker


def hello():

    print("Scheduler works!")


scheduler = Scheduler()

scheduler.add_worker(
    Worker(
        "hello",
        3,
        hello,
    )
)

scheduler.start()

time.sleep(10)

scheduler.stop()