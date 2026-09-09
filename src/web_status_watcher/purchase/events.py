"""
Purchase availability events.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PurchaseAvailableEvent:
    """
    Event emitted when a purchase target becomes available.
    """

    products_id: int
    cid: int