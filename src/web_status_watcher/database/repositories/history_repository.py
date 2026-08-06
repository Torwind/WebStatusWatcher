from __future__ import annotations

import sqlite3


class HistoryRepository:
    """
    Repository for history table.
    """

    def __init__(
        self,
        connection: sqlite3.Connection,
    ) -> None:

        self._connection = connection

    def add(
        self,
        site_id: int,
        status_code: int,
        elapsed: float,
        content_length: int,
    ) -> None:

        self._connection.execute(
            """
            INSERT INTO history
            (
                site_id,
                status_code,
                elapsed,
                content_length
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                site_id,
                status_code,
                elapsed,
                content_length,
            ),
        )

        self._connection.commit()