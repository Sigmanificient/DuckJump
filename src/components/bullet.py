from random import randrange

from src.utils import load


class Bullet:
    _texture = None

    def __init__(self):
        self.rect = self.texture.get_rect()
        self.rect.x, self.rect.y = randrange(1300, 3000), randrange(720)

    @property
    def texture(self):
        if self._texture is None:
            self._texture = load("src/assets/images/bullet-bill.png")
        return self._texture

    def move(self, game):
        if self.rect.x < -50:
            self.rect.x = randrange(1300, 3000)
            self.rect.y = randrange(100, 620)
        else:
            self.rect.x -= 2 * int(game.player.ax)

    def check_hit_box(self, player):
        return self.rect.colliderect(player.rect)