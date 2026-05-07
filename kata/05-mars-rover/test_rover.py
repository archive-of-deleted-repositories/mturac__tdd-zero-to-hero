"""
Kata 05: Mars Rover — Test İskeleti
Her test tek davranış. Sırayla gidin.
"""

import pytest
from rover import Rover


# === Başlangıç ===

def test_default_position_is_origin():
    # TODO: Rover() → (0, 0)
    pass


def test_default_direction_is_north():
    # TODO: Rover() → "N"
    pass


def test_custom_starting_position():
    # TODO: Rover(3, 5, "E") → (3, 5), "E"
    pass


# === İleri Git (F) ===

def test_move_forward_north():
    # TODO: Rover(0, 0, "N").execute("F") → (0, 1)
    pass


def test_move_forward_east():
    # TODO: Rover(0, 0, "E").execute("F") → (1, 0)
    pass


def test_move_forward_south():
    # TODO: Rover(0, 1, "S").execute("F") → (0, 0)
    pass


def test_move_forward_west():
    # TODO: Rover(1, 0, "W").execute("F") → (0, 0)
    pass


# === Geri Git (B) ===

def test_move_backward_north():
    # TODO: Rover(0, 1, "N").execute("B") → (0, 0)
    pass


# === Döndürme ===

def test_turn_left_from_north():
    # TODO: Rover(0, 0, "N").execute("L") → yön "W"
    pass


def test_turn_right_from_north():
    # TODO: Rover(0, 0, "N").execute("R") → yön "E"
    pass


def test_full_rotation_left():
    # TODO: 4 kez L → orijinal yön
    pass


# === Çoklu Komut ===

def test_multiple_commands():
    # TODO: "FFRFF" → pozisyon ve yön kontrolü
    pass


# === Toroidal Izgara ===

def test_wrap_around_north_edge():
    # TODO: Rover(0, 9, "N").execute("F") → (0, 0)
    pass


def test_wrap_around_east_edge():
    # TODO: Rover(9, 0, "E").execute("F") → (0, 0)
    pass


# === Geçersiz Komut ===

def test_invalid_command_ignored():
    # TODO: "FXF" → X görmezden gelinir, sadece FF uygulanır
    pass
