from __future__ import annotations

from enum import Enum


class Status(str, Enum):
    """
    Website status.
    """

    ONLINE = "ONLINE"

    OFFLINE = "OFFLINE"

    TIMEOUT = "TIMEOUT"

    DNS_ERROR = "DNS_ERROR"

    SSL_ERROR = "SSL_ERROR"

    HTTP_ERROR = "HTTP_ERROR"

    CHANGED = "CHANGED"

    UNKNOWN = "UNKNOWN"