from unittest.mock import Mock

import pytest

from checkers.board import Board
from checkers.constants import Color
from checkers.piece import Piece
from checkers.square import Square


@pytest.fixture
def brown_piece():
    return Piece(Color.BROWN)

@pytest.fixture
def red_piece():
    return Piece(Color.RED)

@pytest.fixture
def fake_board():
    return Board(empty=True)

def test_square_has_valid_defaults():
    square = Square(x=0, y=0, column=0, row=0, screen=None)
    assert not square.is_selected
    assert not square.is_hover
    assert square.piece is None


def test_square_can_move_down_when_occupied_by_brown_piece(brown_piece):
    square = Square(x=0, y=0, column=1, row=0, screen=None)
    square.piece = brown_piece
    assert not square.piece.can_move_up
    assert square.piece.can_move_down


@pytest.mark.skip(reason="we moved this logic somewhere else")
def test_legal_move_works_for_legal_moves():
    square1 = Square(x=0, y=0, square_number=1, screen=None)
    square2 = Square(x=0, y=0, square_number=8, screen=None)
    square1.piece = Color.BROWN
    assert square1.legal_move(square2, player=Color.BROWN)


def test_number_always_matches_formula():
    for row in range(8):
        for column in range(8):
            square = Square(x=0, y=0, column=column, row=row, screen=None)
            assert square.number < 64
            assert square.number == column + row*8


def test_knows_legal_moves_in_center(brown_piece, red_piece, fake_board):
    square1 = Square(x=0, y=0, column=3, row=3, screen=None)
    square1.piece = brown_piece
    assert square1.possible_moves(fake_board) == [
        (2, 2),
        (-2, 2),
        (1, 1),
        (-1, 1),
    ]
    square1.piece = red_piece
    assert square1.possible_moves(fake_board) == [
        (2, -2),
        (-2, -2),
        (1, -1),
        (-1, -1),
    ]
