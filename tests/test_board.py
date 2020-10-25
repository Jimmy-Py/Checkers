import pytest

from checkers.board import Board
from checkers.constants import Color


def test_board_sets_up_tiles_correctly():
    """Trickier than it looks, row 1 is white ... row 2 is black... and that pattern repeats 4 times"""
    colors = 4*(4*[Color.WHITE, Color.BLACK] + 4*[Color.BLACK, Color.WHITE])

    board = Board()

    for i in range(64):
        assert board.squares[i].color == colors[i]

@pytest.mark.parametrize("color,piece_indexes",[
    (Color.BROWN, [1, 3, 5, 7, 8, 12, 10, 14, 17, 19, 21, 23]),
    (Color.RED, [40, 42, 44, 46, 49, 51, 53, 55, 56, 58, 60, 62]),
])
def test_board_sets_up_brown_pieces_correctly(color, piece_indexes):
    board = Board()
    for index in piece_indexes:
        assert board.squares[index].piece
        assert board.squares[index].piece.color == color

def test_can_create_empty_board():
    board = Board(empty=True)

    assert len(board.squares) == 64
    assert not [s for s in board.squares if s.piece]
