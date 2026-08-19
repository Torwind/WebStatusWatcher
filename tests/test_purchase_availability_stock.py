from web_status_watcher.purchase.detector import PurchaseAvailabilityDetector
from web_status_watcher.purchase.status import PurchaseAvailabilityStatus

PRODUCT_HTML = """

<html>
<head>
<title>"30 років Конституції України" (c) - Архів</title>
</head>
<body>

<div class="prod_buy_btns">
    <input type="hidden" name="products_id" value="1205">
</div>

<p class="p-info-climit">
    Вам доступно для придбання ще <span>1</span> шт.
</p>

<p>
    Ліміт продукції на одного користувача становить 1 шт.
</p>

<p>
    На складі залишилося всього
    <span class="pd_qty">0</span> шт.
</p>

</body>
</html>
"""

detector = PurchaseAvailabilityDetector()

result = detector.detect(PRODUCT_HTML)

assert result == PurchaseAvailabilityStatus.NOT_AVAILABLE

print("PURCHASE AVAILABILITY STOCK TEST PASSED")
print("products_id=1205")
print("pd_qty=0")
print("status={}".format(result.name))
