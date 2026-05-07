"""
Bölüm 03 — Red-Green-Refactor: Döngünün Mekaniği
Her test tek davranış test eder. AAA pattern.
"""

import pytest
from cart import Cart, Product


# === 🔴 RED → 🟢 GREEN: Temel Davranışlar ===

def test_empty_cart_total_is_zero():
    # Arrange
    cart = Cart()
    # Act
    result = cart.total()
    # Assert
    assert result == 0


def test_single_item_total():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    assert cart.total() == 2500


def test_multiple_items_total():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=2)
    cart.add(Product("Adidas Samba", 3200), quantity=1)
    assert cart.total() == 8200


# === 🔴 RED → 🟢 GREEN: Edge Case'ler ===

def test_negative_quantity_raises_error():
    cart = Cart()
    with pytest.raises(ValueError):
        cart.add(Product("Nike Dunk", 2500), quantity=-1)


def test_zero_quantity_does_not_add_item():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=0)
    assert cart.item_count() == 0


# === 🔴 RED → 🟢 GREEN: Sepetten Silme ===

def test_remove_item_from_cart():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    cart.add(Product("Adidas Samba", 3200), quantity=1)
    cart.remove(Product("Nike Dunk"))
    assert cart.item_count() == 1
    assert cart.total() == 3200


def test_remove_nonexistent_item_does_nothing():
    cart = Cart()
    cart.add(Product("Nike Dunk", 2500), quantity=1)
    cart.remove(Product("Adidas Samba"))
    assert cart.item_count() == 1
