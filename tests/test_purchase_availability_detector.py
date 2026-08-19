from web_status_watcher.purchase.detector import (
    PurchaseAvailabilityDetector,
)
from web_status_watcher.purchase.status import (
    PurchaseAvailabilityStatus,
)


detector = PurchaseAvailabilityDetector()


# 1. Product can be purchased.
available_html = """
<html>
<div id="r_buy_intovar" data-id="1126">
    <button type="submit" class="btn-primary buy">
        Купити
    </button>
</div>
</html>
"""

result = detector.detect(available_html)

assert result == PurchaseAvailabilityStatus.AVAILABLE


# 2. Account has already reached the purchase limit.
limit_html = """
<html>
<p style="font-weight: bold;">
    Ви використали свій ліміт
</p>

<p>
    Ліміт продукції на одного користувача становить 1 шт.
</p>
</html>
"""

result = detector.detect(limit_html)

assert result == PurchaseAvailabilityStatus.LIMIT_REACHED


# 3. Product page exists, but purchase is unavailable.
unavailable_html = """
<html>
<div class="product">
    <span>Монета тимчасово недоступна</span>
</div>
</html>
"""

result = detector.detect(unavailable_html)

assert result == PurchaseAvailabilityStatus.NOT_AVAILABLE


# 4. Empty response.
result = detector.detect("")

assert result == PurchaseAvailabilityStatus.NOT_AVAILABLE


print("PURCHASE AVAILABILITY DETECTOR TEST PASSED")
print("AVAILABLE -> AVAILABLE")
print("LIMIT_REACHED -> LIMIT_REACHED")
print("NOT_AVAILABLE -> NOT_AVAILABLE")
print("EMPTY -> NOT_AVAILABLE")