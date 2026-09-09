"""
Browser-based purchase cart client.
"""

from __future__ import annotations

from playwright.sync_api import (
    Browser,
    Page,
    sync_playwright,
)

from web_status_watcher.purchase.cart import (
    CartItem,
)
from web_status_watcher.purchase.target import (
    PurchaseTarget,
)


class PurchaseCartClient:
    """
    Add purchase targets to the NBU Coins cart
    through an already authenticated Chrome session.
    """

    CDP_URL = "http://127.0.0.1:9222"

    def __init__(
        self,
        playwright,
        browser: Browser,
        page: Page,
    ) -> None:
        self._playwright = playwright
        self._browser = browser
        self._page = page

    @classmethod
    def connect(
        cls,
        cdp_url: str = CDP_URL,
    ) -> "PurchaseCartClient":
        """
        Connect to an already running Chrome instance.
        """

        playwright = sync_playwright().start()

        try:
            browser = playwright.chromium.connect_over_cdp(
                cdp_url,
            )

            if not browser.contexts:
                raise RuntimeError(
                    "No browser contexts found"
                )

            context = browser.contexts[0]

            pages = [
                page
                for page in context.pages
                if "coins.bank.gov.ua" in page.url
            ]

            if not pages:
                raise RuntimeError(
                    "No coins.bank.gov.ua page found"
                )

            return cls(
                playwright=playwright,
                browser=browser,
                page=pages[0],
            )

        except Exception:
            playwright.stop()
            raise

    @property
    def page(self) -> Page:
        """
        Current browser page.
        """

        return self._page

    def _select_page(
        self,
        target: PurchaseTarget,
    ) -> Page:
        """
        Find the browser page for the target product.
        """

        product_marker = (
            f"p-{target.products_id}.html"
        )

        for page in self._page.context.pages:

            if (
                "coins.bank.gov.ua" in page.url
                and product_marker in page.url
            ):
                return page

        raise RuntimeError(
            "Product page was not found in browser: "
            f"{target.product_url}"
        )

    def _read_product_name(
        self,
    ) -> str:
        """
        Read product name from the product page.
        """

        value = self._page.locator(
            'input[name="prod_name"]'
        ).get_attribute(
            "value"
        )

        if not value:
            raise RuntimeError(
                "Product name was not found"
            )

        return value.strip()

    def _read_product_price(
        self,
    ) -> float:
        """
        Read product price from the product page.
        """

        value = self._page.locator(
            'input[name="prod_price"]'
        ).get_attribute(
            "value"
        )

        if not value:
            raise RuntimeError(
                "Product price was not found"
            )

        try:
            return float(value)
        except ValueError as exc:
            raise RuntimeError(
                f"Invalid product price: {value!r}"
            ) from exc

    def _set_quantity(
        self,
        quantity: int,
    ) -> None:
        """
        Set the requested cart quantity.

        Quantity 1 is the default and requires no UI
        interaction. Other quantities use the visible
        Selectize control.
        """

        if quantity == 1:
            return

        select = self._page.locator(
            'select[name="cart_quantity"]'
        )

        if select.count() == 0:
            raise RuntimeError(
                "Quantity selector not found"
            )

        options = select.locator(
            "option"
        )

        available = []

        for index in range(
            options.count()
        ):

            value = options.nth(
                index
            ).get_attribute(
                "value"
            )

            if value:

                try:
                    available.append(
                        int(value)
                    )
                except ValueError:
                    pass

        if quantity not in available:
            raise ValueError(
                f"Quantity {quantity} is not available; "
                f"available={available}"
            )

        # The original <select> is hidden by Selectize.
        # Work with the visible Selectize control instead.
        control = select.locator(
            "xpath=following-sibling::div[contains(@class, 'selectize-control')]"
        )

        if control.count() == 0:
            control = self._page.locator(
                ".selectize-control"
            )

        if control.count() == 0:
            raise RuntimeError(
                "Visible Selectize quantity control "
                "was not found"
            )

        control.first.click()

        option = self._page.locator(
            ".selectize-dropdown .option"
        ).filter(
            has_text=str(quantity),
        )

        if option.count() == 0:
            raise RuntimeError(
                f"Quantity option {quantity} not found"
            )

        option.first.click()

    def _is_in_cart(
        self,
    ) -> bool:
        """
        Check whether the product page indicates
        that the product is already in the cart.
        """

        block = self._page.locator(
            "#r_buy_intovar"
        )

        if block.count() != 1:
            return False

        link = block.locator(
            'a[href="shopping_cart.php"]'
        )

        if link.count() == 0:
            return False

        text = (
            link.first
            .inner_text()
            .strip()
            .upper()
        )

        return text == "В КОШИКУ"

    def add_to_cart(
        self,
        target: PurchaseTarget,
    ) -> CartItem:
        """
        Add the requested product to the cart.

        The operation is performed through the normal
        browser UI in an authenticated session.
        """

        if not target.enabled:
            raise ValueError(
                "Purchase target is disabled"
            )

        if target.products_id <= 0:
            raise ValueError(
                "products_id must be greater than zero"
            )

        if target.quantity <= 0:
            raise ValueError(
                "quantity must be greater than zero"
            )

        self._page = self._select_page(
            target,
        )

        name = self._read_product_name()
        price = self._read_product_price()

        # Do not add the product again if the page already
        # indicates that it is in the cart.
        if self._is_in_cart():
            return CartItem(
                products_id=target.products_id,
                quantity=target.quantity,
                name=name,
                price=price,
            )

        self._set_quantity(
            target.quantity,
        )

        button = self._page.locator(
            "#r_buy_intovar .btn-primary.buy"
        )

        if button.count() != 1:
            raise RuntimeError(
                "Purchase button was not found"
            )

        if not button.is_visible():
            raise RuntimeError(
                "Purchase button is not visible"
            )

        if not button.is_enabled():
            raise RuntimeError(
                "Purchase button is disabled"
            )

        button.click(
            no_wait_after=True,
        )

        # The site performs several asynchronous operations:
        #
        # prepare_buy
        # user_actions_ajax.php
        # add_product
        #
        # We do not rely on add_product.status because
        # the real site has returned status=0 even though
        # the product was successfully added.

        self._page.wait_for_function(
            """
            () => {
                const block =
                    document.querySelector(
                        "#r_buy_intovar"
                    );

                if (!block) {
                    return false;
                }

                const link =
                    block.querySelector(
                        'a[href="shopping_cart.php"]'
                    );

                if (!link) {
                    return false;
                }

                return (
                    link.textContent
                        .trim()
                        .toUpperCase()
                    === "В КОШИКУ"
                );
            }
            """,
            timeout=15000,
        )

        if not self._is_in_cart():
            raise RuntimeError(
                "Product was not confirmed in cart"
            )

        return CartItem(
            products_id=target.products_id,
            quantity=target.quantity,
            name=name,
            price=price,
        )

    def close(self) -> None:
        """
        Close the Playwright connection.
        """

        try:
            self._browser.close()
        finally:
            self._playwright.stop()