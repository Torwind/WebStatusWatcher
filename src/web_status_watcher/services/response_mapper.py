from __future__ import annotations

from web_status_watcher.fingerprint import FingerprintHasher
from web_status_watcher.network.response import HttpResponse
from web_status_watcher.status import (
    CheckResult,
    Status,
)


class ResponseMapper:
    """
    Convert HttpResponse to CheckResult.
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