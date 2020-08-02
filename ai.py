import pygame, random
from constants import Color

class AI():
    def __init__(self):
        self.legal_moves = []

    def find_legal_moves(self, square_sprites, ai_color=Color.BROWN):
        # Creates a list whose elements are initial_square and new_square
        for initial_square in square_sprites:
            if initial_square.piece:
                # All Brown Pieces
                if initial_square.piece.is_brown and initial_square.piece.can_move_down:
                    if square_sprites.sprites()[initial_square.number + 7].piece is None:
                        self.legal_moves.append([initial_square, square_sprites.sprites()[initial_square.number + 7]])
                        # if/when I make an error here, how am I supposed to catch it?
                        # when I print this list to terminal, why does it square 8 always come up first in the list?

                # Brown Kings
                if initial_square.piece.is_brown and initial_square.piece.can_move_up:
                    if square_sprites.sprites[initial_square.number - 7].piece is None:
                        self.legal_moves.append([initial_square, square_sprites.sprites()[initial_square.number - 7]])

    def ai_move_choice(self):
        return random.choice(self.legal_moves)

