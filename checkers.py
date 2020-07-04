# 6-2-20 Checkers project, Jimmy B, overseen by Ray B.

import pygame
from checkers_game import CheckersGame
from square import Square
from constants import Color

# Global Variables
SQUARES_IN_COLUMN = 8
LEFT_SHIFT = 225
DOWN_SHIFT = 10


def make_squares(screen):
    square_sprites = pygame.sprite.Group()
    x = LEFT_SHIFT  # draw board away from left edge of display surface.
    y = DOWN_SHIFT
    column_counter = 0
    color_counter = 0
    for square_number in range(0, 64):
        if color_counter % 2 != 0:  # color_counter is odd
            c = 1  # make next square black.
        else:
            c = 0  # make next square white.
        square_sprites.add(Square(Square.SQUARE_COLORS[c], x, y, square_number, screen=screen))
        x += Square.SQUARE_DIMENSION
        column_counter += 1

        if column_counter >= SQUARES_IN_COLUMN:
            x = LEFT_SHIFT
            y += Square.SQUARE_DIMENSION
            column_counter = 0
            continue
        color_counter += 1  # make next square a different color

    brown_pieces = [1, 3, 5, 7, 8, 12, 10, 14, 17, 19, 21, 23]
    red_pieces = [40, 42, 44, 46, 49, 51, 53, 55, 56, 58, 60, 62]

    for square in square_sprites:
        if square.number in brown_pieces:
            square.piece = Color.BROWN

    for square in square_sprites:
        if square.number in red_pieces:
            square.piece = Color.RED

    return square_sprites


def main():
    # General Setup
    pygame.init()
    smallText = pygame.font.Font("freesansbold.ttf", 20) # this has to come after pygame is initialized.

    # Setting up the main window
    screen_width = 1280
    screen_height = 830
    screen = pygame.display.set_mode((screen_width, screen_height))  # returns a display-surface object
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
