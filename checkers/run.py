# 6-2-20 Checkers project, Jimmy B, overseen by Ray B.
import logging
import sys

import pygame

from .board import Board
from .game import CheckersGame
from .sound_machine import SoundMachine


def main():
    # General Setup
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    pygame.init()
    sound_machine = SoundMachine()

    board = Board()
    game = CheckersGame(board, sound_machine)
    should_restart = game.run()
    pygame.quit()
    if should_restart:
        return "Restart"
    should_restart = False
    logging.info("Game ended with 'should_restart' set to %s", should_restart)


if __name__ == "__main__":
    while main() == "Restart":
        pass
