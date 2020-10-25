from unittest.mock import Mock

import pytest

from square import Square
from piece import Piece
from constants import Color


@pytest.fixture
def brown_piece():
    return Piece(Color.BROWN)

@pytest.fixture
def red_piece():
    return Piece(Color.RED)

@pytest.fixture
def fake_board():
    def mock_square_number(i):
        m = Mock()
        m.number = i
        return m
    return [mock_square_number(i) for i in range(64)]

def test_square_has_valid_defaults():
    square = Square(Color.WHITE, x=0, y=0, square_number=0, screen=None)
    assert not square.is_selected
    assert not square.is_hover
    assert square.piece is None


def test_square_can_move_down_when_occupied_by_brown_piece(brown_piece):
    square = Square(Color.WHITE, x=0, y=0, square_number=1, screen=None)
    square.piece = brown_piece
    assert not square.piece.can_move_up
    assert square.piece.can_move_down


@pytest.mark.skip(reason="we moved this logic somewhere else")
def test_legal_move_works_for_legal_moves():
    square1 = Square(Color.BLACK, x=0, y=0, square_number=1, screen=None)
    square2 = Square(Color.BLACK, x=0, y=0, square_number=8, screen=None)
    square1.piece = Color.BROWN
    assert square1.legal_move(square2, player=Color.BROWN)


def test_column_and_row_always_below_8():
    for i in range(64):
        square = Square(Color.BLACK, x=0, y=0, square_number=i, screen=None)
        assert square.column < 8
        assert square.row < 8
        assert square.column >= 0
        assert square.row >= 0


def test_knows_legal_moves_in_center(brown_piece, red_piece, fake_board):
    square1 = Square(Color.BLACK, x=0, y=0, square_number=36, screen=None)
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
