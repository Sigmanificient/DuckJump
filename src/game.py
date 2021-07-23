import pygame

from src.components.bullet import Bullet
from src.components.platform import Platform
from src.components.player import Player
from src.components.scrolling_background import ScrollingBackground
from src.utils import load, get_text


class Game:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1280, 720))

        pygame.display.set_icon(load("src/assets/images/icon.png"))
        self.font = {
            size: pygame.font.Font("src/assets/fonts/setbackt.ttf", size)
            for size in (48, 64, 96, 128)
        }

        self.show_fps = True
        self.player = Player()

        self.run = True
        self.pause = False
        self.over = False

        self.events = {
            pygame.K_ESCAPE: self.pause_screen,
            pygame.K_SPACE: self.player.jump,
            pygame.K_d: self.player.accelerate,
            pygame.K_a: self.player.decelerate,
            pygame.K_f: self.toggle_fps
        }

        self.platforms = []
        self.bullets = []
        self.backgrounds = []
        self.limit = 4000
        self.score = 0

        self.cap_fps = 100

    def setup(self):
        pygame.mixer.music.load("src/assets/musics/music.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play()

        self.platforms = [
            Platform(x, y) for x, y in ((280, 620), (960, 640), (1620, 660))
        ]

        self.bullets = [Bullet() for _ in range(3)]
        self.player.reset()
        self.backgrounds = [ScrollingBackground(1280), ScrollingBackground(0)]
        self.over = False
        self.limit = 4000
        self.score = 0

    def toggle_fps(self):
        self.show_fps = not self.show_fps

    def update(self):
        self.screen.fill((121, 201, 249), ((0, 0), (1280, 360)))
        self.screen.fill((127, 173, 113), ((0, 593), (1280, 720)))
        for background in self.backgrounds:
            background.update()
            self.screen.blit(
                background.texture,
                (background.rect.x, 350),
                (0, 0, 1280, 360)
            )

        for platform in self.platforms:
            platform.check_hit_box(self)
            platform.move(self)
            self.screen.blit(platform.texture, platform.rect)

        self.player.move()
        self.player.apply_gravity()

        if self.player.above(720):
            self.over = True

        self.screen.blit(self.player.texture, self.player.rect)

        for bullet in self.bullets:
            bullet.move(self)
            self.screen.blit(bullet.texture, bullet.rect)

            if bullet.check_hit_box(self.player):
                self.over = True
                break

        if len(self.bullets) < 3:
            self.bullets.append(Bullet())

        pygame.draw.rect(
            self.screen, (255, 255, 255), ((5, 5), (1270, 710)), 3
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                return

            if event.type == pygame.KEYDOWN:
                if event.key in self.events:
                    self.events[event.key]()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.player.jump_available = True

                elif event.key in [pygame.K_a, pygame.K_d]:
                    self.player.walk()

    def main(self):
        self.setup()

        while self.run:
            self.update()
            self.handle_events()

            if self.over:
                self.over_screen()

            else:
                self.draw()

    def draw(self):
        pygame.display.set_caption(
            f"Duck Jump 2 | score : {self.score}"
            + f" | {self.clock.get_fps()} " * self.show_fps
        )

        pygame.display.update()
        self.score += int(self.player.ax)
        self.clock.tick(self.cap_fps)

    def pause_screen(self):
        pygame.mixer.music.pause()
        self.fade((0, 128, 255, 1), 64)
        pygame.display.set_caption(
            "Duck Jump 2 | score : %i | Paused" % self.score
        )

        self.screen.blit(
            *get_text(
                "Paused",
                self.font[96],
                (255, 255, 255),
                (640, 300),
                centered=True)
        )

        self.screen.blit(
            *get_text(
                "press escape to unpause",
                self.font[48],
                (255, 255, 255),
                (640, 400),
                centered=True
            )
        )
        pygame.display.update()

        self.pause = True
        while self.pause:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.unpause()
                    pygame.event.clear()
                    self.pause = False

            elif event.type == pygame.QUIT:
                self.pause = False
                self.run = False

    def over_screen(self):
        pygame.mixer.music.pause()
        self.fade((255, 32, 32, 1), 128)
        pygame.display.set_caption(
            "Duck Jump 2 | score : %i | GameOver" % self.score
        )

        self.screen.blit(
            *get_text(
                "Game Over",
                self.font[96],
                (255, 255, 255),
                (640, 300),
                centered=True
            )
        )

        self.screen.blit(
            *get_text(
                "press space to retry",
                self.font[48],
                (255, 255, 255),
                (640, 400),
                centered=True
            )
        )

        pygame.display.update()

        self.pause = True
        while self.pause:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.setup()
                    self.pause = False

            elif event.type == pygame.QUIT:
                self.pause = False
                self.run = False

    def fade(self, c, iterations):
        alpha_layer = pygame.Surface((1280, 720), pygame.SRCALPHA)
        alpha_layer.fill(c)

        for _ in range(iterations):
            self.screen.blit(alpha_layer, (0, 0))

            pygame.draw.rect(
                self.screen, (255, 255, 255), ((5, 5), (1270, 710)), 3
            )

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    break

            pygame.display.update()
