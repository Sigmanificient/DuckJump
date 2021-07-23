from random import randrange
from typing import Optional

import pygame

from src.game import Game
from src.utils import load


PLATFORM_TEXTURE_PATH: str = "src/assets/images/platform.png"


class Platform:
    _texture: Optional[pygame.Surface] = None

    def __init__(self, x: int, y: int) -> None:
        """Initialises a new moving platform."""
        self.rect: pygame.Rect = self.texture.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.initial_y: int = self.rect.y

    @property
    def texture(self) -> pygame.Surface:
        """Load the platform texture."""
        if self._texture is None:
            self._texture: pygame.Surface = load(PLATFORM_TEXTURE_PATH)
        return self._texture

    def move(self, game: Game) -> None:
        if self.rect.x < -500:
            self.rect.x = max(
                platform.rect.x for platform in game.platforms
            ) + randrange(600, 1000)

            self.rect.y = randrange(400, 620)
            self.initial_y: int = self.rect.y

        else:
            self.rect.x -= int(game.player.ax)

    def check_hit_box(self, game: Game) -> None:
        """Check player hit box with the platform."""
        if any(
                [
                    self.rect.collidepoint(
                        game.player.rect.x, game.player.rect.y + 68
                    ),
                    self.rect.collidepoint(
                        game.player.rect.x + 50, game.player.rect.y + 68
                    )
                ]
        ):

            game.player.rect.y = self.rect.y - 68 + 1
            game.player.jump_count = 1
            self.rect.x += randrange(0, 2) - 1
            self.rect.y += 2

        elif self.rect.y > self.initial_y:
            self.rect.y -= 1

        if any(
                [
                    self.rect.collidepoint(
                        game.player.rect.x + 50, game.player.rect.y
                    ),
                    self.rect.collidepoint(
                        game.player.rect.x + 50, game.player.rect.y + 66
                    )
                ]
        ):
            game.player.rect.x = self.rect.x - 51
            if game.player.rect.x < 0:
                game.over = True
