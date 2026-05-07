"""
Kata 02: Roman Numerals — Test İskeleti
Küçükten büyüğe gidin. Her test tek sembol/kural.
"""

import pytest
from roman import to_roman


# === Basit rakamlar ===

def test_1_is_I():
    # TODO
    pass


def test_2_is_II():
    # TODO
    pass


def test_3_is_III():
    # TODO
    pass


# === Subtractive notation ===

def test_4_is_IV():
    # TODO
    pass


def test_9_is_IX():
    # TODO
    pass


# === 5 ve üzeri ===

def test_5_is_V():
    # TODO
    pass


def test_6_is_VI():
    # TODO
    pass


# === 10 ve üzeri ===

def test_10_is_X():
    # TODO
    pass


def test_14_is_XIV():
    # TODO
    pass


def test_40_is_XL():
    # TODO
    pass


def test_90_is_XC():
    # TODO
    pass


# === Büyük sayılar ===

def test_1994_is_MCMXCIV():
    # TODO
    pass


def test_3999_is_MMMCMXCIX():
    # TODO
    pass


# === Parametrize bonus ===

@pytest.mark.parametrize("n,expected", [
    (1, "I"),
    (4, "IV"),
    (5, "V"),
    (9, "IX"),
    (10, "X"),
    (40, "XL"),
    (50, "L"),
    (90, "XC"),
    (100, "C"),
    (400, "CD"),
    (500, "D"),
    (900, "CM"),
    (1000, "M"),
    (1994, "MCMXCIV"),
    (3999, "MMMCMXCIX"),
])
def test_roman_numeral_conversions(n, expected):
    # TODO
    pass
