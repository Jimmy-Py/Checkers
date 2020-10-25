from pathlib import Path
from pygame.locals import K_r, K_m
import os

import pygame

from .ai import AI
from .constants import Color
from .square import Square

# Local Constants
LOOP_ITERATIONS_PER_SECOND = 5


class CheckersGame():
    WAITING = "Waiting for Player"
    OVER = "Game Over"
    PARTIAL_SELECT = "Partial Select"
    TOP_KING_PROMOTION_SQUARES = [1, 3, 5, 7]
    BOTTOM_KING_PROMOTION_SQUARES = [56, 58, 60, 62]

    def __init__(self, board, sound_machine=None):
        self.board = board
        self.sound_machine = sound_machine

        self.font = pygame.font.Font("freesansbold.ttf", 20)
        self.state = self.WAITING
        self.player = Color.RED
        self.message = "Red's Turn"
        self.previous_selection = None
        self._temporary_message_timer = 0
        self._temporary_message = None
        self.AI_IS_ON = False
        if self.AI_IS_ON:
            self.ai = AI()

    def play_sound(self, sound):
        if self.sound_machine:
            self.sound_machine.play(sound)
        else:
            print("skipping", sound, "sound")

    def accepting_clicks(self):
        return self.state != self.OVER

    def can_movef(self, player):
        return self.player == player  # returns a boolean whether or not a given player can move.

    def change_players(self):
        if self.player == Color.RED:
            self.player = Color.BROWN
            self.message = "Brown's Turn"
        elif self.player == Color.BROWN:
            self.player = Color.RED
            self.message = "Red's Turn"

    def temporary_message(self, message):
        self._temporary_message = message
        self._temporary_message_timer = 4

    def communication_window(self, message):
        if self._temporary_message_timer > 0:
            message = self._temporary_message
            self._temporary_message_timer -= 1
        square_length = Square.SQUARE_SIDE_LENGTH
        y_pos = square_length * 8 + 50
        text = self.font.render(message, True, Color.BLACK, Color.WHITE)
        rect = text.get_rect(centerx=(square_length * 12.5)/2, top=y_pos)
        self.board.screen.blit(text, rect)

    @staticmethod
    def is_jump(previous_selection, new_selection):
        # Jumping Up
        if new_selection.number == previous_selection.number - 14:
            return True

        elif new_selection.number == previous_selection.number - 18:
            return True

        # Jumping Down
        elif new_selection.number == previous_selection.number + 14:
            return True

        elif new_selection.number == previous_selection.number + 18:
            return True

    def remove_capture(self, previous_selection, new_selection):
        # Jumping Up
        if new_selection.number == previous_selection.number - 14:
            self.board.squares[previous_selection.number - 7].piece = None

        elif new_selection.number == previous_selection.number - 18:
            self.board.squares[previous_selection.number - 9].piece = None

        # Jumping Down
        elif new_selection.number == previous_selection.number + 14:
            self.board.squares[previous_selection.number + 7].piece = None

        elif new_selection.number == previous_selection.number + 18:
            self.board.squares[previous_selection.number + 9].piece = None

    def legal_move(self, previous_selection, new_selection):
        proposed_move = (
            new_selection.column - previous_selection.column,
            new_selection.row - previous_selection.row,
        )
        print(proposed_move)
        possible_moves = previous_selection.possible_moves(self.board)
        print(possible_moves)
        return proposed_move in possible_moves

    def make_king(self, previous_selection, new_selection):
        if previous_selection.piece.is_red and new_selection.number in self.TOP_KING_PROMOTION_SQUARES:
            previous_selection.piece.is_king = True
            print("Congratulations, you're a king!")

        if previous_selection.piece.is_brown and new_selection.number in self.BOTTOM_KING_PROMOTION_SQUARES:
            previous_selection.piece.is_king = True
            print("Congratulations, you're a king!")

    def handle_click(self, mouse_x, mouse_y):
        new_selection = None
        for square in self.board.square_sprites:
            if square.contains_point(mouse_x, mouse_y):
                new_selection = square
                break

        if new_selection:
            return self._handle_click_square(new_selection)

    def _handle_click_square(self, new_selection):
        if self.state == self.PARTIAL_SELECT and new_selection.piece is None:  # User selects an open square, in state "Partial Select". # why is this better than " == None" ?
            if self.legal_move(self.previous_selection, new_selection):
                # Give piece to new square.
                player_goes_again = False
                new_selection.piece = self.previous_selection.piece
                if self.is_jump(self.previous_selection, new_selection):
                    self.remove_capture(self.previous_selection, new_selection)
                    self.play_sound("capture")
                    if new_selection.possible_moves(self.board, captures_only=True):
                        player_goes_again = True
                self.make_king(self.previous_selection, new_selection)
                self.state = self.WAITING
                if not player_goes_again:
                    self.change_players()
                self.previous_selection.is_selected = False
                self.previous_selection.piece = None
                self.previous_selection = None
                self.play_sound("normal_move")

            else:
                self.temporary_message("Illegal Move!")
                self.play_sound("illegal_move")

        # User selects square they have already selected for first choice in "Partial Select"
        elif self.state == self.PARTIAL_SELECT and new_selection.is_selected:
            new_selection.is_selected = False  # unselect original square.
            self.state = "Waiting for Player"
            self.play_sound("unselection")

        # State is "Waiting for Player" and player selects a square with a piece (in order to move it).
        elif self.state == self.WAITING and new_selection.piece and new_selection.piece.belongs_to(self.player):
            new_selection.is_selected = True
            self.state = self.PARTIAL_SELECT
            self.previous_selection = new_selection
            self.play_sound("selection")

    def run(self):
        clock = pygame.time.Clock()  # clock method stored in the variable "clock"
        pygame.display.set_caption("Checkers!")
        while True:
            print(self.state, self.player)
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    self.board = None  # I commented this line out, and the program still shutdown correctly without it. Does it server some other purpose?
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_r:
                        self.board = None
                        return True
                    if event.key == K_m and self.sound_machine:  # mute sound effects
                        if self.sound_machine.toggle_mute():
                            self.temporary_message("Sound Muted")
                        else:
                            self.temporary_message("Sound Enabled")

                # Upon user click, see if mouse is in any square. "Select" square where mouse is and "unselect"
                # previously selected square.
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(*mouse)

                # Mouse Hover turns Square Blue (unless square is already selected).
                for square in self.board.square_sprites:
                    if square.contains_point(*mouse):
                        square.is_hover = True
                    else:
                        square.is_hover = False

            if self.AI_IS_ON and self.player == Color.BROWN: # technically not using State (unless you consider self.player state)
                self.ai.find_legal_moves(self.board)
                print(self.ai.legal_moves)
                initial_square, new_square = self.ai.ai_move_choice()
                # gives piece from initial to new.
                new_square.piece = initial_square.piece
                initial_square.piece = None

                self.play_sound("normal_move")
                self.state = self.WAITING
                self.change_players()
                self.play_sound("normal_move")


            # Visuals
            self.board.screen.fill(Color.LIGHT_GREY)
            self.communication_window(self.message)
            self.board.update()
            pygame.display.update()
            clock.tick(LOOP_ITERATIONS_PER_SECOND)
