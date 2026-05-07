"""
Bölüm 05 — İyi Test vs Kötü Test
Karşılaştırmalı test örnekleri.
"""

import pytest
from cart import Cart, Product


# ============================================================
# ❌ KÖTÜ TESTLER — Bunları YAZMAYIN
# ============================================================

# ❌ Kötü: 3 davranışı birden test ediyor
def test_calculate_total_BAD():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), 1)
    cart.add(Product("Adidas Samba", 3200), 2)
    assert cart.total_with_shipping() == 8900


# ❌ Kötü: ismi hiçbir şey anlatmıyor
def test_cart_BAD():
    cart = Cart()
    cart.add(Product("A", 100), 1)
    assert cart.total_with_shipping() == 100


# ❌ Kötü: implementation detail'e bağlı
def test_product_has_name_BAD():
    p = Product("Nike Dunk", 2500)
    assert p.name == "Nike Dunk"  # dataclass zaten garanti ediyor


# ❌ Kötü: çok zayıf assertion
def test_total_not_none_BAD():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), 1)
    assert cart.total_with_shipping() is not None


# ============================================================
# ✅ İYİ TESTLER — Bunları YAZIN
# ============================================================

# ✅ İyi: tek davranış, net isim
def test_empty_cart_includes_shipping_cost():
    cart = Cart()
    assert cart.total_with_shipping() == 50


# ✅ İyi: AAA pattern
def test_single_item_equals_price():
    # Arrange
    cart = Cart()
    product = Product("Nike Dunk", price=2500)

    # Act
    cart.add(product, quantity=1)
    result = cart.total_with_shipping()

    # Assert
    assert result == 2500


# ✅ İyi: davranış odaklı
def test_discount_reduces_product_total_by_20_percent():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    cart.discount_code = "SOLE20"
    assert cart.total_with_shipping() == 2000


# ✅ İyi: edge case erken yakalanır
def test_discount_not_applied_below_minimum():
    cart = Cart()
    cart.add(Product("Shoe Laces", 50), quantity=1)
    cart.discount_code = "SOLE20"
    assert cart.total_with_shipping() == 100  # İndirim yok


# ✅ İyi: hata durumu
def test_negative_quantity_raises_value_error():
    cart = Cart()
    with pytest.raises(ValueError, match="Miktar"):
        cart.add(Product("Nike Dunk", 2500), quantity=-1)


# ✅ İyi: parametrize ile data-driven
@pytest.mark.parametrize("quantity,expected", [
    (1, 2500),
    (2, 5000),
    (3, 7500),
    (10, 25000),
])
def test_item_total_varies_with_quantity(quantity, expected):
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=quantity)
    assert cart.product_total() == expected
