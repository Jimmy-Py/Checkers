from pathlib import Path
from pygame.locals import K_r, K_m
import logging
import os

import pygame

from .ai import AI
from .constants import Color
from .square import Square, Move, is_jump, get_jumped_move

# Local Constants
LOOP_ITERATIONS_PER_SECOND = 5


class CheckersGame():
    WAITING = "Waiting for Player"
    OVER = "Game Over"
    PARTIAL_SELECT = "Partial Select"
    TOP_PROMOTION_ROW = 0
    BOTTOM_PROMOTION_ROW = 7

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
            logging.warn("skipping", sound, "sound")

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

    def remove_capture(self, previous_selection, move):
        intermediate_square = previous_selection.other_square_from_move(get_jumped_move(move))
        intermediate_square.piece = None

    def make_king(self, previous_selection, new_selection):
        if previous_selection.piece.is_red and new_selection.row == self.TOP_PROMOTION_ROW:
            previous_selection.piece.is_king = True
            logging.info("Congratulations, you're a king!")

        if previous_selection.piece.is_brown and new_selection.row == self.BOTTOM_PROMOTION_ROW:
            previous_selection.piece.is_king = True
            logging.info("Congratulations, you're a king!")

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
            proposed_move = Move(
                column_delta=new_selection.column - self.previous_selection.column,
                row_delta=new_selection.row - self.previous_selection.row,
            )
            if proposed_move in self.previous_selection.possible_moves():
                # Give piece to new square.
                player_goes_again = False
                new_selection.piece = self.previous_selection.piece
                if is_jump(proposed_move):
                    self.remove_capture(self.previous_selection, proposed_move)
                    self.play_sound("capture")
                    if new_selection.possible_moves(captures_only=True):
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
        # Setup
        clock = pygame.time.Clock()  # clock method stored in the variable "clock"
        pygame.display.set_caption("Checkers!")
        while True:
            # Handle events
            logging.debug("Current State %s - Player %s", self.state, self.player)
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

                ##  !!!! THIS IS WHERE THE REAL GAME LOGIC STARTS !!!!!!
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
                logging.debug(self.ai.legal_moves)
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
