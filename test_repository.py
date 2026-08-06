from web_status_watcher.constants import DATA_DIR
from web_status_watcher.database import Database

db = Database(
    DATA_DIR / "webstatuswatcher.db"
)

db.connect()

assert db.sites is not None

sites = db.sites.get_all()

for site in sites:
    print(
        site["id"],
        site["name"],
        site["url"],
    )

db.close()