import pygame
from .constants import Color


class Square(pygame.sprite.Sprite):
    SQUARE_COLORS = [Color.WHITE, Color.BLACK]
    COLUMNS = ["a", "b", "c", "d", "e", "f", "g", "h"]
    NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8"]
    SQUARE_SIDE_LENGTH = 10

    def __init__(self, color, x, y, square_number, screen=None):
        super().__init__()
        self.screen = screen
        self.image = pygame.Surface((self.SQUARE_SIDE_LENGTH, self.SQUARE_SIDE_LENGTH))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color
        self.is_selected = False
        self.number = square_number
        self.is_hover = False
        self.piece = None  # either Color.RED or Color.BROWN

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Square(number={self.number})>"

    @property
    def can_move_up(self):
        return self.piece == Color.RED

    @property
    def can_move_down(self):
        return self.piece == Color.BROWN

    def contains_point(self, x, y):
        return self.rect.x + Square.SQUARE_SIDE_LENGTH > x > self.rect.x and self.rect.y + Square.SQUARE_SIDE_LENGTH > y > self.rect.y

    def draw(self):
        if self.is_selected:
            pygame.draw.rect(self.screen, Color.GREEN, self.rect)  # make square green (selected).

        elif self.is_hover:
            pygame.draw.rect(self.screen, Color.BLUE_DARK, self.rect)  # make square blue (hovered).

        else:
            pygame.draw.rect(self.screen, self.color, self.rect)  # square is neither selected nor hovered.

        if self.piece:
            pygame.draw.ellipse(self.screen, self.piece, self.rect)

    def legal_move(self, new_square, player):
        if self.can_move_up:
            if new_square.number == self.number - 7 or new_square.number == self.number - 9:
                print("True, Legal!", "new:", new_square.number, "previous:", self.number)
                print(self.number - 7)
                return True
            else:
                print("False, Illegal!", "new:", new_square.number, "previous:", self.number)
                print(self.number - 7)
                return False

        if self.can_move_down:
            if new_square.number == self.number + 7 or new_square.number == self.number + 9:
                print("True, Legal!", "new:", new_square.number, "previous:", self.number)
                print(self.number - 7)
                return True
            else:
                print("False, Illegal!", "new:", new_square.number, "previous:", self.number)
                print(self.number + 7)
                return False

        return False

    def update(self):
        self.draw()  # am I hover, selected, or original? Am I empty, have BROWN, or RED piece?
