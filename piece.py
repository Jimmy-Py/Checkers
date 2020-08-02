import pygame
from constants import Color

class Piece():
    def __init__(self,color,is_king=False):
        self.color = color
        self.is_king = is_king

    @property
    def is_red(self):
        return self.color == Color.RED

    @property
    def is_brown(self):
        return self.color == Color.BROWN

    def belongs_to(self, player):
        return self.color == player

    def draw(self, screen, rect):
        pygame.draw.ellipse(screen, self.color, rect)

        if self.is_king:
            pygame.draw.line(screen, Color.BLACK,
                             (rect.centerx, rect.top), (rect.centerx, rect.bottom), 2)
            pygame.draw.line(screen, Color.BLACK,
                             (rect.left, rect.centery), (rect.right, rect.centery), 2)
