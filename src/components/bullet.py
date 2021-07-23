from random import randrange
from typing import Optional

import pygame

from src.components.player import Player
from src.utils import load

PLATFORM_TEXTURE_PATH: str = "assets/images/bullet-bill.png"


class Bullet:
    """The player enemy which kills the player on collision."""
    _texture: Optional[pygame.Surface] = None

    def __init__(self) -> None:
        """Initialises a bullet enemy."""
        self.rect: pygame.Rect = self.texture.get_rect()
        self.setup()

    def setup(self) -> None:
        """Set bullet coordinates for a new party."""
        self.rect.x = randrange(1300, 3000)
        self.rect.y = randrange(720)

    @property
    def texture(self) -> pygame.Surface:
        """Load the bullet texture."""
        if self._texture is None:
            self._texture: pygame.Surface = load(PLATFORM_TEXTURE_PATH)
        return self._texture

    def move(self, game) -> None:
        """Move the bullet to the left and cycle position if offscreen."""
        self.rect.x -= 2 * int(game.player.ax)

        if self.rect.x - self.rect.width > 0:
            self.setup()

    def check_hit_box(self, player: Player) -> int:
        """Check any collision with a player to trigger a game over."""
        return self.rect.colliderect(player.rect)
