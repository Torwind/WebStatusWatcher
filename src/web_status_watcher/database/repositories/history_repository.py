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

        self._ensure_content_hash()

    def _ensure_content_hash(self) -> None:
        """
        Ensure history table contains content_hash column.
        """

        columns = self._connection.execute(
            """
            PRAGMA table_info(history)
            """
        ).fetchall()

        column_names = {
            column["name"]
            for column in columns
        }

        if "content_hash" not in column_names:

            self._connection.execute(
                """
                ALTER TABLE history
                ADD COLUMN content_hash TEXT NOT NULL DEFAULT ''
                """
            )

            self._connection.commit()

    def add(
        self,
        site_id: int,
        status_code: int,
        elapsed: float,
        content_length: int,
        content_hash: str = "",
    ) -> None:

        self._connection.execute(
            """
            INSERT INTO history
            (
                site_id,
                status_code,
                elapsed,
                content_length,
                content_hash
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                site_id,
                status_code,
                elapsed,
                content_length,
                content_hash,
            ),
        )

        self._connection.commit()

    def get_last(
        self,
        site_id: int,
    ) -> sqlite3.Row | None:
        """
        Return the latest history record for a site.
        """

        cursor = self._connection.execute(
            """
            SELECT *
            FROM history
            WHERE site_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (
                site_id,
            ),
        )

        return cursor.fetchone()