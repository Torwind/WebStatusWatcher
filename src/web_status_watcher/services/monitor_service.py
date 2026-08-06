from __future__ import annotations

import time
from sqlite3 import Row

from web_status_watcher.database import Database
from web_status_watcher.logging import get_logger
from web_status_watcher.network import HttpClient


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

            last = self._last_check.get(site_id, 0)

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

        self._database.history.add(
            site_id=site["id"],
            status_code=response.status_code,
            elapsed=response.elapsed,
            content_length=response.content_length,
        )

        self._logger.info(
            "%s OK (%d) %.3fs %d bytes",
            site["name"],
            response.status_code,
            response.elapsed,
            response.content_length,
        )