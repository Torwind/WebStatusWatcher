import time

from web_status_watcher.constants import DATABASE_FILE
from web_status_watcher.database import Database
from web_status_watcher.scheduler.scheduler import Scheduler
from web_status_watcher.scheduler.worker import Worker
from web_status_watcher.services.monitor_service import MonitorService

database = Database(DATABASE_FILE)
database.connect()

service = MonitorService(database)

scheduler = Scheduler()

scheduler.add_worker(
    Worker(
        "monitor",
        1,
        service.tick,
    )
)

scheduler.start()

time.sleep(35)

scheduler.stop()

database.close()