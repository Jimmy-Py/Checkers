import pygame
from pygame.locals import K_r, K_m
from constants import Color
from ai import AI
import sounds

# Local Constants
LOOP_ITERATIONS_PER_SECOND = 5


class CheckersGame():
    WAITING = "Waiting for Player"
    OVER = "Game Over"
    PARTIAL_SELECT = "Partial Select"
    TOP_KING_PROMOTION_SQUARES = [1, 3, 5, 7]
    BOTTOM_KING_PROMOTION_SQUARES = [56, 58, 60, 62]

    def __init__(self, square_sprites):
        self.sound_enabled = True
        self.capture_sound = pygame.mixer.Sound("sounds\\capture.wav")
        self.unselection_sound = pygame.mixer.Sound("sounds\\unselect.wav")
        self.selection_sound = pygame.mixer.Sound("sounds\\select.wav")
        self.normal_move_sound = pygame.mixer.Sound("sounds\\normal_move.wav")
        self.illegal_move_sound = pygame.mixer.Sound("sounds\\illegal_move.wav")
        self.font = pygame.font.Font("freesansbold.ttf", 20)
        self.state = self.WAITING
        self.player = Color.RED
        self.message = "Red's Turn"
        self.square_sprites = square_sprites
        self.previous_selection = None
        self._temporary_message_timer = 0
        self._temporary_message = None
        self.AI_IS_ON = True
        if self.AI_IS_ON:
            self.ai = AI()

    def play_sound(self, sound):
        if self.sound_enabled:
            pygame.mixer.Sound.play(sound)  # the sounds variables are found in the init() of the class.

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

    def communication_window(self, message, screen):
        if self._temporary_message_timer > 0:
            message = self._temporary_message
            self._temporary_message_timer -= 1
        square_length = self.square_sprites.sprites()[0].SQUARE_SIDE_LENGTH
        y_pos = square_length * 8 + 50
        text = self.font.render(message, True, Color.BLACK, Color.WHITE)
        rect = text.get_rect(centerx=(square_length * 12.5)/2, top=y_pos)
        screen.blit(text, rect)

    @staticmethod
    def is_capture(previous_selection, new_selection):
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

    def remove_capture(self, previous_selection, new_selection, square_sprites):
        # Jumping Up
        if new_selection.number == previous_selection.number - 14:
            square_sprites.sprites()[previous_selection.number - 7].piece = None

        elif new_selection.number == previous_selection.number - 18:
            square_sprites.sprites()[previous_selection.number - 9].piece = None

        # Jumping Down
        elif new_selection.number == previous_selection.number + 14:
            square_sprites.sprites()[previous_selection.number + 7].piece = None

        elif new_selection.number == previous_selection.number + 18:
            square_sprites.sprites()[previous_selection.number + 9].piece = None

    def legal_move(self, previous_selection, new_selection, square_sprites):
        if previous_selection.piece.can_move_up:
            if new_selection.number == previous_selection.number - 7 \
                    or new_selection.number == previous_selection.number - 9:
                print("True, Legal!", "new:", new_selection.number, "previous:", previous_selection.number)
                return True

            # Jumping
            elif new_selection.number == previous_selection.number - 14 \
                    and square_sprites.sprites()[previous_selection.number - 7].piece.color != previous_selection.piece.color:
                return True

            elif new_selection.number == previous_selection.number - 18 \
                    and square_sprites.sprites()[previous_selection.number - 9].piece.color != previous_selection.piece.color:
                return True

        if previous_selection.piece.can_move_down:
            if new_selection.number == previous_selection.number + 7 \
                    or new_selection.number == previous_selection.number + 9:
                print("True, Legal!", "new:", new_selection.number, "previous:", previous_selection.number)
                print(previous_selection.number - 7)
                return True

            # Jumping
            elif new_selection.number == previous_selection.number + 14 \
                    and square_sprites.sprites()[previous_selection.number + 7].piece.color \
                    != previous_selection.piece.color:
                return True

            elif new_selection.number == previous_selection.number + 18 \
                    and square_sprites.sprites()[previous_selection.number + 9].piece.color \
                    != previous_selection.piece.color:
                return True

        else:
            print("False, Illegal!", "new:", new_selection.number, "previous:", previous_selection.number)
            return False

    def make_king(self, previous_selection, new_selection):
        if previous_selection.piece.is_red and new_selection.number in self.TOP_KING_PROMOTION_SQUARES:
            previous_selection.piece.is_king = True
            print("Congratulations, you're a king!")

        if previous_selection.piece.is_brown and new_selection.number in self.BOTTOM_KING_PROMOTION_SQUARES:
            previous_selection.piece.is_king = True
            print("Congratulations, you're a king!")

    def handle_click(self, mouse_x, mouse_y):
        new_selection = None
        for square in self.square_sprites:
            if square.contains_point(mouse_x, mouse_y):
                new_selection = square
                break

        if new_selection:
            return self._handle_click_square(new_selection)

    def _handle_click_square(self, new_selection):
        if self.state == self.PARTIAL_SELECT and new_selection.piece is None:  # User selects an open square, in state "Partial Select". # why is this better than " == None" ?
            if self.legal_move(self.previous_selection, new_selection, self.square_sprites):
                # Give piece to new square.
                new_selection.piece = self.previous_selection.piece
                if self.is_capture(self.previous_selection, new_selection):
                    self.remove_capture(self.previous_selection, new_selection, self.square_sprites)
                    self.play_sound(self.capture_sound)
                self.make_king(self.previous_selection, new_selection)
                self.play_sound(self.normal_move_sound)
                self.state = self.WAITING
                self.change_players()
                self.previous_selection.is_selected = False
                self.previous_selection.piece = None
                self.previous_selection = None
                self.play_sound(self.normal_move_sound)

            else:
                self.temporary_message("Illegal Move!")
                self.play_sound(self.illegal_move_sound)

        # User selects square they have already selected for first choice in "Partial Select"
        elif self.state == self.PARTIAL_SELECT and new_selection.is_selected:
            new_selection.is_selected = False  # unselect original square.
            self.state = "Waiting for Player"
            self.play_sound(self.unselection_sound)

        # State is "Waiting for Player" and player selects a square with a piece (in order to move it).
        elif self.state == self.WAITING and new_selection.piece and new_selection.piece.belongs_to(self.player):
            new_selection.is_selected = True
            self.state = self.PARTIAL_SELECT
            self.previous_selection = new_selection
            self.play_sound(self.selection_sound)

    def run(self, screen):
        clock = pygame.time.Clock()  # clock method stored in the variable "clock"
        while True:
            print(self.state, self.player)
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    self.square_sprites = None  # I commented this line out, and the program still shutdown correctly without it. Does it server some other purpose?
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_r:
                        self.square_sprites = None
                        return True
                    if event.key == K_m:  # mute sound effects
                        self.sound_enabled = not self.sound_enabled
                        if self.sound_enabled:
                            self.temporary_message("Sound Enabled")
                        else:
                            self.temporary_message("Sound Muted")

                # Upon user click, see if mouse is in any square. "Select" square where mouse is and "unselect"
                # previously selected square.
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(*mouse)

                # Mouse Hover turns Square Blue (unless square is already selected).
                for square in self.square_sprites:
                    if square.contains_point(*mouse):
                        square.is_hover = True
                    else:
                        square.is_hover = False

            if self.AI_IS_ON and self.player == Color.BROWN: # technically not using State (unless you consider self.player state)
                self.ai.find_legal_moves(self.square_sprites)
                print(self.ai.legal_moves)
                initial_square, new_square = self.ai.ai_move_choice()

                self.play_sound(self.normal_move_sound)
                self.state = self.WAITING
                self.change_players()
                self.play_sound(self.normal_move_sound)


            # Visuals
            screen.fill(Color.LIGHT_GREY)
            self.communication_window(self.message, screen)
            self.square_sprites.update()
            pygame.display.update()
            clock.tick(LOOP_ITERATIONS_PER_SECOND)
