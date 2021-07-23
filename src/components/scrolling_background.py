from typing import Optional

import pygame

from src.utils import load

BACKGROUND_PATH: str = "assets/images/bg.png"


class ScrollingBackground:
    """A Layer used to create a indefinitely scrolling background."""
    _texture: Optional[pygame.Surface] = None

    def __init__(self, offset) -> None:
        """Initialises infinite scroll background."""
        self.rect: pygame.Rect = self.texture.get_rect()
        self.rect.x = offset

    @property
    def texture(self) -> pygame.Surface:
        """Load the background texture."""
        if self._texture is None:
            self._texture: pygame.Surface = load(BACKGROUND_PATH)
        return self._texture

    def update(self) -> None:
        """Move the scrolling background for a infinite effect."""
        self.rect.x = self.rect.x - 1 if self.rect.x > -1280 else 1280
