from typing import Tuple, Dict, Callable, List

import Background as Background
import pygame

from src.components.bullet import Bullet
from src.components.platform import Platform
from src.components.player import Player
from src.components.scrolling_background import ScrollingBackground
from src.utils import load, get_text

ASSETS_DIR: str = "src/assets/"
MUSIC_PATH: str = f"{ASSETS_DIR}musics/music.mp3"
ICON_PATH: str = f"{ASSETS_DIR}images/icon.png"
FONT_PATH: str = f"{ASSETS_DIR}fonts/setbackt.ttf"

TITLE: str = "Duck Jump 2"
CAP_FPS: int = 100

SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 720
SCREEN_SIZE: Tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT)


class Game:
    """The Game Controller that include core mechanics."""

    def __init__(self) -> None:
        """Initialises assets, refer events and create the window."""
        pygame.init()
        pygame.mixer.init()

        self.clock: pygame.time.Clock = pygame.time.Clock()
        
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_icon(load(ICON_PATH))

        self.fonts: Dict[int, pygame.Font] = {
            size: pygame.font.Font(FONT_PATH, size) for size in (48, 64, 96)
        }

        self.show_fps: bool = True
        self.player: Player = Player()

        self.run: bool = True
        self.pause: bool = False
        self.over: bool = False

        self.events: Dict[pygame.Event, Callable[[], None]] = {
            pygame.K_ESCAPE: self.pause_screen,
            pygame.K_SPACE: self.player.jump,
            pygame.K_d: self.player.accelerate,
            pygame.K_a: self.player.decelerate,
            pygame.K_f: self.toggle_fps
        }

        self.platforms: List[Platform] = []
        self.bullets: List[Bullet] = []
        self.backgrounds: List[ScrollingBackground] = []
        self.limit: int = 4000
        self.score: int = 0

    def __del__(self) -> None:
        """Quitting pygame for proper cleanup."""
        pygame.mixer.quit()
        pygame.display.quit()
        pygame.quit()

    def setup(self) -> None:
        """Initialises a new party."""
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play()

        self.platforms: List[Platform] = [
            Platform(x, y) for x, y in ((280, 620), (960, 640), (1620, 660))
        ]

        self.bullets: List[Bullet] = [Bullet() for _ in range(3)]

        self.backgrounds: List[ScrollingBackground] = [
            ScrollingBackground(0), ScrollingBackground(SCREEN_WIDTH)
        ]

        self.player.reset()

        self.over: bool = False
        self.limit: int = 4000
        self.score: int = 0

    def toggle_fps(self) -> None:
        """Toggle a fps meter in the title bar."""
        self.show_fps: bool = not self.show_fps

    def update(self) -> None:
        """The main loop content, ran each frame."""
        self.screen.fill((121, 201, 249), ((0, 0), (SCREEN_WIDTH, 360)))
        self.screen.fill((127, 173, 113), ((0, 593), SCREEN_SIZE))

        for background in self.backgrounds:
            background.update()
            self.screen.blit(
                background.texture,
                (background.rect.x, 350),
                (0, 0, SCREEN_WIDTH, 360)
            )

        for platform in self.platforms:
            platform.check_hit_box(self)
            platform.move(self)
            self.screen.blit(platform.texture, platform.rect)

        self.player.move()
        self.player.apply_gravity()

        if self.player.above(SCREEN_HEIGHT):
            self.over: bool = True

        self.screen.blit(self.player.texture, self.player.rect)

        for bullet in self.bullets:
            bullet.move(self)
            self.screen.blit(bullet.texture, bullet.rect)

            if bullet.check_hit_box(self.player):
                self.over: bool = True
                break

        if len(self.bullets) < 3:
            self.bullets.append(Bullet())

        pygame.draw.rect(
            self.screen, (255, 255, 255), ((5, 5), (1270, 710)), 3
        )

    def handle_events(self) -> None:
        """A method to handle player interactions."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run: bool = False
                return

            if event.type == pygame.KEYDOWN:
                if event.key in self.events:
                    self.events[event.key]()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.player.jump_available = True

                elif event.key in [pygame.K_a, pygame.K_d]:
                    self.player.walk()

    def main(self) -> None:
        """Game entry point."""
        self.setup()

        while self.run:
            self.update()
            self.handle_events()

            if self.over:
                self.over_screen()

            else:
                self.draw()

    def draw(self) -> None:
        """Refreshes the screen, update the score and title, then sync fps."""
        pygame.display.set_caption(
            f"{TITLE} | score : {self.score}"
            + (f" | {self.clock.get_fps():,.3f} " * self.show_fps)
        )

        pygame.display.update()
        self.score += int(self.player.ax)
        self.clock.tick(CAP_FPS)

    def pause_screen(self) -> None:
        """Screen show when player pause the game"""
        pygame.mixer.music.pause()
        self.fade((0, 128, 255, 1), 64)
        pygame.display.set_caption(f"{TITLE} | score: {self.score} | Paused")

        self.screen.blit(
            *get_text(
                "Paused",
                self.fonts[96],
                (255, 255, 255),
                (640, 300),
                centered=True)
        )

        self.screen.blit(
            *get_text(
                "press escape to unpause",
                self.fonts[48],
                (255, 255, 255),
                (640, 400),
                centered=True
            )
        )
        pygame.display.update()

        self.pause: bool = True
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

    def over_screen(self) -> None:
        """Screen shown on player death."""
        pygame.mixer.music.pause()
        self.fade((255, 32, 32, 1), 128)
        pygame.display.set_caption(f"{TITLE} | GameOver")

        self.screen.blit(
            *get_text(
                "Game Over",
                self.fonts[96],
                (255, 255, 255),
                (640, 300),
                centered=True
            )
        )

        self.screen.blit(
            *get_text(
                "press space to retry",
                self.fonts[48],
                (255, 255, 255),
                (640, 400),
                centered=True
            )
        )

        pygame.display.update()

        self.pause: bool = True
        while self.pause:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.setup()
                    self.pause = False

            elif event.type == pygame.QUIT:
                self.pause = False
                self.run = False

    def fade(self, color: Tuple[int, int, int], iterations: int) -> None:
        """Screen fade transition between game states."""
        alpha_layer = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        alpha_layer.fill(color)

        for _ in range(iterations):
            self.screen.blit(alpha_layer, (0, 0))

            pygame.draw.rect(
                self.screen, (255, 255, 255), ((5, 5), (1270, 710)), 3
            )

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    break

            pygame.display.update()
