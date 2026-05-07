"""
Bölüm 02 — Işık: TDD ile Tanışma
Test dosyası — RED → GREEN → REFACTOR döngüsü.
"""

import pytest
from cart import Cart, Product


# 🔴 RED → 🟢 GREEN: Boş sepet
def test_empty_cart_total_is_zero():
    cart = Cart()
    assert cart.total() == 0


# 🔴 RED → 🟢 GREEN: Tek ürün
def test_single_item_total():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    assert cart.total() == 2500


# 🟢 GREEN: Çoklu ürün — zaten çalışıyordu
def test_multiple_items_total():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=2)
    cart.add(Product("Adidas Samba", 3200), quantity=1)
    assert cart.total() == 8200


# 🔴 RED → 🟢 GREEN: Miktar ile çarpım
def test_single_item_multiplied_by_quantity():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=3)
    assert cart.total() == 7500
