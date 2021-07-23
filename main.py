import pygame

from src.game import Game

__release__ = "04/05/2020"
__version__ = 2.0

pygame.init()
pygame.mixer.init()


def main():
    game = Game()
    game.main()


if __name__ == '__main__':
    main()
