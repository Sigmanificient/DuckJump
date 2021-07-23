from typing import Optional

import pygame

from src.utils import load


PLAYER_SOUND_PATH: str = "src/assets/sounds/jump.wav"
PLAYER_TEXTURE_PATH: str = "src/assets/images/duck3.png"

Sound = pygame.mixer.Sound


class Player:
    """The game player with associated mechanism."""

    _texture: Optional[pygame.Surface] = None

    def __init__(self) -> None:
        """Load Player assets and behavior."""
        self.jump_sound: Sound = pygame.mixer.Sound(PLAYER_SOUND_PATH)
        self.rect: pygame.Rect = self.texture.get_rect()
        self.rect.x, self.rect.y = 300, -100

        self.ax: float = 0
        self.ay: float = 0
        self.gravity: float = 0.1
        self.max_speed_y: int = 8
        self.max_speed_x: int = 10
        self.jump_count: int = 2
        self.currently_in_jump: bool = False
        self.jump_available: bool = True
        self.behavior: str = "walk"

    @property
    def texture(self) -> pygame.Surface:
        """Load the player texture."""
        if self._texture is None:
            self._texture = load(PLAYER_TEXTURE_PATH)
        return self._texture

    def reset(self) -> None:
        """Reset player for a new party."""
        self.rect.x = 300
        self.rect.y = -100
        self.behavior: str = "walk"
        self.ax: float = 0
        self.ay: float = 0

    def move(self) -> None:
        """Handle player X axis movements."""
        if self.behavior == "walk":
            self.ax += 0.2 if self.ax < 4 else -0.2

        elif self.behavior == "accelerate":
            self.ax = self.max_speed_x \
                if self.ax > self.max_speed_x else self.ax + 0.6

        else:
            self.ax = 1 if self.ax <= 1 else self.ax - 0.2

    def jump(self) -> None:
        """Handle player jump."""
        if self.jump_available and self.jump_count:
            self.jump_sound.play()
            self.ay: float = -self.max_speed_y
            self.jump_count -= 1

            if not self.currently_in_jump:
                self.currently_in_jump: bool = True

            self.jump_available: bool = False

    def apply_gravity(self) -> None:
        """Handle player falling."""
        self.ay += self.gravity
        if self.ay > self.max_speed_y:
            self.ay: float = self.max_speed_y

        elif self.ay < -self.max_speed_y:
            self.ay: float = -self.max_speed_y

        self.rect.y += int(self.ay)
        self.rect.y = max(self.rect.y, 0)

    def above(self, y) -> bool:
        """Check whether the player is above a given height"""
        return self.rect.y > y

    def accelerate(self) -> None:
        """Set player behavior to gain speed."""
        self.behavior: str = "accelerate"

    def decelerate(self) -> None:
        """Set player behavior to slow down."""
        self.behavior: str = "decelerate"

    def walk(self) -> None:
        """Reset player behavior to normal."""
        self.behavior: str = "walk"
