"""
Purchase cart response handling.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class CartItem:
    """
    Item confirmed in the purchase cart.
    """

    products_id: int
    quantity: int
    name: str
    price: float


class CartResponseError(ValueError):
    """
    Invalid cart response.
    """


def parse_cart_response(
    data: dict[str, Any],
) -> CartItem | None:
    """
    Parse add/check-cart response.

    Returns CartItem when the requested product is present.
    Returns None when the response indicates an empty cart
    or no product item.
    """

    if not isinstance(data, dict):
        raise CartResponseError(
            "Cart response must be a JSON object"
        )

    if data.get("success") is not True:
        return None

    status = data.get("status")

    if status != 1:
        return None

    product_id = data.get("id")

    if product_id is None:
        raise CartResponseError(
            "Cart response does not contain product id"
        )

    try:
        products_id = int(product_id)
    except (TypeError, ValueError) as exc:
        raise CartResponseError(
            "Invalid product id in cart response"
        ) from exc

    try:
        quantity = int(
            data.get(
                "quantity",
                0,
            )
        )
    except (TypeError, ValueError) as exc:
        raise CartResponseError(
            "Invalid quantity in cart response"
        ) from exc

    if quantity <= 0:
        raise CartResponseError(
            "Cart quantity must be greater than zero"
        )

    try:
        price = float(
            data.get(
                "price",
                0,
            )
        )
    except (TypeError, ValueError) as exc:
        raise CartResponseError(
            "Invalid price in cart response"
        ) from exc

    return CartItem(
        products_id=products_id,
        quantity=quantity,
        name=str(
            data.get(
                "name",
                "",
            )
        ),
        price=price,
    )