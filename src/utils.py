import pygame


def load(path, alpha=True):
    return pygame.image.load(path).convert_alpha() \
        if alpha else pygame.image.load(path).convert()


def get_text(text, font, c, pos, centered=False):
    text = font.render(text, True, c, None)
    text_rect = text.get_rect()
    if centered:
        text_rect.center = pos
    else:
        text_rect.x, text_rect.y = pos
    return text, text_rect
