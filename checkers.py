# 6-2-20 Checkers project, Jimmy B, overseen by Ray B.

import pygame
from checkers_game import CheckersGame
from square import Square
from constants import Color

# Global Variables
NUMBER_OF_ROWS = 8
NUMBER_OF_COLUMNS = 8
HORIZONTAL_BUFFER = int(Square.SQUARE_SIDE_LENGTH * 2.25)
VERTICAL_BUFFER = int(Square.SQUARE_SIDE_LENGTH / 10)
SCREEN_WIDTH = Square.SQUARE_SIDE_LENGTH * NUMBER_OF_COLUMNS + 2 * HORIZONTAL_BUFFER
SCREEN_HEIGHT = Square.SQUARE_SIDE_LENGTH * NUMBER_OF_ROWS + 2 * VERTICAL_BUFFER + 100


def make_squares(screen):
    square_sprites = pygame.sprite.Group()
    x = HORIZONTAL_BUFFER  # draw board away from left edge of display surface.
    y = VERTICAL_BUFFER
    column_counter = 0
    color_counter = 0
    for square_number in range(0, 64):
        if color_counter % 2 != 0:  # color_counter is odd
            c = 1  # make next square black.
        else:
            c = 0  # make next square white.
        square_sprites.add(Square(Square.SQUARE_COLORS[c], x, y, square_number, screen=screen))
        x += Square.SQUARE_SIDE_LENGTH
        column_counter += 1

        if column_counter >= NUMBER_OF_COLUMNS:
            x = HORIZONTAL_BUFFER
            y += Square.SQUARE_SIDE_LENGTH
            column_counter = 0
            continue
        color_counter += 1  # make next square a different color

    initial_brown_pieces = [1, 3, 5, 7, 8, 12, 10, 14, 17, 19, 21, 23]
    initial_red_pieces = [40, 42, 44, 46, 49, 51, 53, 55, 56, 58, 60, 62]

    for square in square_sprites:
        if square.number in initial_brown_pieces:
            square.piece = Color.BROWN

    for square in square_sprites:
        if square.number in initial_red_pieces:
            square.piece = Color.RED

    return square_sprites


def main():
    # General Setup
    pygame.init()

    # Setting up the main window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # returns a display-surface object
    pygame.display.set_caption("Checkers!")

    squares = make_squares(screen)
    game = CheckersGame(squares)
    should_restart = game.run(screen)
    pygame.quit()
    if should_restart:
        return "Restart"
    print(should_restart)


if __name__ == "__main__":
    while main() == "Restart":
        pass
