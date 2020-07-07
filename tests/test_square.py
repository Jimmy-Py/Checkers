from checkers.square import Square
from checkers.constants import Color

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
