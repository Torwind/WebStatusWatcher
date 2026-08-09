"""
Purchase product availability checking.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AvailabilityResult:
    """
    Result of a product availability check.
    """

    available: bool
    products_id: int
    cid: int
    status_code: int
    message: str = ""