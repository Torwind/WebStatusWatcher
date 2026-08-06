"""
Network layer.

Provides HTTP client abstractions used by WebStatusWatcher.
"""

from .client import HttpClient
from .response import HttpResponse
from .exceptions import (
    NetworkError,
    InvalidUrlError,
    TimeoutError,
)

__all__ = [
    "HttpClient",
    "HttpResponse",
    "NetworkError",
    "InvalidUrlError",
    "TimeoutError",
]