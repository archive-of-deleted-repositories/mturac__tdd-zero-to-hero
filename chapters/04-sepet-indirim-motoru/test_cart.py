"""
Bölüm 04 — İlk Kan: Sepet İndirim Motoru
TDD ile yazılmış testler. Her test tek davranış.
"""

import pytest
from cart import Cart, Product


# === Adım 1: Boş Sepet ===

def test_empty_cart_shipping_only():
    """Boş sepette sadece kargo ücreti var."""
    cart = Cart()
    assert cart.total_with_shipping() == 50  # 0 + 50 kargo


# === Adım 2: Tek Ürün ===

def test_single_item_total():
    """Tek ürün, fiyat × miktar."""
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    assert cart.total_with_shipping() == 2500  # 2500 + 0 kargo (500+)


# === Adım 3: Çoklu Ürün ===

def test_multiple_items_total():
    """Birden fazla ürün toplanır."""
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=2)
    cart.add(Product("Adidas Samba", 3200), quantity=1)
    assert cart.total_with_shipping() == 8200  # 8200 + 0 kargo


# === Adım 4: Kargo Kuralları ===

def test_shipping_free_over_500():
    """500₺ üzeri ücretsiz kargo."""
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    assert cart.shipping_cost() == 0


def test_shipping_50_under_500():
    """500₺ altı 50₺ kargo."""
    cart = Cart()
    cart.add(Product("Shoe Laces", 50), quantity=1)
    assert cart.shipping_cost() == 50


# === Adım 5: İndirim Kodu ===

def test_discount_applies_to_products():
    """İndirim sadece ürünlere uygulanır."""
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    cart.discount_code = "SOLE20"
    # 2500 * 0.8 = 2000, kargo 0 (500+)
    assert cart.total_with_shipping() == 2000


# === Adım 6: Minimum Sepet Tutarı ===

def test_discount_requires_minimum_200():
    """İndirim kodu için minimum 200₺ gerekli."""
    cart = Cart()
    cart.add(Product("Shoe Laces", 50), quantity=1)
    cart.discount_code = "SOLE20"
    # 50 < 200, indirim yok → 50 + 50 kargo = 100
    assert cart.total_with_shipping() == 100


# === Adım 7: Geçersiz İndirim Kodu ===

def test_invalid_discount_code_no_discount():
    """Geçersiz kod = indirim yok."""
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    cart.discount_code = "INVALID"
    assert cart.total_with_shipping() == 2500


# === Adım 8: Edge Case — Negatif Miktar ===

def test_negative_quantity_raises():
    """Negatif miktar hata fırlatmalı."""
    cart = Cart()
    with pytest.raises(ValueError):
        cart.add(Product("Nike Dunk", 2500), quantity=-1)


# === Adım 9: Farklı İndirim Kodları ===

def test_different_discount_codes():
    """Farklı kodlar farklı indirim uygular."""
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)

    cart.discount_code = "SOLE10"
    assert cart.total_with_shipping() == 2250  # 2500 * 0.9

    cart.discount_code = "WELCOME"
    assert cart.total_with_shipping() == 2125  # 2500 * 0.85


# === Adım 10: Kargo + İndirim Etkileşimi ===

def test_discount_may_affect_shipping_threshold():
    """İndirim sonrası tutar 500'ün altına düşerse kargo eklenir."""
    cart = Cart()
    cart.add(Product("Nike Dunk", 600), quantity=1)
    cart.discount_code = "SOLE20"
    # 600 * 0.8 = 480 < 500 → kargo 50 → toplam 530
    assert cart.total_with_shipping() == 530
