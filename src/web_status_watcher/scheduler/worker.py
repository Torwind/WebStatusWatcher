from __future__ import annotations

import time
from typing import Callable


class Worker:
    """
    Scheduled task.
    """

    def __init__(
        self,
        name: str,
        interval: float,
        callback: Callable,
    ) -> None:

        if interval <= 0:
            raise ValueError(
                "Worker interval must be greater than zero"
            )

        self.name = name
        self.interval = interval
        self.callback = callback
        self.elapsed = 0.0
        self.running = True

        self._last_run: float | None = None

    def tick(self) -> None:
        """
        Execute the callback when the worker interval has elapsed.
        """

        if not self.running:
            return

        now = time.monotonic()

        if self._last_run is None:

            self._last_run = now

            self.callback()

            return

        elapsed = now - self._last_run

        if elapsed < self.interval:
            return

        self._last_run = now
        self.elapsed = elapsed

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
        self._last_run = None
        self.elapsed = 0.0