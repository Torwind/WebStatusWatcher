from __future__ import annotations

from pathlib import Path

from web_status_watcher.database import Database
from web_status_watcher.network.exceptions import TimeoutError
from web_status_watcher.services.monitor_service import MonitorService
from web_status_watcher.status import Status


TEST_DB = Path("data/test_timeout_transition.db")

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
        "Timeout Transition Test",
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

        # 1. ONLINE
        if self.calls == 1:

            return type(
                "FakeResponse",
                (),
                {
                    "is_success": True,
                    "status_code": 200,
                    "elapsed": 0.1,
                    "content_length": 100,
                    "text": "ONLINE",
                },
            )()

        # 2. TIMEOUT
        if self.calls == 2:

            raise TimeoutError(
                "Request timeout"
            )

        # 3. ONLINE / RECOVERY
        return type(
            "FakeResponse",
            (),
            {
                "is_success": True,
                "status_code": 200,
                "elapsed": 0.1,
                "content_length": 100,
                "text": "ONLINE",
            },
        )()


# ---------------------------------------------------------
# Monitor service
# ---------------------------------------------------------

service = MonitorService(database)

service._client = FakeClient()


# ---------------------------------------------------------
# 1. ONLINE
# ---------------------------------------------------------

service.check_site(site)

row = database.history.get_last(1)

assert row is not None

print(
    "1:",
    row["status"],
    row["message"],
)

assert row["status"] == Status.ONLINE.value


# ---------------------------------------------------------
# 2. TIMEOUT
# ---------------------------------------------------------

service.check_site(site)

row = database.history.get_last(1)

assert row is not None

print(
    "2:",
    row["status"],
    row["message"],
)

assert row["status"] == Status.TIMEOUT.value

assert row["message"] == "Request timeout"


# ---------------------------------------------------------
# 3. ONLINE / RECOVERY
# ---------------------------------------------------------

service.check_site(site)

row = database.history.get_last(1)

assert row is not None

print(
    "3:",
    row["status"],
    row["message"],
)

assert row["status"] == Status.ONLINE.value


# ---------------------------------------------------------
# Result
# ---------------------------------------------------------

print()
print("TIMEOUT TRANSITION TEST PASSED")

database.close()