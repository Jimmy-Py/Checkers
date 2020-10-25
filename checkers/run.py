# 6-2-20 Checkers project, Jimmy B, overseen by Ray B.

import pygame

from .board import Board
from .game import CheckersGame
from .sound_machine import SoundMachine

# Global Variables

def main():
    # General Setup
    pygame.init()
    sound_machine = SoundMachine()

    board = Board()
    game = CheckersGame(board, sound_machine)
    should_restart = game.run()
    pygame.quit()
    if should_restart:
        return "Restart"
    print(should_restart)


if __name__ == "__main__":
    while main() == "Restart":
        pass
