from __future__ import annotations

from pathlib import Path

from web_status_watcher.database import Database
from web_status_watcher.network.response import HttpResponse
from web_status_watcher.services.monitor_service import MonitorService
from web_status_watcher.status import Status

TEST_DB = Path("data/test_http_error_transition.db")

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
        "HTTP Error Transition Test",
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

    def get(self, url: str) -> HttpResponse:
        self.calls += 1

        # 1. ONLINE
        if self.calls == 1:
            return HttpResponse(
                url=url,
                status_code=200,
                text="TEST",
                elapsed=0.1,
                ok=True,
                headers={},
            )

        # 2. HTTP ERROR
        if self.calls == 2:
            return HttpResponse(
                url=url,
                status_code=500,
                text="Internal Server Error",
                elapsed=0.1,
                ok=False,
                headers={},
            )

        # 3. ONLINE / RECOVERY
        return HttpResponse(
            url=url,
            status_code=200,
            text="TEST",
            elapsed=0.1,
            ok=True,
            headers={},
        )


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
    row["status_code"],
    row["message"],
)

assert row["status"] == Status.ONLINE.value
assert row["status_code"] == 200


# ---------------------------------------------------------
# 2. HTTP ERROR
# ---------------------------------------------------------

service.check_site(site)

row = database.history.get_last(1)

assert row is not None

print(
    "2:",
    row["status"],
    row["status_code"],
    row["message"],
)

assert row["status"] == Status.HTTP_ERROR.value
assert row["status_code"] == 500


# ---------------------------------------------------------
# 3. ONLINE / RECOVERY
# ---------------------------------------------------------

service.check_site(site)

row = database.history.get_last(1)

assert row is not None

print(
    "3:",
    row["status"],
    row["status_code"],
    row["message"],
)

assert row["status"] == Status.ONLINE.value
assert row["status_code"] == 200


# ---------------------------------------------------------
# Result
# ---------------------------------------------------------

print()
print("HTTP ERROR TRANSITION TEST PASSED")

database.close()