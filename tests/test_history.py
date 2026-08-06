from web_status_watcher.constants import DATABASE_FILE
from web_status_watcher.database import Database

db = Database(DATABASE_FILE)
db.connect()

rows = db.connection.execute(
    """
    SELECT
        id,
        site_id,
        checked_at,
        status_code,
        elapsed,
        content_length
    FROM history
    ORDER BY id DESC
    """
).fetchall()

print(f"History records: {len(rows)}")
print()

for row in rows:
    print(
        row["id"],
        row["site_id"],
        row["checked_at"],
        row["status_code"],
        row["elapsed"],
        row["content_length"],
    )

db.close()