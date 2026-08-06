from __future__ import annotations

from dataclasses import dataclass

from .status import Status


@dataclass(slots=True)
class CheckResult:
    """
    Result of website check.
    """

    status: Status

    http_status: int

    elapsed: float

    content_length: int

    content_hash: str = ""

    message: str = ""

    @property
    def ok(self) -> bool:
        """
        True if website is online.
        """

        return self.status == Status.ONLINE