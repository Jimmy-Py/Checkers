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
        self.previously_selected = None
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

    def handle_click(self, mouse_x, mouse_y):
        for square in self.square_sprites:
            if square.contains_point(mouse_x, mouse_y):
                if self.state == self.PARTIAL_SELECT and square.piece is None:  # User selects an open square, in state "Partial Select". # why is this better than " == None" ?
                    if self.previously_selected.legal_move(square, self.player, self.square_sprites):
                        # Give piece to new square.
                        square.piece = self.player
                        self.state = self.WAITING
                        self.change_players()
                        # if self.previously_selected.is_capture():
                        #     pass
                        self.previously_selected.is_selected = False
                        self.previously_selected.piece = None
                        self.previously_selected = None
                        self.play_sound(self.normal_move_sound)


                    else:
                        self.temporary_message("Illegal Move!")
                        self.play_sound(self.illegal_move_sound)

                # User selects square they have already selected for first choice in "Partial Select"
                elif self.state == self.PARTIAL_SELECT and square.is_selected:
                    square.is_selected = False  # unselect original square.
                    self.state = "Waiting for Player"
                    self.play_sound(self.unselection_sound)

                # State is "Waiting for Player" and player selects a square with a piece (in order to move it).
                elif square.piece == self.player and self.state == self.WAITING:
                    square.is_selected = True
                    self.state = self.PARTIAL_SELECT
                    self.previously_selected = square
                    self.play_sound(self.selection_sound)
