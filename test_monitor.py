from web_status_watcher.constants import DATABASE_FILE
from web_status_watcher.database import Database
from web_status_watcher.services.monitor_service import MonitorService

database = Database(DATABASE_FILE)

database.connect()

service = MonitorService(database)

service.check_all()

database.close()