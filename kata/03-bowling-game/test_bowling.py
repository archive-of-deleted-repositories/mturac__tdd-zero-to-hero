"""
Kata 03: Bowling Game — Test İskeleti
Her test tek senaryo. Sırayla gidin.
"""

import pytest
from bowling import BowlingGame


def test_gutter_game_scores_zero():
    """Tüm atışlarda 0 pin → skor 0."""
    # TODO: 20 kez 0 at, skor 0 olmalı
    pass


def test_all_ones_scores_twenty():
    """Tüm atışlarda 1 pin → skor 20."""
    # TODO: 20 kez 1 at, skor 20 olmalı
    pass


def test_one_spare():
    """Bir spare + sonraki atışın bonusu."""
    # TODO: 5+5 (spare), sonra 3, sonra 17 kez 0
    # Skor: 10 + 3 (bonus) + 3 = 16
    pass


def test_one_strike():
    """Bir strike + sonraki 2 atışın bonusu."""
    # TODO: 10 (strike), sonra 3+4, sonra 16 kez 0
    # Skor: 10 + 3 + 4 + 3 + 4 = 24
    pass


def test_perfect_game():
    """Mükemmel oyun: tüm strike'lar → skor 300."""
    # TODO: 12 kez 10 at (10 frame + 2 bonus)
    # Skor: 300
    pass


def test_all_spares():
    """Tüm spare'ler → skor 150."""
    # TODO: 21 kez 5 at (10 spare + 1 bonus)
    # Skor: 150
    pass
