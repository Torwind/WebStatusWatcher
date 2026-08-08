from __future__ import annotations

import time
from sqlite3 import Row

from web_status_watcher.database import Database
from web_status_watcher.logging import get_logger
from web_status_watcher.network import HttpClient
from web_status_watcher.network.exceptions import (
    HttpRequestError,
    TimeoutError,
)
from web_status_watcher.services.response_mapper import ResponseMapper
from web_status_watcher.status import Status


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
        """
        Check one website.
        """

        assert self._database.history is not None

        self._logger.info(
            "Checking %s",
            site["name"],
        )

        try:

            response = self._client.get(
                site["url"],
            )

            result = ResponseMapper.map(
                response,
            )

        except TimeoutError as exc:

            result = ResponseMapper.error(
                Status.TIMEOUT,
                str(exc),
            )

        except HttpRequestError as exc:

            result = ResponseMapper.error(
                Status.OFFLINE,
                str(exc),
            )

        self._save_result(
            site,
            result,
        )

    def _save_result(
        self,
        site: Row,
        result,
    ) -> None:
        """
        Process and save monitoring result.
        """

        assert self._database.history is not None

        # Last record is used for availability transitions.
        previous = self._database.history.get_last(
            site["id"],
        )

        previous_status: str | None = None

        if previous is not None:
            previous_status = previous["status"]

        # Detect availability transition.
        self._detect_transition(
            site,
            previous_status,
            result.status,
        )

        # Last ONLINE record is used for content comparison.
        previous_online = self._database.history.get_last_online(
            site["id"],
        )

        # Detect content change.
        self._detect_content_change(
            site,
            previous_online,
            result,
        )

        # Save result.
        self._database.history.add(
            site_id=site["id"],
            status_code=result.http_status,
            elapsed=result.elapsed,
            content_length=result.content_length,
            content_hash=result.content_hash,
            status=result.status.value,
            message=result.message,
        )

        # Log final result.
        self._log_result(
            site,
            result,
        )

    def _detect_transition(
        self,
        site: Row,
        previous_status: str | None,
        current_status: Status,
    ) -> None:
        """
        Detect availability state transitions.
        """

        if previous_status is None:
            return

        # ONLINE -> OFFLINE/TIMEOUT
        if (
            previous_status == Status.ONLINE.value
            and current_status in (
                Status.OFFLINE,
                Status.TIMEOUT,
            )
        ):
            self._logger.warning(
                "%s DOWN: %s -> %s",
                site["name"],
                previous_status,
                current_status.value,
            )

        # OFFLINE/TIMEOUT -> ONLINE
        elif (
            previous_status in (
                Status.OFFLINE.value,
                Status.TIMEOUT.value,
            )
            and current_status == Status.ONLINE
        ):
            self._logger.info(
                "%s RECOVERY: %s -> ONLINE",
                site["name"],
                previous_status,
            )

    def _detect_content_change(
        self,
        site: Row,
        previous_online: Row | None,
        result,
    ) -> None:
        """
        Detect content fingerprint changes.

        Only successful ONLINE responses participate
        in content comparison. Network errors and HTTP
        errors are ignored for fingerprint comparison.
        """

        if result.status != Status.ONLINE:
            return

        if previous_online is None:
            return

        previous_hash = previous_online["content_hash"]

        if not previous_hash:
            return

        if previous_hash == result.content_hash:
            return

        result.status = Status.CHANGED

        self._logger.warning(
            "%s CONTENT CHANGED",
            site["name"],
        )

    def _log_result(
        self,
        site: Row,
        result,
    ) -> None:
        """
        Log final monitoring result.
        """

        if result.status == Status.ONLINE:

            self._logger.info(
                "%s ONLINE (%d) %.3fs %d bytes",
                site["name"],
                result.http_status,
                result.elapsed,
                result.content_length,
            )

        elif result.status == Status.CHANGED:

            self._logger.warning(
                "%s CHANGED (%d) %.3fs %d bytes",
                site["name"],
                result.http_status,
                result.elapsed,
                result.content_length,
            )

        else:

            self._logger.error(
                "%s %s: %s",
                site["name"],
                result.status.value,
                result.message,
            )