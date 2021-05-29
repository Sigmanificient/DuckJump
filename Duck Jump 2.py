from random import randrange

import pygame

__release__ = "04/05/2020"
__version__ = 2.0


class Game:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1280, 720))

        pygame.display.set_icon(load("assets/images/icon.png"))
        self.font = {size: pygame.font.Font("assets/fonts/setbackt.ttf", size) for size in (48, 64, 96, 128)}

        self.show_fps = True
        self.player = Player()

        self.run = True
        self.pause = False
        self.over = False

        self.textures = {
            "bg": load("assets/images/bg.png"),
            "platform": load("assets/images/platform.png"),
            "bullet": load("assets/images/bullet-bill.png")
        }

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

    def setup(self):
        pygame.mixer.music.load("assets/musics/Smash_Brothers.wav")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play()

        self.platforms = [Platform(x, y) for x, y in ((280, 620), (960, 640), (1620, 660))]
        self.bullets = [Bullet() for _ in range(3)]
        self.player.reset()
        self.backgrounds = [ScrollingBackground(1280), ScrollingBackground(0)]
        self.over = False
        self.limit = 4000
        self.score = 0

    def toggle_fps(self):
        self.show_fps = False if self.show_fps else True

    def main(self):
        self.setup()

        while self.run:
            self.screen.fill((121, 201, 249), ((0, 0), (1280, 360)))
            self.screen.fill((127, 173, 113), ((0, 593), (1280, 720)))
            for background in self.backgrounds:
                background.update()
                self.screen.blit(self.textures["bg"], (background.rect.x, 350), (0, 0, 1280, 360))

            for platform in self.platforms:
                platform.check_hit_box()
                platform.move()
                self.screen.blit(self.textures["platform"], platform.rect)

            self.player.move()
            self.player.apply_gravity()
            self.screen.blit(self.player.texture, self.player.rect)

            for bullet in self.bullets:
                bullet.move()
                self.screen.blit(game.textures["bullet"], bullet.rect)
                bullet.check_hitbox()

            if len(self.bullets) < 3:
                self.bullets.append(Bullet())

            pygame.draw.rect(self.screen, (255, 255, 255), ((5, 5), (1270, 710)), 3)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in self.events:
                        self.events[event.key]()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.player.jump_available = True
                    elif event.key == pygame.K_a or event.key == pygame.K_d:
                        self.player.walk()

                elif event.type == pygame.QUIT:
                    self.run = False

            if self.over:
                self.over_screen()

            else:
                pygame.display.set_caption(
                    f"Duck Jump 2 by Sigmanificient Corp. | score : {self.score}"
                    + f"| {self.clock.get_fps()} " * self.show_fps
                )

                pygame.display.update()
                self.score += int(self.player.ax)
                self.clock.tick(100)

    def pause_screen(self):
        pygame.mixer.music.pause()
        self.fade((0, 128, 255, 1), 64)
        pygame.display.set_caption("Duck Jump 2 by Sigmanificient Corp. | score : %i | Paused" % self.score)
        self.screen.blit(*get_text("Paused", self.font[96], (255, 255, 255), (640, 300), centered=True))
        self.screen.blit(
            *get_text("press escape to unpause", self.font[48], (255, 255, 255), (640, 400), centered=True))
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
        pygame.display.set_caption("Duck Jump 2 by Sigmanificient Corp. | score : %i | GameOver" % self.score)
        self.screen.blit(*get_text("Game Over", self.font[96], (255, 255, 255), (640, 300), centered=True))
        self.screen.blit(*get_text("press space to retry", self.font[48], (255, 255, 255), (640, 400), centered=True))
        pygame.display.update()

        self.pause = True
        while self.pause:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.setup()
                    self.pause = False

            elif event.type == pygame.QUIT:
                self.pause = False
                self.run = False

    def fade(self, c, iterations):
        alpha_layer = pygame.Surface((1280, 720), pygame.SRCALPHA)
        alpha_layer.fill(c)
        for iteration in range(iterations):
            self.screen.blit(alpha_layer, (0, 0))
            pygame.draw.rect(self.screen, (255, 255, 255), ((5, 5), (1270, 710)), 3)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    break

            pygame.display.update()


