from __future__ import annotations

from .database import Database
from .migrations import SCHEMA


class Repository:
    """
    High level database API.
    """

    def __init__(self, database: Database):

        self.database = database

        self.initialize()

    def initialize(self) -> None:

        self.database.executescript(
            SCHEMA
        )

    def add_site(
        self,
        name: str,
        url: str,
        interval: int = 30,
    ) -> None:

        self.database.execute(
            """
            INSERT INTO sites
            (
                name,
                url,
                interval_seconds
            )
            VALUES
            (
                ?,
                ?,
                ?
            )
            """,
            (
                name,
                url,
                interval,
            ),
        )

    def get_sites(self):

        cursor = self.database.execute(
            """
            SELECT *
            FROM sites
            ORDER BY id
            """
        )

        return cursor.fetchall()