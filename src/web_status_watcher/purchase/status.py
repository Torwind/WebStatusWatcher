"""
Purchase availability status definitions.
"""

from enum import Enum


class PurchaseAvailabilityStatus(str, Enum):
    """
    Possible purchase availability states.
    """

    AVAILABLE = "available"
    LIMIT_REACHED = "limit_reached"
    NOT_AVAILABLE = "not_available"