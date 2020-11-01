from collections import namedtuple
import pygame

from .constants import Color

Move = namedtuple("Move", "column_delta, row_delta")

def is_jump(move_tuple):
    return abs(move_tuple.column_delta) == 2

def get_jumped_move(move_tuple):
    """Take a move tuple (e.g. 2, 2) and return the jumped equivalent for that move (e.g. 1, 1)"""
    assert set(abs(x) for x in move_tuple) == set([2]), f"tried to calculate jump on {move_tuple}"
    return Move(
        column_delta=(1 if move_tuple.column_delta == 2 else -1),
        row_delta=(1 if move_tuple.row_delta == 2 else -1)
    )

class Square(pygame.sprite.Sprite):
    COLUMNS = ["a", "b", "c", "d", "e", "f", "g", "h"]
    NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8"]
    SQUARE_SIDE_LENGTH = 50

    def __init__(self, x, y, column, row, board=None):
        super().__init__()
        self.board = board
        self.image = pygame.Surface((self.SQUARE_SIDE_LENGTH, self.SQUARE_SIDE_LENGTH))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = Color.WHITE if column % 2 == row % 2 else Color.BLACK
        self.is_selected = False
        self.column = column
        self.row = row
        self.is_hover = False
        self.piece = None  # can become either Color.RED or Color.BROWN

    def __repr__(self):
        return f"<Square(number={self.number})>"

    @property
    def number(self):
        return self.column + self.row*8

    def possible_moves(self, captures_only=False):
        possible_moves = [
            Move(2,   2),
            Move(2,  -2),
            Move(-2,  2),
            Move(-2, -2),
        ]
        if not captures_only:
            possible_moves.extend([get_jumped_move(m) for m in possible_moves])

        moves_on_the_board = [
            m for m in possible_moves
            if 0 <= m[0] + self.column < 8  # you stay on the horizontal
               and 0 <= m[1] + self.row < 8  # you stay on the vertical
        ]
        moves_in_the_correct_direction = [
            m for m in moves_on_the_board
            if (self.piece.can_move_down and m.row_delta > 0)
               or (self.piece.can_move_up and m.row_delta < 0 )
        ]
        moves_we_can_enter = [ m for m in moves_in_the_correct_direction if self.can_enter(m)]

        return [m for m in moves_we_can_enter
                if not is_jump(m) or self.can_perform_jump(m)]

    def can_enter(self, move):
        return self.other_square_from_move(move).piece is None

    def can_perform_jump(self, jump_move_tuple):
        """ returns true, when there is an opposing piece diagonally
        adjacent to you in the direction of the jump"""
        jumped_move = get_jumped_move(jump_move_tuple) # turn -2, 2 into -1, 1
        jumped_square = self.other_square_from_move(jumped_move)
        return jumped_square.piece is not None and self.piece != jumped_square.piece

    def other_square_from_move(self, move):
        return self.board.square_at(
            column=self.column + move.column_delta,
            row=self.row + move.row_delta,
        )

    def contains_point(self, x, y):
        return self.rect.x + Square.SQUARE_SIDE_LENGTH > x > self.rect.x and self.rect.y + Square.SQUARE_SIDE_LENGTH > y > self.rect.y

    def draw(self):
        if self.is_selected:
            pygame.draw.rect(self.board.screen, Color.GREEN, self.rect)  # make square green (selected).

        elif self.is_hover:
            pygame.draw.rect(self.board.screen, Color.BLUE_DARK, self.rect)  # make square blue (hovered).

        else:
            pygame.draw.rect(self.board.screen, self.color, self.rect)  # square is neither selected nor hovered.

        if self.piece:
            self.piece.draw(self.board.screen, self.rect)

    def update(self):
        self.draw()  # am I hover, selected, or original? Am I empty, have BROWN, or RED piece?
