# 6-2-20 Checkers project, Jimmy B, overseen by Ray B.

import pygame, sys

# Global Variables
SQUARES_IN_COLUMN = 8
LEFT_SHIFT = 225
DOWN_SHIFT = 10
# pieces_list = [[0, 0, False, n] for n in range(0, 64)]
# first digit is color (0 for empty, 1 for brown, 2 for black).
# second digit is 0 for foot solider, 1 for king.
# Third boolean, Fale for unselected-square, True for selected-square.

# General Setup
pygame.init()
clock = pygame.time.Clock()  # clock method stored in the variable "clock"

# Setting up the main window
screen_width = 1280
screen_height = 830
screen = pygame.display.set_mode((screen_width, screen_height))  # returns a display-surface object
pygame.display.set_caption("Checkers!")

# Colors
LIGHT_GREY = (200, 200, 200)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
BLUE_DARK = (0, 0, 255)
GREEN = (0, 255, 0)


class CheckersGame():
    def __init__(self):
        self.state = "Waiting for Player"
        self.player = "P1"

    def accepting_clicks(self):
        return self.state != "Game Over."

    def can_move(self, player):
        return self.player == player  # returns a boolean whether or not a given player can move.

    def change_players(self):
        if self.player == "P1":
            self.player = "P2"
        elif self.player == "P2":
            self.player = "P1"




class Square(pygame.sprite.Sprite):
    SQUARE_COLORS = [WHITE, BLACK]
    COLUMNS = ["a", "b", "c", "d", "e", "f", "g", "h"]
    NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8"]
    SQUARE_DIMENSION = 100

    def __init__(self, color, x, y, number, column=None):
        super().__init__()
        # why do we need to use put "Square" in front of "SQUARE_DIMENSION"? it's inside the same class...
        self.image = pygame.Surface((self.SQUARE_DIMENSION, self.SQUARE_DIMENSION))
        #self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color
        self.is_selected = False
        self.number = number
        self.is_hover = False
        self.piece = None
        # self.name = column + number

    def __string__(self):
        return self.name

    def contains_point(self, x, y):
        return self.rect.x + Square.SQUARE_DIMENSION > x > self.rect.x and self.rect.y + Square.SQUARE_DIMENSION > y > self.rect.y

    def draw(self):
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, self.rect)

        elif self.is_hover:
            pygame.draw.rect(screen, BLUE_DARK, self.rect)

        else:
            pygame.draw.rect(screen, self.color, self.rect)  # square is neither selected nor hovered.

        if self.piece:
            if self.piece == "BROWN":
                pygame.draw.ellipse(screen, BROWN, self.rect)
            if self.piece == "RED":
                pygame.draw.ellipse(screen, RED, self.rect)

    # def open_neighbor_selected(self):
    #     if self.is_selected and self.piece:
    #         for square in square_sprites:
    #             if square.is_selected and square.piece is None:  # why is this better than " == None" ?
    #
    #
    #     open_neighbors = pygame.sprite.group()
    #     for square in square_sprites:
    #         if square.is_selected:
    #             open_neighbors.add(square)
    #     # for square in open_neighbors:
    #     #     if square.number


    def update(self):
        self.draw()  # am I hover, selected, or original? Am I empty, have BROWN, or RED piece?


# Sprites
square_sprites = pygame.sprite.Group()
pieces_sprites = pygame.sprite.Group()


def make_squares():
    x = LEFT_SHIFT  # draw board away from left edge of display surface.
    y = DOWN_SHIFT
    column_counter = 0
    color_counter = 0
    for square in range(0, 64):
        if color_counter % 2 != 0:  # color_counter is odd
            c = 1  # make next square black.
        else:
            c = 0  # make next square white.
        square_sprites.add(Square(Square.SQUARE_COLORS[c], x, y, square))
        x += Square.SQUARE_DIMENSION
        column_counter += 1

        if column_counter >= SQUARES_IN_COLUMN:
            x = LEFT_SHIFT
            y += Square.SQUARE_DIMENSION
            column_counter = 0
            continue
        color_counter += 1  # make next square a different color


def set_initial_piece_position():
    brown_pieces = [1, 3, 5, 7, 8, 12, 10, 14, 17, 19, 21, 23]
    red_pieces = [40, 42, 44, 46, 49, 51, 53, 55, 56, 58, 60, 62]

    for square in square_sprites:
        if square.number in brown_pieces:
            square.piece = "BROWN"

    for square in square_sprites:
        if square.number in red_pieces:
            square.piece = "RED"


# Main
Game = CheckersGame()
make_squares()
set_initial_piece_position()


while True:
    print(Game.state, Game.player)
    for event in pygame.event.get():
        mouse = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Upon user click, see if mouse is in any square. "Select" square where mouse is and "unselect" previously
        # selected square.
        if event.type == pygame.MOUSEBUTTONDOWN:
            for square in square_sprites:
                if square.contains_point(*mouse):

                    if Game.state == "Partial Select" and square.piece is None:  # why is this better than " == None" ?

                        # Gives piece to new square.
                        # Maybe we should just use "RED" and "BROWN" instead of P1 and P2?
                        if Game.player == "P1":
                            square.piece = "RED"
                        if Game.player == "P2":
                            square.piece = "BROWN"

                        for i in square_sprites:  # is there a better name choice here than using "i"?
                            if i.is_selected:
                                i.piece = None  # remove piece from old square
                                i.is_selected = False  # unselect old square.
                        Game.state = "Waiting for Player"
                        Game.change_players()

                    # Player selects square they have already selected for first choice in "Partial Select"
                    elif Game.state == "Partial Select" and square.is_selected:
                        square.is_selected = False
                        Game.state = "Waiting for Player"
                    else:
                        square.is_selected = True
                        Game.state = "Partial Select"

        # Mouse Hover turns Square Blue (unless square is already selected).
        for square in square_sprites:
            if square.contains_point(*mouse):
                square.is_hover = True
            else:
                square.is_hover = False

        for square in square_sprites:
            if square.is_selected:
                Game.state = "Partial Select"

#TODO add a display for user to see who's turn it is.
    # Visuals
    screen.fill(LIGHT_GREY)
    square_sprites.update()
    pygame.display.update()
    clock.tick(5)
