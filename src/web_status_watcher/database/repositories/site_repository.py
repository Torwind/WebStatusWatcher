from __future__ import annotations

import sqlite3


class SiteRepository:
    """
    Repository for sites table.
    """

    def __init__(
        self,
        connection: sqlite3.Connection,
    ) -> None:

        self._connection = connection

    def get_all(self) -> list[sqlite3.Row]:

        cursor = self._connection.execute(
            """
            SELECT *
            FROM sites
            ORDER BY id
            """
        )

        return list(cursor.fetchall())

    def get_by_id(
        self,
        site_id: int,
    ) -> sqlite3.Row | None:

        cursor = self._connection.execute(
            """
            SELECT *
            FROM sites
            WHERE id = ?
            """,
            (
                site_id,
            ),
        )

        return cursor.fetchone()