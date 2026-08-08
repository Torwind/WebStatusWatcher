from __future__ import annotations

from pathlib import Path

from web_status_watcher.database import Database
from web_status_watcher.services.monitor_service import MonitorService
from web_status_watcher.status import Status


TEST_DB = Path("data/test_content_change.db")

if TEST_DB.exists():
    TEST_DB.unlink()


database = Database(TEST_DB)
database.connect()

assert database.sites is not None
assert database.history is not None


# ---------------------------------------------------------
# Create test site
# ---------------------------------------------------------

database.connection.execute(
    """
    INSERT INTO sites
    (
        name,
        url,
        interval_seconds,
        enabled
    )
    VALUES (?, ?, ?, ?)
    """,
    (
        "Content Change Test",
        "https://example.com",
        1,
        1,
    ),
)

database.connection.commit()

site = database.sites.get_by_id(1)

assert site is not None


# ---------------------------------------------------------
# Fake HTTP client
# ---------------------------------------------------------

class FakeClient:

    def __init__(self) -> None:
        self.calls = 0

    def get(self, url: str):

        self.calls += 1

        # 1. Initial ONLINE response.
        if self.calls == 1:

            return type(
                "FakeResponse",
                (),
                {
                    "is_success": True,
                    "status_code": 200,
                    "elapsed": 0.1,
                    "content_length": 7,
                    "text": "CONTENT1",
                },
            )()

        # 2. Same content.
        if self.calls == 2:

            return type(
                "FakeResponse",
                (),
                {
                    "is_success": True,
                    "status_code": 200,
                    "elapsed": 0.1,
                    "content_length": 7,
                    "text": "CONTENT1",
                },
            )()

        # 3. Changed content.
        return type(
            "FakeResponse",
            (),
            {
                "is_success": True,
                "status_code": 200,
                "elapsed": 0.1,
                "content_length": 7,
                "text": "CONTENT2",
            },
        )()


# ---------------------------------------------------------
# Monitor service
# ---------------------------------------------------------

service = MonitorService(database)

service._client = FakeClient()


# ---------------------------------------------------------
# 1. Initial ONLINE
# ---------------------------------------------------------

service.check_site(site)

row = database.history.get_last(1)

assert row is not None

print(
    "1:",
    row["status"],
    row["content_hash"],
)

assert row["status"] == Status.ONLINE.value


# ---------------------------------------------------------
# 2. Same content -> ONLINE
# ---------------------------------------------------------

service.check_site(site)

row = database.history.get_last(1)

assert row is not None

print(
    "2:",
    row["status"],
    row["content_hash"],
)

assert row["status"] == Status.ONLINE.value


# ---------------------------------------------------------
# 3. Changed content -> CHANGED
# ---------------------------------------------------------

service.check_site(site)

row = database.history.get_last(1)

assert row is not None

print(
    "3:",
    row["status"],
    row["content_hash"],
)

assert row["status"] == Status.CHANGED.value


# ---------------------------------------------------------
# Result
# ---------------------------------------------------------

print()
print("CONTENT CHANGE TEST PASSED")


database.close()