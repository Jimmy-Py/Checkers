import pygame
from pygame.locals import K_r, K_m
from constants import Color
import sounds

# Local Constants
LOOP_ITERATIONS_PER_SECOND = 5


class CheckersGame():
    WAITING = "Waiting for Player"
    OVER = "Game Over"
    PARTIAL_SELECT = "Partial Select"

    def __init__(self, square_sprites):
        self.sound_enabled = True
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

    def play_sound(self, sound):
        if self.sound_enabled:
            pygame.mixer.Sound.play(sound)  # the sounds variables are found in the init() of the class.

    def accepting_clicks(self):
        return self.state != self.OVER

    def can_move(self, player):
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

            # Visuals
            screen.fill(Color.LIGHT_GREY)
            self.communication_window(self.message, screen)
            self.square_sprites.update()
            pygame.display.update()
            clock.tick(LOOP_ITERATIONS_PER_SECOND)

    def is_capture(self, previous_selection, new_selection):
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

    def handle_click(self, mouse_x, mouse_y):
        for new_selection in self.square_sprites:
            if new_selection.contains_point(mouse_x, mouse_y):
                if self.state == self.PARTIAL_SELECT and new_selection.piece is None:  # User selects an open square, in state "Partial Select". # why is this better than " == None" ?
                    if self.previous_selection.legal_move(new_selection, self.player, self.square_sprites):
                        # Give piece to new square.
                        new_selection.piece = self.player
                        if self.is_capture(self.previous_selection, new_selection):
                            self.remove_capture(self.previous_selection, new_selection, self.square_sprites)
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
                elif new_selection.piece == self.player and self.state == self.WAITING:
                    new_selection.is_selected = True
                    self.state = self.PARTIAL_SELECT
                    self.previous_selection = new_selection
                    self.play_sound(self.selection_sound)
