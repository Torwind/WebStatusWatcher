"""
Network exceptions.
"""


class NetworkError(Exception):
    """
    Base network exception.
    """


class InvalidUrlError(NetworkError):
    """
    Invalid URL.
    """


class TimeoutError(NetworkError):
    """
    HTTP timeout.
    """


class HttpRequestError(NetworkError):
    """
    Request failed.
    """