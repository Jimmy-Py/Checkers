from square import Square
from constants import Color

def test_square_has_valid_defaults():
    square = Square(Color.WHITE, x=0, y=0, square_number=0, screen=None)
    assert not square.is_selected
    assert not square.is_hover
    assert square.piece is None
    # if no piece can't move
    assert not square.can_move_up
    assert not square.can_move_down

def test_square_can_move_down_when_occupied_by_brown_piece():
    square = Square(Color.WHITE, x=0, y=0, square_number=1, screen=None)
    square.piece = Color.BROWN
    assert not square.can_move_up
    assert square.can_move_down

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


def test_knows_legal_moves_in_center():
    square1 = Square(Color.BLACK, x=0, y=0, square_number=36, screen=None)
    assert square1.possible_moves == [
            (2,   2),
            (1,   1),
            (2,  -2),
            (1,  -1),
            (-1,  1),
            (-2,  2),
            (-1, -1),
            (-2, -2),
    ]
