from __future__ import annotations

import sqlite3
from pathlib import Path

from .schema import SCHEMA
from .repositories import (
    SiteRepository,
    HistoryRepository,
)


class Database:
    """
    SQLite database wrapper.
    """

    def __init__(self, db_path: Path):

        self._db_path = db_path

        self._connection: sqlite3.Connection | None = None

        self.sites: SiteRepository | None = None

        self.history: HistoryRepository | None = None

    @property
    def connection(self) -> sqlite3.Connection:

        if self._connection is None:

            self.connect()

        assert self._connection is not None

        return self._connection

    def connect(self) -> None:

        if self._connection is not None:
            return

        self._db_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._connection = sqlite3.connect(
            self._db_path,
            check_same_thread=False,
        )

        self._connection.row_factory = sqlite3.Row

        self._connection.execute(
            "PRAGMA foreign_keys = ON;"
        )

        self._connection.executescript(
            SCHEMA
        )

        self.sites = SiteRepository(
            self._connection
        )

        self.history = HistoryRepository(
            self._connection
        )

    def close(self) -> None:

        if self._connection is not None:

            self._connection.close()

            self._connection = None

            self.sites = None

            self.history = None

    def execute(
        self,
        sql: str,
        parameters: tuple = (),
    ) -> sqlite3.Cursor:

        cursor = self.connection.execute(
            sql,
            parameters,
        )

        self.connection.commit()

        return cursor

    def executescript(
        self,
        script: str,
    ) -> None:

        self.connection.executescript(
            script
        )

        self.connection.commit()