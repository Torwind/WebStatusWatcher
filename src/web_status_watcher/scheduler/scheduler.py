from __future__ import annotations

import threading
import time
import traceback

from .worker import Worker


class Scheduler:
    """
    Simple scheduler.

    The scheduler checks registered workers every 0.25 seconds.
    Each worker controls its own execution interval.
    """

    TICK_INTERVAL = 0.25
    STARTUP_DELAY = 1.0

    def __init__(self) -> None:
        self._workers: list[Worker] = []
        self._running = False
        self._thread: threading.Thread | None = None

    def add_worker(
        self,
        worker: Worker,
    ) -> None:
        """
        Register worker.
        """

        self._workers.append(
            worker,
        )

    def start(self) -> None:
        """
        Start scheduler thread.
        """

        if self._running:
            return

        self._running = True

        self._thread = threading.Thread(
            target=self._run,
            name="Scheduler",
            daemon=True,
        )

        self._thread.start()

    def stop(self) -> None:
        """
        Stop scheduler.
        """

        self._running = False

        if self._thread is not None:
            self._thread.join()
            self._thread = None

    def _run(self) -> None:
        """
        Scheduler loop.
        """

        print(
            "Scheduler started"
        )

        time.sleep(
            self.STARTUP_DELAY
        )

        while self._running:

            print(
                f"[{time.strftime('%H:%M:%S')}] Tick"
            )

            for worker in self._workers:

                try:

                    print(
                        f" -> {worker.name}"
                    )

                    worker.tick()

                except Exception:

                    print(
                        "Worker crashed:"
                    )

                    traceback.print_exc()

            time.sleep(
                self.TICK_INTERVAL
            )

        print(
            "Scheduler stopped"
        )
