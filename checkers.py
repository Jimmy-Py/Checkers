# 6-2-20 Checkers project, Jimmy B, overseen by Ray B.

import pygame, sys

SQUARES_IN_COLUMN = 8  # Why can't I store this inside the Board() class?


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


class Square(pygame.Rect):
    SQUARE_COLORS = [BLACK, WHITE]
    COLUMNS = ["a","b","c","d","e","f","g","h"]
    NUMBERS = ["1","2","3","4","5","6","7","8"]
    SQUARE_DIMENSION = 10

    def __init__(self, column, number, color, x, y):
        super(Square,self).__init__(x, y, 10, 10)  # why can't I use SQUARE_DIMENSION here?
        self.name = column + number
        self.color = color
        self.piece = None

    def __string__(self):
        rep = self.name + self.color
        return rep

class Board():

    def __init__(self):
        self.board_list = []


    def make_board_list(self):
        x, y = 0, 0
        i = 0
        c = 0
        color_counter = 0
        for column in Square.COLUMNS:
            for number in Square.NUMBERS:
                self.board_list.append(Square(column,number,Square.SQUARE_COLORS[c],x,y))
                x += Square.SQUARE_DIMENSION
                i += 1
                if color_counter % 2 != 0:  # color_counter is odd
                    color = 1
                else:
                    color = 0

                if i > SQUARES_IN_COLUMN:
                    x = 0
                    y += Square.SQUARE_DIMENSION
                    i = 1


    # def draw_board(self):
    #     for square in test.board_list:
    #         #pygame.draw.rect(screen, square.color)
    #         print square.color  # how to access attributes of squares in board_list?

test = Board()
test.make_board_list()
print(test.board_list)


#Main
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Visuals
    all_sprites.update()
    all_sprites.draw(screen)


    pygame.display.update()
    clock.tick(60)