import sys
import os

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from basic_version_terminal import create_board, check_victory, check_draw


# ---------------------------------------------------------------------------
# create_board
# ---------------------------------------------------------------------------

def test_board_creation_size():
    """Deska má správný počet řádků a sloupců."""
    board = create_board(5)
    assert len(board) == 5
    assert all(len(row) == 5 for row in board)


def test_board_creation_empty():
    """Všechny buňky nové desky jsou prázdné."""
    board = create_board(3)
    assert all(cell == " " for row in board for cell in row)


# ---------------------------------------------------------------------------
# check_victory
# ---------------------------------------------------------------------------

def test_check_victory_row():
    """Vítěz je detekován v řádku."""
    board = create_board(5)
    for col in range(3):
        board[0][col] = "X"
    won, seq = check_victory(board, "X", 3)
    assert won is True
    assert (0, 0) in seq
    assert (0, 1) in seq
    assert (0, 2) in seq


def test_check_victory_column():
    """Vítěz je detekován ve sloupci."""
    board = create_board(5)
    for row in range(3):
        board[row][2] = "O"
    won, seq = check_victory(board, "O", 3)
    assert won is True
    assert (0, 2) in seq
    assert (2, 2) in seq


def test_check_victory_main_diagonal():
    """Vítěz je detekován na hlavní diagonále."""
    board = create_board(5)
    for k in range(3):
        board[k][k] = "X"
    won, seq = check_victory(board, "X", 3)
    assert won is True
    assert (0, 0) in seq
    assert (1, 1) in seq
    assert (2, 2) in seq


def test_check_victory_anti_diagonal():
    """Vítěz je detekován na vedlejší diagonále."""
    board = create_board(5)
    for k in range(3):
        board[k][2 - k] = "O"
    won, seq = check_victory(board, "O", 3)
    assert won is True


def test_check_victory_no_winner():
    """Prázdná deska nemá vítěze."""
    board = create_board(4)
    won, seq = check_victory(board, "X", 3)
    assert won is False
    assert seq is None


def test_check_victory_not_enough_in_row():
    """Sekvence kratší než win_length není vítězná."""
    board = create_board(5)
    board[0][0] = "X"
    board[0][1] = "X"
    won, seq = check_victory(board, "X", 3)
    assert won is False


# ---------------------------------------------------------------------------
# check_draw
# ---------------------------------------------------------------------------

def test_check_draw_full_board():
    """Plná deska bez vítěze je remíza."""
    board = [
        ["X", "O", "X"],
        ["O", "X", "O"],
        ["O", "X", "O"],
    ]
    assert check_draw(board) is True


def test_check_draw_empty_board():
    """Prázdná deska není remíza."""
    board = create_board(3)
    assert check_draw(board) is False


def test_check_draw_one_empty_cell():
    """Deska s jednou prázdnou buňkou není remíza."""
    board = [
        ["X", "O", "X"],
        ["O", "X", "O"],
        ["O", "X", " "],
    ]
    assert check_draw(board) is False