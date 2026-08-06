from __future__ import annotations

import threading
import time
import traceback

from .worker import Worker


class Scheduler:
    """
    Simple scheduler.

    Executes every registered worker once per second.
    Each worker decides internally whether it should
    perform its work.
    """

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

        self._workers.append(worker)

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

        print("Scheduler started")

        while self._running:

            time.sleep(1)

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

        print("Scheduler stopped")