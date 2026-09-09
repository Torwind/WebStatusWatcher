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
        self.running = True

    def tick(self) -> None:
        """
        Execute task when the worker is running.
        """

        if not self.running:
            return

        self.callback()

    def stop(self) -> None:
        """
        Stop scheduled task execution.
        """

        self.running = False

    def start(self) -> None:
        """
        Resume scheduled task execution.
        """

        self.running = True