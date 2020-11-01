from unittest.mock import Mock

import pytest

from checkers.board import Board
from checkers.constants import Color
from checkers.piece import Piece
from checkers.square import Square, Move, is_jump


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
    square = Square(x=0, y=0, column=0, row=0)
    assert not square.is_selected
    assert not square.is_hover
    assert square.piece is None


def test_square_can_move_down_when_occupied_by_brown_piece(brown_piece):
    square = Square(x=0, y=0, column=1, row=0)
    square.piece = brown_piece
    assert not square.piece.can_move_up
    assert square.piece.can_move_down


def test_number_always_matches_formula():
    for row in range(8):
        for column in range(8):
            square = Square(x=0, y=0, column=column, row=row)
            assert square.number < 64
            assert square.number == column + row*8


def test_knows_legal_moves_in_center_for_brown(brown_piece, fake_board):
    square1 = Square(x=0, y=0, column=3, row=3, board=fake_board)
    square1.piece = brown_piece
    assert square1.possible_moves() == [
        (1, 1),
        (-1, 1),
    ]


def test_knows_legal_moves_in_center_for_red(red_piece, fake_board):
    square1 = Square(x=0, y=0, column=3, row=3, board=fake_board)
    square1.piece = red_piece
    assert square1.possible_moves() == [
        (1, -1),
        (-1, -1),
    ]

def test_handles_jump_condition(brown_piece, red_piece, fake_board):
    """
        . . . . .
        . . B . .
        . R . . .
        . . . . .
    """
    red_square = fake_board.square_at(column=1, row=2)
    red_square.piece = red_piece

    brown_square = fake_board.square_at(column=2,row=1)
    brown_square.piece = brown_piece

    assert set(red_square.possible_moves()) == set([
        Move(column_delta=2, row_delta=-2),
        Move(column_delta=-1, row_delta=-1),
    ])

def test_only_legal_jumps_possible(brown_piece, red_piece, fake_board):
    """
        . . . . .
        . . . B .
        . . R . .
        . . . . .
    """

    red_square = fake_board.square_at(column=2, row=2)
    red_square.piece = red_piece

    brown_square = fake_board.square_at(column=3,row=1)
    brown_square.piece = brown_piece

    assert set(red_square.possible_moves()) == set([
        Move(column_delta=2, row_delta=-2),
        Move(column_delta=-1, row_delta=-1),
    ])

def test_is_jump_works_correctly():
    jumps = [
        Move(2,2),
        Move(2,-2),
        Move(-2,2),
        Move(-2,-2),
    ]
    not_jumps = [
        Move(1,1),
        Move(1,-1),
        Move(-1,1),
        Move(-1,-1),
    ]

    assert not [jump for jump in jumps if not is_jump(jump)]
    assert not [not_jump for not_jump in not_jumps if is_jump(not_jump)]
