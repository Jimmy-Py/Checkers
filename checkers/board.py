import pygame

from .constants import Color
from .piece import Piece
from .square import Square

class Board:
    NUMBER_OF_ROWS = 8
    NUMBER_OF_COLUMNS = 8
    HORIZONTAL_BUFFER = int(Square.SQUARE_SIDE_LENGTH * 2.25)
    VERTICAL_BUFFER = int(Square.SQUARE_SIDE_LENGTH / 10)

    DEFAULT_SCREEN_WIDTH = Square.SQUARE_SIDE_LENGTH * NUMBER_OF_COLUMNS + 2 * HORIZONTAL_BUFFER
    DEFAULT_SCREEN_HEIGHT = Square.SQUARE_SIDE_LENGTH * NUMBER_OF_ROWS + 2 * VERTICAL_BUFFER + 100

    def __init__(self, screen=None, empty=False):
        self.screen = screen or pygame.display.set_mode((self.DEFAULT_SCREEN_WIDTH, self.DEFAULT_SCREEN_HEIGHT))
        self.square_sprites = pygame.sprite.Group()
        self._load_sprites(empty)
        self.squares = self.square_sprites.sprites()

    def update(self):
        self.square_sprites.update()

    def square_at(self, column, row):
        return self.squares[column+row*8]

    def _load_sprites(self, empty):
        # Start drawing at the edge of the buffer space
        for row in range(8):
            x = self.HORIZONTAL_BUFFER
            y = row * Square.SQUARE_SIDE_LENGTH

            for column in range(8):
                self.square_sprites.add(Square(x, y, column=column, row=row, board=self))
                x += Square.SQUARE_SIDE_LENGTH

        if not empty:
            for square in [s for s in self.square_sprites if s.color == Color.BLACK]:
                if square.row < 3:
                    square.piece = Piece(Color.BROWN)
                elif square.row > 4:
                    square.piece = Piece(Color.RED)
