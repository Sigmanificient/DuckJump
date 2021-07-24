from typing import NoReturn

import pygame

from src.game import Game

__release__: str = "07/24/2020"
__version__: float = 3.0

pygame.init()
pygame.display.init()


def main() -> NoReturn:
    game: Game = Game()
    game.main()


if __name__ == '__main__':
    main()
