from typing import NoReturn

import pygame

from src.game import Game

__release__: str = "04/05/2020"
__version__: float = 2.0

pygame.init()
pygame.mixer.init()


def main() -> NoReturn:
    game: Game = Game()
    game.main()


if __name__ == '__main__':
    main()
