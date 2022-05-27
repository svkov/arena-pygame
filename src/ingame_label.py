from typing import Tuple
import numpy as np
import pygame

from src.camera import Camera
from src.game_config import GameConfig
from src.game_object import GameObject

class IngameLabel(pygame.sprite.Sprite):

    def __init__(self,
                 font: pygame.font.Font,
                 content: str,
                 color,
                 pos: Tuple[int, int],
                 camera: Camera,
                 image: pygame.Surface = None) -> None:
        super().__init__()
        self.font = font
        self.rendered_text = self.font.render(content, True, color)
        self.pos = pos.copy()
        self.camera = camera
        if image is None:
            self.image = pygame.surface.Surface(self.rendered_text.get_size(), pygame.SRCALPHA).convert_alpha()
            self.image.fill((0, 0, 0))
            self.image.set_colorkey((0, 0, 0))
            self.image.blit(self.rendered_text, (0, 0, *self.rendered_text.get_size()))
        else:
            self.image = image
        self.rect = self.image.get_rect()
        self.lifetime = 30

    def update(self, *args, **kwargs):
        super().update()
        (x, y) = self.camera.to_screen_coord(self.pos)
        self.rect.x = int(x)
        self.rect.y = int(y)
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

class ExpLabel(IngameLabel):

    def __init__(self, content: str, pos: Tuple[int, int], camera: Camera) -> None:
        font = pygame.font.SysFont(pygame.font.get_default_font(), 32)
        color = (0, 0, 255, 0)
        super().__init__(font, content, color, pos, camera)

    def update(self, *args, **kwargs):
        self.pos[1] -= 3
        super().update(*args, **kwargs)

class ItemLabel(IngameLabel):

    def __init__(self, content: str, pos: Tuple[int, int], camera: Camera) -> None:
        pos = np.array(pos)
        pos = camera.to_world_coord(pos)
        font = pygame.font.SysFont(pygame.font.get_default_font(), 32)
        color = (255, 255, 255, 0)
        super().__init__(font, content, color, pos, camera)
        self.lifetime = 2
        pos[0] -= self.rendered_text.get_size()[0] // 2

    def update(self, *args, **kwargs):
        (x, y) = self.camera.to_screen_coord(self.pos)
        width, height = self.rendered_text.get_size()
        # rect = [
        #     x - width // 2,
        #     y,
        #     width,
        #     height
        # ]
        # pygame.draw.rect(kwargs['screen'], '#3d3d3d', rect)
        super().update(*args, **kwargs)

class LevelUpLabel(GameObject):

    def __init__(self, pos: Tuple[int, int], camera: Camera, game_config: GameConfig) -> None:
        font_size_difference = 2
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 40)
        content = 'Level UP'
        green_color = (20, 255, 20)
        color_key = (2, 2, 2)
        # Black is not (0, 0, 0) because there is a problem
        # with black color on image and black on default mask background
        black_color = (1, 1, 1)
        self.rendered_text = self.font.render(content, False, green_color)
        self.rendered_text = self.add_outline_to_image(self.rendered_text, font_size_difference, black_color)
        text_size = self.rendered_text.get_size()
        image = pygame.image.load('assets/lvlup_arrow.png').convert_alpha()
        image_size = (128, 128)
        image = pygame.transform.scale(image, image_size)
        full_image_size = [image_size[0], image_size[1] + text_size[1]]
        self.image = pygame.Surface(full_image_size)
        self.rect = self.image.get_rect()
        self.image.fill(color_key)
        self.image.set_colorkey(color_key)
        self.image.blit(image, (0, 0))
        self.image.blit(self.rendered_text, (self.rect.centerx - text_size[0] // 2,
                                             image_size[1]))
        self.pos = pos
        self.camera = camera
        super().__init__(pos, self.image, full_image_size, camera=camera, game_config=game_config)
        self.lifetime = 90

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.pos[1] -= 3
        (x, y) = self.camera.to_screen_coord(self.pos)
        self.rect.x = int(x)
        self.rect.y = int(y)
        self.lifetime -= 1
        if self.lifetime == 0:
            self.kill()

    def add_outline_to_image(self, image: pygame.Surface,
                             thickness: int, color: tuple,
                             color_key: tuple = (255, 0, 255)) -> pygame.Surface:
        mask = pygame.mask.from_surface(image)
        mask_surf = mask.to_surface(setcolor=color)
        mask_surf.set_colorkey((0, 0, 0))

        new_img = pygame.Surface((image.get_width() + 2, image.get_height() + 2))
        new_img.fill(color_key)
        new_img.set_colorkey(color_key)

        for i in -thickness, thickness:
            new_img.blit(mask_surf, (i + thickness, thickness))
            new_img.blit(mask_surf, (thickness, i + thickness))
        new_img.blit(image, (thickness, thickness))

        return new_img
