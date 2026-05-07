"""
Kata 04: String Calculator — Test İskeleti
Her kural için ayrı test. Sırayla gidin.
"""

import pytest
from string_calc import add


# === Kural 1: Boş string ===

def test_empty_string_returns_zero():
    # TODO: add("") → 0
    pass


# === Kural 2: Tek sayı ===

def test_single_number_returns_itself():
    # TODO: add("1") → 1
    pass


# === Kural 3: İki sayı ===

def test_two_numbers_comma_separated():
    # TODO: add("1,2") → 3
    pass


# === Kural 4: Birden fazla sayı ===

def test_multiple_numbers():
    # TODO: add("1,2,3") → 6
    pass


# === Kural 5: Yeni satır ayırıcı ===

def test_newline_as_delimiter():
    # TODO: add("1\n2,3") → 6
    pass


# === Kural 6: Özel ayırıcı ===

def test_custom_delimiter():
    # TODO: add("//;\n1;2") → 3
    pass


# === Kural 7: Negatif sayılar ===

def test_negative_number_raises_error():
    # TODO: add("1,-2") → ValueError
    pass


def test_multiple_negatives_show_all_in_error():
    # TODO: add("1,-2,-3") → ValueError: "negatif sayılar kabul edilmez: -2, -3"
    pass
