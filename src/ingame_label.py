from typing import Tuple
import numpy as np
import pygame

from src.camera import Camera

class IngameLabel(pygame.sprite.Sprite):

    def __init__(self, font: pygame.font.Font, content: str, color, pos: Tuple[int, int], camera: Camera) -> None:
        super().__init__()
        self.font = font
        self.rendered_text = self.font.render(content, True, color)
        self.pos = pos
        self.camera = camera
        self.image = pygame.surface.Surface(self.rendered_text.get_size(), pygame.SRCALPHA).convert_alpha()
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.lifetime = 30

    def update(self, *args, **kwargs):
        super().update()
        (x, y) = self.camera.to_screen_coord(self.pos)
        self.rect.x = int(x)
        self.rect.y = int(y)
        self.image.blit(self.rendered_text, (0, 0, *self.rendered_text.get_size()))
        self.lifetime -= 1
        if self.lifetime == 0:
            self.kill()

class DamageLabel(IngameLabel):

    def __init__(self, content: str, pos: Tuple[int, int], camera: Camera) -> None:
        font = pygame.font.SysFont(pygame.font.get_default_font(), 28)
        color = (255, 0, 0, 0)
        pos = np.array(pos) + np.random.randint(30, 60, size=2)
        super().__init__(font, content, color, pos, camera)

    def update(self, *args, **kwargs):
        self.pos[1] += 1
        return super().update(*args, **kwargs)
