from src.utils import load

BACKGROUND_PATH = "src/assets/images/bg.png"


class ScrollingBackground:
    _texture = None

    def __init__(self, offset):
        self.rect = self.texture.get_rect()
        self.rect.x = offset

    @property
    def texture(self):
        if self._texture is None:
            self._texture = load(BACKGROUND_PATH)
        return self._texture

    def update(self):
        self.rect.x = self.rect.x - 1 if self.rect.x > -1280 else 1280
