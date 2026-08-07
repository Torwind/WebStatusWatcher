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

        self._ensure_columns()

    def _ensure_columns(self) -> None:
        """
        Ensure history table contains all required columns.
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

        changed = False

        if "content_hash" not in column_names:

            self._connection.execute(
                """
                ALTER TABLE history
                ADD COLUMN content_hash TEXT NOT NULL DEFAULT ''
                """
            )

            changed = True

        if "status" not in column_names:

            self._connection.execute(
                """
                ALTER TABLE history
                ADD COLUMN status TEXT NOT NULL DEFAULT 'UNKNOWN'
                """
            )

            changed = True

        if "message" not in column_names:

            self._connection.execute(
                """
                ALTER TABLE history
                ADD COLUMN message TEXT NOT NULL DEFAULT ''
                """
            )

            changed = True

        if changed:
            self._connection.commit()

    def add(
        self,
        site_id: int,
        status_code: int,
        elapsed: float,
        content_length: int,
        content_hash: str = "",
        status: str = "UNKNOWN",
        message: str = "",
    ) -> None:

        self._connection.execute(
            """
            INSERT INTO history
            (
                site_id,
                status_code,
                elapsed,
                content_length,
                content_hash,
                status,
                message
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                site_id,
                status_code,
                elapsed,
                content_length,
                content_hash,
                status,
                message,
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