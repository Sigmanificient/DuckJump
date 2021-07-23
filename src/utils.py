from typing import Tuple

import pygame


def load(path: str, alpha: bool = True) -> pygame.Surface:
    """Loads a asset from a file and convert it into a pygame.Surface."""
    return pygame.image.load(path).convert_alpha() \
        if alpha else pygame.image.load(path).convert()


def get_text(
        text: str,
        font: pygame.Font,
        color: Tuple[int, int, int],
        position: Tuple[int, int],
        centered: bool = False
) -> Tuple[pygame.Surface, pygame.Rect]:
    """Return a rendered text with proper coordinates and its rect."""
    text: pygame.Surface = font.render(text, True, color, None)
    text_rect: pygame.Rect = text.get_rect()

    if centered:
        text_rect.center = position
    else:
        text_rect.x, text_rect.y = position

    return text, text_rect
