from random import randrange

from src.utils import load


class Platform:
    _texture = None

    def __init__(self, x, y):
        self.rect = self.texture.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.initial_y = self.rect.y

    @property
    def texture(self):
        if self._texture is None:
            self._texture = load("src/assets/images/platform.png")
        return self._texture

    def move(self, game):
        if self.rect.x < -500:
            self.rect.x = self.rect.x = max(
                platform.rect.x for platform in game.platforms
            ) + randrange(600, 1000)

            self.rect.y = randrange(400, 620)
            self.initial_y = self.rect.y

        else:
            self.rect.x -= int(game.player.ax)

    def check_hit_box(self, game):
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
