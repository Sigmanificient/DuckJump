from random import randrange

from src.utils import load

PLATFORM_TEXTURE_PATH = "src/assets/images/bullet-bill.png"


class Bullet:
    _texture = None

    def __init__(self):
        self.rect = self.texture.get_rect()
        self.setup()

    def setup(self):
        self.rect.x = randrange(1300, 3000)
        self.rect.y = randrange(720)

    @property
    def texture(self):
        if self._texture is None:
            self._texture = load(PLATFORM_TEXTURE_PATH)
        return self._texture

    def move(self, game):
        self.rect.x -= 2 * int(game.player.ax)

        if self.rect.x - self.rect.width > 0:
            self.setup()

    def check_hit_box(self, player):
        return self.rect.colliderect(player.rect)
