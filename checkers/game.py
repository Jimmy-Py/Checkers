import pygame
from pygame.locals import K_r
from .constants import Color

# Local Constants
LOOP_ITERATIONS_PER_SECOND = 5


class CheckersGame():
    WAITING = "Waiting for Player"
    OVER = "Game Over"
    PARTIAL_SELECT = "Partial Select"

    def __init__(self, square_sprites):
        self.state = self.WAITING
        self.player = Color.RED
        self.message = "Red's Turn"
        self.square_sprites = square_sprites
        self.previously_selected = None

    def accepting_clicks(self):
        return self.state != self.OVER

    def can_move(self, player):
        return self.player == player  # returns a boolean whether or not a given player can move.

    def change_players(self):
        if self.player == Color.RED:
            self.player = Color.BROWN
        elif self.player == Color.BROWN:
            self.player = Color.RED

    def communication_window(self, message):
        pass
        #textSurface = font.render(text, True, black)

    def run(self, screen):
        clock = pygame.time.Clock()  # clock method stored in the variable "clock"
        while True:
            print(self.state, self.player)
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    self.square_sprites = None
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_r:
                        self.square_sprites = None
                        return True

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

            # TODO add a display for user to see who's turn it is.
            # Visuals
            screen.fill(Color.LIGHT_GREY)
            self.communication_window("test")
            self.square_sprites.update()
            pygame.display.update()
            clock.tick(LOOP_ITERATIONS_PER_SECOND)

    def handle_click(self, mouse_x, mouse_y):
        for square in self.square_sprites:
            if square.contains_point(mouse_x, mouse_y):
                if self.state == self.PARTIAL_SELECT and square.piece is None:  # User selects an open square, in state "Partial Select". # why is this better than " == None" ?
                    if self.previously_selected.legal_move(square, self.player):
                        # Give piece to new square.
                        square.piece = self.player
                        self.state = self.WAITING
                        self.change_players()
                        self.previously_selected.is_selected = False
                        self.previously_selected.piece = None
                        self.previously_selected = None


                # User selects square they have already selected for first choice in "Partial Select"
                elif self.state == self.PARTIAL_SELECT and square.is_selected:
                    square.is_selected = False  # unselect original square.
                    self.state = "Waiting for Player"

                # State is "Waiting for Player" and player selects a square with a piece (in order to move it).
                elif square.piece == self.player and self.state == self.WAITING:
                    square.is_selected = True
                    self.state = self.PARTIAL_SELECT
                    self.previously_selected = square

                else:
                    pass
                    # TODO Display message "Please select a (brown or red) piece based on whose turn it is."
