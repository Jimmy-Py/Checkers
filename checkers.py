# 6-2-20 Checkers project, Jimmy B, overseen by Ray B.

import pygame, sys

# Global Variables
SQUARES_IN_COLUMN = 8
LEFT_SHIFT = 225
DOWN_SHIFT = 10
pieces_list = [[0,0,False] for n in range(0, 64)]
# first digit is color (0 for empty, 1 for brown, 2 for black).
# second digit is 0 for foot solider, 1 for king.
# Third boolean, Fale for unselected-square, True for selected-square.

# General Setup
pygame.init()
clock = pygame.time.Clock()   # clock method stored in the variable "clock"

# Setting up the main window
screen_width = 1280
screen_height = 830
screen = pygame.display.set_mode((screen_width, screen_height))  # returns a display-surface object
pygame.display.set_caption("Checkers!")

# Colors
LIGHT_GREY = (200,200,200)
RED = (255, 0, 0)
BLACK = (0,0,0)
WHITE = (255,255,255)
BROWN = (139,69,19)
BLUE_DARK = (0,0,255)
GREEN = (0,255,0)


class Square(pygame.sprite.Sprite):
    SQUARE_COLORS = [WHITE,BLACK]
    COLUMNS = ["a","b","c","d","e","f","g","h"]
    NUMBERS = ["1","2","3","4","5","6","7","8"]
    SQUARE_DIMENSION = 100


    def __init__(self, color, x, y, number, column = None):
        super().__init__()
        # why do we need to use put "Square" infront of "SQUARE_DIMENSON"? it's inside the same class...
        self.image = pygame.Surface((Square.SQUARE_DIMENSION,Square.SQUARE_DIMENSION))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color
        self.selected = False
        self.number = number
        # self.piece = None
        # self.name = column + number

    def __string__(self):
        return self.name

    def update(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.rect.x + Square.SQUARE_DIMENSION > mouse[0] > self.rect.x and self.rect.y + Square.SQUARE_DIMENSION > mouse[1] > self.rect.y:
            self.image.fill(BLUE_DARK)
            if click[0] == 1:
                self.selected = not self.selected  # toggle boolean value of self.selected
                #print(pieces_list[self.number][2])
                pieces_list[self.number][2] = not pieces_list[self.number][2]  # Toggle boolean of square selection.

        else:
            self.image.fill(self.color)

        if self.selected:
            self.image.fill(GREEN)
            print(pieces_list[self.number][2])

# Sprites
square_sprites = pygame.sprite.Group()
pieces_sprites = pygame.sprite.Group()


def make_squares():
    x = LEFT_SHIFT  # draw board away from left edge of display surface.
    y = DOWN_SHIFT
    column_counter = 0
    c = 0
    color_counter = 0
    for square in range(0,64):
        if color_counter % 2 != 0:  # color_counter is odd
            c = 1  # make next square black.
        else:
            c = 0  # make next square white.
        square_sprites.add(Square(Square.SQUARE_COLORS[c],x,y,square))
        x += Square.SQUARE_DIMENSION
        column_counter += 1

        if column_counter >= SQUARES_IN_COLUMN:
            x = LEFT_SHIFT
            y += Square.SQUARE_DIMENSION
            column_counter = 0
            continue
        color_counter += 1  # make next square a different color


def set_initial_piece_position():
    brown_pieces = [1,3,5,7,8,12,10,14,17,19,21,23]
    red_pieces = [40,42,44,46,49,51,53,55,56,58,60,62]

    for piece in brown_pieces:
        pieces_list[piece][0] = 1

    for piece in red_pieces:
        pieces_list[piece][0] = 2


def attach_pieces():
    piece_counter = 0
    for square in square_sprites:
        if pieces_list[piece_counter][0] == 1:
            pygame.draw.ellipse(screen, BROWN, square)
        if pieces_list[piece_counter][0] == 2:
            pygame.draw.ellipse(screen, RED, square)
        piece_counter += 1


def move():
    selected_squares = []
    for square in pieces_list:
        if square[2]:  # Test if Square is selected.
            selected_squares.append(square)

    if len(selected_squares) >= 2:
        if selected_squares[0][0] == 1 and selected_squares[1][0] == 0:  # first square has brown piece, other square is open.
            pieces_list[selected_squares[0][3]][0] = 0  # original square with brown piece is to empty.
            pieces_list[selected_squares[1][3]][0] = 1  # open square now gets brown piece
            #square_sprites[selected_squares[0][3]].selected = False  # this throws and interesting error.
    print(selected_squares)

# Main
make_squares()
set_initial_piece_position()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Visuals
    screen.fill(LIGHT_GREY)
    square_sprites.update()
    square_sprites.draw(screen)
    move()
    attach_pieces()
    #print(piece_list)


    pygame.display.update()
    clock.tick(5)