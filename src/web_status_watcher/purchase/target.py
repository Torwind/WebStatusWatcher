"""
Purchase target model.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PurchaseTarget:
    """
    Target product for the purchase workflow.
    """

    product_url: str
    products_id: int
    quantity: int = 1
    enabled: bool = True

    def __post_init__(self) -> None:
        if not self.enabled:
            return

        if not self.product_url:
            raise ValueError(
                "product_url must not be empty"
            )

        if self.products_id <= 0:
            raise ValueError(
                "products_id must be greater than zero"
            )

        if self.quantity <= 0:
            raise ValueError(
                "quantity must be greater than zero"
            )