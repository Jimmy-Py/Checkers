import pygame
from constants import Color


class Square(pygame.sprite.Sprite):
    SQUARE_COLORS = [Color.WHITE, Color.BLACK]
    COLUMNS = ["a", "b", "c", "d", "e", "f", "g", "h"]
    NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8"]
    SQUARE_SIDE_LENGTH = 50

    def __init__(self, color, x, y, square_number, screen=None):
        super().__init__()
        self.screen = screen
        self.image = pygame.Surface((self.SQUARE_SIDE_LENGTH, self.SQUARE_SIDE_LENGTH))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color # is either black or white (this is the color of the square, not the piece).
        self.is_selected = False
        self.number = square_number
        self.is_hover = False
        self.piece = None  # can become either Color.RED or Color.BROWN
        self.is_king = False

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Square(number={self.number})>"

    @property
    def can_move_up(self):
        if self.is_king:
            return True
        return self.piece == Color.RED

    @property
    def can_move_down(self):
        if self.is_king:
            return True
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

        if self.is_king:
            pygame.draw.line(self.screen, Color.BLACK,
                             (self.rect.centerx, self.rect.top), (self.rect.centerx, self.rect.bottom), 2)
            pygame.draw.line(self.screen, Color.BLACK,
                             (self.rect.left, self.rect.centery), (self.rect.right, self.rect.centery), 2)


    def update(self):
        self.draw()  # am I hover, selected, or original? Am I empty, have BROWN, or RED piece?
