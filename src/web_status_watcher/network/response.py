from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class HttpResponse:
    """
    Normalized HTTP response.

    This object isolates the rest of the application from the
    concrete HTTP library (httpx).
    """

    url: str
    status_code: int
    text: str
    elapsed: float
    ok: bool
    headers: dict[str, str]

    @property
    def is_success(self) -> bool:
        """
        True if response status is 2xx.
        """

        return 200 <= self.status_code < 300

    @property
    def content_length(self) -> int:
        """
        Length of received text.
        """

        return len(self.text)

    def __str__(self) -> str:
        return (
            f"HttpResponse("
            f"status={self.status_code}, "
            f"elapsed={self.elapsed:.3f}s)"
        )