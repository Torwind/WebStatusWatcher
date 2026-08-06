from __future__ import annotations

from typing import Callable


class Worker:
    """
    Scheduled task.
    """

    def __init__(
        self,
        name: str,
        interval: int,
        callback: Callable,
    ) -> None:

        self.name = name
        self.interval = interval
        self.callback = callback
        self.elapsed = 0

    def tick(self) -> None:
        """
        Execute task.
        """

        self.callback()