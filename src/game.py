import pygame

from src.utils import load_texture


ICON_PATH: str = "icon/icon.ico"


class Game:

    def __init__(self):
        self.height = 1280
        self.width = 720

        self.screen = pygame.display.set_mode((self.height, self.width))
        self.clock = pygame.time.Clock()

        pygame.display.set_icon(load_texture(ICON_PATH))

        self.is_running = False

        self.max_fps = 60

    def main(self) -> None:
        """Game entry point."""
        self.is_running = True

        while self.is_running:
            self.update()

            for event in pygame.event.get():
                self.handle_event(event)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.is_running = False
            return

    def update(self):
        pygame.display.update()
        self.clock.tick(self.max_fps)
