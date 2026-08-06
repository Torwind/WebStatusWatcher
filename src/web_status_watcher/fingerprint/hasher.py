from __future__ import annotations

import hashlib


class FingerprintHasher:
    """
    HTML fingerprint generator.
    """

    @staticmethod
    def sha256(
        text: str,
    ) -> str:
        """
        Calculate SHA256 hash.
        """

        return hashlib.sha256(
            text.encode("utf-8"),
        ).hexdigest()