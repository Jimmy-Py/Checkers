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

    def __init__(self, screen=None):
        self.screen = screen or pygame.display.set_mode((self.DEFAULT_SCREEN_WIDTH, self.DEFAULT_SCREEN_HEIGHT))
        self.square_sprites = pygame.sprite.Group()
        self._load_sprites()
        self.squares = self.square_sprites.sprites()

    def update(self):
        self.square_sprites.update()

    def square_at(self, column, row):
        return self.squares[column+row*8]

    def _load_sprites(self):
        # Start drawing at the edge of the buffer space
        x, y = self.HORIZONTAL_BUFFER, self.VERTICAL_BUFFER
        column_counter = 0
        color_counter = 0
        for square_number in range(0, 64):
            if color_counter % 2 != 0:  # color_counter is odd
                c = 1  # make next square black.
            else:
                c = 0  # make next square white.
            self.square_sprites.add(Square(Square.SQUARE_COLORS[c], x, y, square_number, screen=self.screen))
            x += Square.SQUARE_SIDE_LENGTH
            column_counter += 1

            if column_counter >= self.NUMBER_OF_COLUMNS:
                x = self.HORIZONTAL_BUFFER
                y += Square.SQUARE_SIDE_LENGTH
                column_counter = 0
                continue
            color_counter += 1  # make next square a different color

        initial_brown_pieces = [1, 3, 5, 7, 8, 12, 10, 14, 17, 19, 21, 23]
        initial_red_pieces = [40, 42, 44, 46, 49, 51, 53, 55, 56, 58, 60, 62]

        for square in self.square_sprites:
            if square.number in initial_brown_pieces:
                square.piece = Piece(Color.BROWN)
            if square.number in initial_red_pieces:
                square.piece = Piece(Color.RED)