class Platform:

    def __init__(self, x, y):
        self.rect = game.textures["platform"].get_rect()
        self.rect.x, self.rect.y = x, y
        self.initial_y = self.rect.y

    def move(self):
        if self.rect.x < -500:
            self.rect.x = max([platform.rect.x for platform in game.platforms]) + randrange(600, 1000)
            self.rect.y = randrange(400, 620)
            self.initial_y = self.rect.y

        else:
            self.rect.x -= int(game.player.ax)

    def check_hit_box(self):
        if any(
                [
                    self.rect.collidepoint(game.player.rect.x, game.player.rect.y + 68),
                    self.rect.collidepoint(game.player.rect.x + 50, game.player.rect.y + 68)
                ]
        ):

            game.player.rect.y = self.rect.y - 68 + 1
            game.player.jump_count = 1
            self.rect.x += randrange(0, 2) - 1
            self.rect.y += 2

        else:
            if self.rect.y > self.initial_y:
                self.rect.y -= 1

        if any([self.rect.collidepoint(game.player.rect.x + 50, game.player.rect.y),
                self.rect.collidepoint(game.player.rect.x + 50, game.player.rect.y + 66)]):
            game.player.rect.x = self.rect.x - 51
            if game.player.rect.x < 0:
                game.over = True


class ScrollingBackground:

    def __init__(self, offset):
        self.rect = game.textures["bg"].get_rect()
        self.rect.x = offset

    def update(self):
        self.rect.x = self.rect.x - 1 if self.rect.x > -1280 else 1280


class Bullet:

    def __init__(self):
        self.rect = game.textures["bullet"].get_rect()
        self.rect.x, self.rect.y = randrange(1300, 3000), randrange(720)

    def move(self):
        if self.rect.x < -50:
            self.rect.x = randrange(1300, 3000)
            self.rect.y = randrange(100, 620)
        else:
            self.rect.x -= 2 * int(game.player.ax)

    def check_hitbox(self):
        if self.rect.colliderect(game.player.rect):
            print(game.player.rect)
            game.over = True


class Player:

    def __init__(self):
        self.jump_sound = pygame.mixer.Sound("assets/sounds/jump.wav")
        self.texture = load("assets/images/duck3.png")
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
            self.ax = self.max_speed_x if self.ax > self.max_speed_x else self.ax + 0.6

        else:
            self.ax = 1 if self.ax <= 1 else self.ax - 0.2

    def jump(self):
        if self.jump_available and self.jump_count:
            self.jump_sound.play()
            self.ay = -self.max_speed_y
            self.jump_count -= 1
            if self.currently_in_jump:
                self.jump_available = False
            else:
                self.currently_in_jump = True
                self.jump_available = False

    def apply_gravity(self):

        self.ay += self.gravity
        if self.ay > self.max_speed_y:
            self.ay = self.max_speed_y

        elif self.ay < -self.max_speed_y:
            self.ay = -self.max_speed_y

        self.rect.y += int(self.ay)
        if self.rect.y < 0:
            self.rect.y = 0

        elif self.rect.y > 720:
            game.over = True

    def accelerate(self):
        self.behavior = "accelerate"

    def decelerate(self):
        self.behavior = "decelerate"

    def walk(self):
        self.behavior = "walk"


def load(path, alpha=True):
    return pygame.image.load(path).convert_alpha() if alpha else pygame.image.load(path).convert()


def get_text(text, font, c, pos, centered=False):
    text = font.render(text, True, c, None)
    text_rect = text.get_rect()
    if centered:
        text_rect.center = pos
    else:
        text_rect.x, text_rect.y = pos
    return text, text_rect


if __name__ == "__main__":
    game = Game()
    game.main()
