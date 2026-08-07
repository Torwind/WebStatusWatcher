"""
Network layer.

Provides HTTP client abstractions used by WebStatusWatcher.
"""

from .client import HttpClient
from .exceptions import (
    HttpRequestError,
    InvalidUrlError,
    NetworkError,
    TimeoutError,
)
from .response import HttpResponse
from .retry import RetryEngine

__all__ = [
    "HttpClient",
    "HttpResponse",
    "RetryEngine",
    "NetworkError",
    "InvalidUrlError",
    "TimeoutError",
    "HttpRequestError",
]