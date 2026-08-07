from __future__ import annotations

import time
from collections.abc import Callable
from typing import TypeVar

from .exceptions import (
    HttpRequestError,
    TimeoutError,
)


T = TypeVar("T")


class RetryEngine:
    """
    Retry failed network operations.
    """

    def __init__(
        self,
        attempts: int = 3,
        delay: float = 1.0,
    ) -> None:

        if attempts < 1:
            raise ValueError(
                "attempts must be greater than or equal to 1"
            )

        if delay < 0:
            raise ValueError(
                "delay must not be negative"
            )

        self._attempts = attempts
        self._delay = delay

    @property
    def attempts(self) -> int:
        return self._attempts

    @property
    def delay(self) -> float:
        return self._delay

    def execute(
        self,
        operation: Callable[[], T],
    ) -> T:
        """
        Execute operation with retries.

        The first attempt is the original request.
        Additional attempts are performed only after
        TimeoutError or HttpRequestError.
        """

        last_error: Exception | None = None

        for attempt in range(
            1,
            self._attempts + 1,
        ):

            try:

                return operation()

            except (
                TimeoutError,
                HttpRequestError,
            ) as exc:

                last_error = exc

                if attempt >= self._attempts:
                    raise

                if self._delay > 0:
                    time.sleep(self._delay)

        assert last_error is not None

        raise last_error