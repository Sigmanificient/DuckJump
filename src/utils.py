import pygame

TEXTURES_PATH: str = "assets/textures"


def load_texture(file: str, alpha: bool = True) -> pygame.Surface:
    """Loads a asset from a file and convert it into a pygame.Surface."""
    surface = pygame.image.load(f'{TEXTURES_PATH}/{file}')
    return surface.convert_alpha() if alpha else surface.convert()
