"""
Kata 01: FizzBuzz — Test İskeleti
Bu testleri doldurun. Her test tek davranış test etsin.
"""

import pytest
from fizzbuzz import fizzbuzz


def test_returns_number_as_string_for_non_divisible():
    # TODO: 1 → "1"
    pass


def test_returns_fizz_for_multiples_of_3():
    # TODO: 3 → "Fizz"
    pass


def test_returns_buzz_for_multiples_of_5():
    # TODO: 5 → "Buzz"
    pass


def test_returns_fizzbuzz_for_multiples_of_15():
    # TODO: 15 → "FizzBuzz"
    pass


# Bonus: parametrize ile
@pytest.mark.parametrize("n,expected", [
    (1, "1"),
    (2, "2"),
    (3, "Fizz"),
    (5, "Buzz"),
    (9, "Fizz"),
    (15, "FizzBuzz"),
    (30, "FizzBuzz"),
    (7, "7"),
])
def test_fizzbuzz_parametrized(n, expected):
    # TODO
    pass
