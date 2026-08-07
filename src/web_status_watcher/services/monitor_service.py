from __future__ import annotations

import time
from sqlite3 import Row

from web_status_watcher.database import Database
from web_status_watcher.logging import get_logger
from web_status_watcher.network import HttpClient
from web_status_watcher.services.response_mapper import ResponseMapper


class MonitorService:
    """
    Website monitoring service.
    """

    def __init__(
        self,
        database: Database,
    ) -> None:

        self._database = database
        self._client = HttpClient()
        self._logger = get_logger()

        self._last_check: dict[int, float] = {}

    def tick(self) -> None:
        """
        Called every second by Scheduler.
        """

        assert self._database.sites is not None

        now = time.time()

        for site in self._database.sites.get_all():

            site_id = site["id"]

            interval = site["interval_seconds"]

            last = self._last_check.get(
                site_id,
                0,
            )

            if now - last >= interval:

                self._last_check[site_id] = now

                self.check_site(site)

    def check_site(
        self,
        site: Row,
    ) -> None:

        assert self._database.history is not None

        self._logger.info(
            "Checking %s",
            site["name"],
        )

        response = self._client.get(
            site["url"],
        )

        result = ResponseMapper.map(
            response,
        )

        previous = self._database.history.get_last(
            site["id"],
        )

        changed = False

        if (
            previous is not None
            and previous["content_hash"]
            and previous["content_hash"] != result.content_hash
        ):
            changed = True

        self._database.history.add(
            site_id=site["id"],
            status_code=result.http_status,
            elapsed=result.elapsed,
            content_length=result.content_length,
            content_hash=result.content_hash,
        )

        if changed:

            self._logger.warning(
                "%s CONTENT CHANGED",
                site["name"],
            )

        self._logger.info(
            "%s %s (%d) %.3fs %d bytes",
            site["name"],
            result.status.value,
            result.http_status,
            result.elapsed,
            result.content_length,
        )