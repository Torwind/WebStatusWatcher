from __future__ import annotations

import time

import httpx

from .exceptions import (
    HttpRequestError,
    TimeoutError,
)
from .headers import DEFAULT_HEADERS
from .response import HttpResponse
from .retry import RetryEngine
from .user_agent import APP_USER_AGENT
from .validator import validate_url


class HttpClient:
    """
    HTTP client based on httpx.
    """

    def __init__(
        self,
        timeout: float = 15.0,
        follow_redirects: bool = True,
        verify_ssl: bool = True,
        retry_attempts: int = 3,
        retry_delay: float = 1.0,
    ) -> None:

        self._timeout = timeout

        headers = DEFAULT_HEADERS.copy()
        headers["User-Agent"] = APP_USER_AGENT

        self._client = httpx.Client(
            timeout=timeout,
            headers=headers,
            follow_redirects=follow_redirects,
            verify=verify_ssl,
        )

        self._retry = RetryEngine(
            attempts=retry_attempts,
            delay=retry_delay,
        )

    @property
    def timeout(self) -> float:
        """
        Current timeout.
        """

        return self._timeout

    def close(self) -> None:
        """
        Close underlying HTTP session.
        """

        self._client.close()

    def __enter__(self) -> "HttpClient":
        return self

    def __exit__(
        self,
        exc_type,
        exc,
        tb,
    ) -> None:

        self.close()

    def get(
        self,
        url: str,
    ) -> HttpResponse:

        return self._request(
            "GET",
            url,
        )

    def post(
        self,
        url: str,
        data: dict | None = None,
    ) -> HttpResponse:

        return self._request(
            "POST",
            url,
            data=data,
        )

    def _request(
        self,
        method: str,
        url: str,
        **kwargs,
    ) -> HttpResponse:
        """
        Execute HTTP request with retry support.
        """

        url = validate_url(url)

        def operation() -> HttpResponse:

            started = time.perf_counter()

            try:

                response = self._client.request(
                    method=method,
                    url=url,
                    **kwargs,
                )

            except httpx.TimeoutException as exc:

                raise TimeoutError(
                    f"Request timeout: {url}"
                ) from exc

            except httpx.HTTPError as exc:

                raise HttpRequestError(
                    str(exc)
                ) from exc

            elapsed = time.perf_counter() - started

            return HttpResponse(
                url=str(response.url),
                status_code=response.status_code,
                text=response.text,
                elapsed=elapsed,
                ok=response.is_success,
                headers=dict(response.headers),
            )

        return self._retry.execute(
            operation,
        )

    def __del__(self) -> None:
        """
        Ensure HTTP session is closed.
        """

        try:
            self.close()
        except Exception:
            pass