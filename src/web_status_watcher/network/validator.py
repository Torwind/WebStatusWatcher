from __future__ import annotations

from urllib.parse import urlparse

from .exceptions import InvalidUrlError


def validate_url(url: str) -> str:
    """
    Validate HTTP/HTTPS URL.
    """

    if not url:
        raise InvalidUrlError("URL is empty.")

    url = url.strip()

    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise InvalidUrlError(
            "Only HTTP and HTTPS are supported."
        )

    if not parsed.netloc:
        raise InvalidUrlError(
            "Invalid URL."
        )

    return url