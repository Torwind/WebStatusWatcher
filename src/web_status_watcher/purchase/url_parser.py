"""
Product URL parser for the NBU Coins website.
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse
import re


@dataclass(frozen=True, slots=True)
class ProductUrl:
    """
    Parsed product URL information.
    """

    url: str
    products_id: int
    cid: int


class ProductUrlParser:
    """
    Parse product URLs from coins.bank.gov.ua.
    """

    _PRODUCT_ID_PATTERN = re.compile(
        r"/p-(\d+)\.html$",
        re.IGNORECASE,
    )

    _ALLOWED_HOST = "coins.bank.gov.ua"

    @classmethod
    def parse(cls, url: str) -> ProductUrl:
        """
        Parse and validate a product URL.

        Example:
            https://coins.bank.gov.ua/arhistratig-mihajil-c-/p-1126.html?cid=14348
        """

        if not isinstance(url, str) or not url.strip():
            raise ValueError("Product URL must not be empty")

        url = url.strip()

        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            raise ValueError(
                "Product URL must use HTTP or HTTPS"
            )

        if parsed.netloc.lower() != cls._ALLOWED_HOST:
            raise ValueError(
                "Product URL must belong to coins.bank.gov.ua"
            )

        match = cls._PRODUCT_ID_PATTERN.search(
            parsed.path
        )

        if match is None:
            raise ValueError(
                "Product URL must contain /p-<products_id>.html"
            )

        products_id = int(match.group(1))

        query = parse_qs(
            parsed.query,
            keep_blank_values=True,
        )

        cid_values = query.get("cid")

        if not cid_values or not cid_values[0]:
            raise ValueError(
                "Product URL must contain cid"
            )

        try:
            cid = int(cid_values[0])
        except ValueError as exc:
            raise ValueError(
                "cid must be an integer"
            ) from exc

        if products_id <= 0:
            raise ValueError(
                "products_id must be positive"
            )

        if cid <= 0:
            raise ValueError(
                "cid must be positive"
            )

        return ProductUrl(
            url=url,
            products_id=products_id,
            cid=cid,
        )