from web_status_watcher.constants import DATABASE_FILE
from web_status_watcher.database import Database


database = Database(DATABASE_FILE)

database.connect()

assert database.history is not None

last = database.history.get_last(1)

if last is None:
    print("No history records")
else:
    print(
        last["id"],
        last["site_id"],
        last["status_code"],
        last["elapsed"],
        last["content_length"],
        last["content_hash"],
    )

database.close()