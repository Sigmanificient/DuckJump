import pygame

from src.utils import load

PLAYER_SOUND_PATH = "src/assets/sounds/jump.wav"
PLAYER_TEXTURE_PATH = "src/assets/images/duck3.png"


class Player:
    _texture = None

    def __init__(self):
        self.jump_sound = pygame.mixer.Sound(PLAYER_SOUND_PATH)
        self.rect = self.texture.get_rect()
        self.rect.x, self.rect.y = 300, -100

        self.ax = 0
        self.ay = 0
        self.gravity = 0.1
        self.max_speed_y = 8
        self.max_speed_x = 10
        self.jump_count = 2
        self.currently_in_jump = False
        self.jump_available = True
        self.behavior = "walk"

    @property
    def texture(self):
        if self._texture is None:
            self._texture = load(PLAYER_TEXTURE_PATH)
        return self._texture

    def reset(self):
        self.rect.x = 300
        self.rect.y = -100
        self.behavior = "walk"
        self.ax = 0
        self.ay = 0

    def move(self):
        if self.behavior == "walk":
            self.ax += 0.2 if self.ax < 4 else -0.2

        elif self.behavior == "accelerate":
            self.ax = self.max_speed_x \
                if self.ax > self.max_speed_x else self.ax + 0.6

        else:
            self.ax = 1 if self.ax <= 1 else self.ax - 0.2

    def jump(self):
        if self.jump_available and self.jump_count:
            self.jump_sound.play()
            self.ay = -self.max_speed_y
            self.jump_count -= 1

            if not self.currently_in_jump:
                self.currently_in_jump = True

            self.jump_available = False

    def apply_gravity(self):
        self.ay += self.gravity
        if self.ay > self.max_speed_y:
            self.ay = self.max_speed_y

        elif self.ay < -self.max_speed_y:
            self.ay = -self.max_speed_y

        self.rect.y += int(self.ay)
        self.rect.y = max(self.rect.y, 0)

    def above(self, y):
        return self.rect.y > y

    def accelerate(self):
        self.behavior = "accelerate"

    def decelerate(self):
        self.behavior = "decelerate"

    def walk(self):
        self.behavior = "walk"
