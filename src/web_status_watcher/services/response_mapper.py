from __future__ import annotations

from web_status_watcher.fingerprint import FingerprintHasher
from web_status_watcher.network.response import HttpResponse
from web_status_watcher.status import (
    CheckResult,
    Status,
)


class ResponseMapper:
    """
    Convert HTTP response to CheckResult.
    """

    @staticmethod
    def map(
        response: HttpResponse,
    ) -> CheckResult:

        if response.is_success:

            status = Status.ONLINE

        else:

            status = Status.HTTP_ERROR

        return CheckResult(
            status=status,
            http_status=response.status_code,
            elapsed=response.elapsed,
            content_length=response.content_length,
            content_hash=FingerprintHasher.sha256(
                response.text,
            ),
        )

    @staticmethod
    def error(
        status: Status,
        message: str,
    ) -> CheckResult:
        """
        Create CheckResult for a failed network request.
        """

        return CheckResult(
            status=status,
            http_status=0,
            elapsed=0.0,
            content_length=0,
            content_hash="",
            message=message,
        )