from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
import numpy as np
import pygame

from src.game_object import GameObject

if TYPE_CHECKING:
    from src.core.camera import Camera
    from src.config.game_config import GameConfig
    from src.item import InventoryItem

class IngameLabel(pygame.sprite.Sprite):

    def __init__(self,
                 font: pygame.font.Font,
                 content: str,
                 color,
                 pos: Tuple[int, int],
                 camera: Camera,
                 image: pygame.Surface = None,
                 rendered_text: pygame.Surface = None) -> None:
        super().__init__()
        self.font = font
        if rendered_text is None:
            self.rendered_text = self.font.render(content, True, color)
        else:
            self.rendered_text = rendered_text
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
        self.update_pos()

    def update_pos(self):
        (x, y) = self.camera.to_screen_coord(self.pos)
        self.rect.x = int(x)
        self.rect.y = int(y)
        self.update_lifetime()

    def update_lifetime(self):
        self.lifetime -= 1
        if self.lifetime == 0:
            self.kill()

class DamageLabel(IngameLabel):

    def __init__(self, content: str, pos: Tuple[int, int], camera: Camera, color=(255, 0, 0, 0)) -> None:
        font = pygame.font.SysFont(pygame.font.get_default_font(), 28)
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

    def __init__(self, item: InventoryItem, pos: Tuple[int, int], camera: Camera, with_image=True) -> None:
        font = pygame.font.SysFont(pygame.font.get_default_font(), 32)
        italic_font = pygame.font.SysFont(pygame.font.get_default_font(), 25, italic=True)
        color = (255, 255, 255, 0)
        image = self.get_image(item, font, color, italic_font, with_image)
        super().__init__(font, item.description, color, np.array(pos), camera, image, self.item_name)
        self.lifetime = 2
        self.pos[0] -= self.width + 5
        self.pos[1] -= self.height + 5

    def get_image(self, item: InventoryItem, font, color, italic_font, with_image):
        text_to_blit = self.get_text_to_blit(item, font, color, italic_font)
        return self.get_image_by_text_to_blit(item, text_to_blit, with_image)

    def get_text_to_blit(self, item, font, color, italic_font):
        self.item_name = font.render(item.name, True, color)
        self.item_description = italic_font.render(item.description, True, color)
        if hasattr(item, 'stats'):
            self.item_stats = font.render(str(item.stats), True, color)
        else:
            self.item_stats = pygame.Surface([0, 0])
        self.item_rare = italic_font.render(item.item_rare_name, True, color)

        text_to_blit = [
            self.item_name,
            self.item_stats,
            self.item_rare,
            self.item_description,
        ]
        return text_to_blit

    def get_image_by_text_to_blit(self, item, text_to_blit, blit_with_item_image=True):
        text_sizes = [text.get_size() for text in text_to_blit]

        image_size = item.image.get_size()
        margin = 5

        max_between_x = max(map(lambda x: x[0], text_sizes))
        sum_ = sum(map(lambda x: x[1], text_sizes))
        if blit_with_item_image:
            sum_over_y = max(sum_, image_size[1])
        else:
            sum_over_y = sum_
        three_margin = margin * 3

        self.width = max_between_x + image_size[0] + three_margin
        self.height = sum_over_y + margin * (len(text_to_blit) + 1)

        image = self.get_empty_image(self.width, self.height, item.item_rare_color)
        if blit_with_item_image:
            image = self.blit_text_with_image(image, text_to_blit, margin, item.image)
        else:
            image = self.blit_text_without_image(image, text_to_blit, margin)
        return image

    def blit_text_with_image(self, image, text_to_blit, margin, item_image):
        image_size = item_image.get_size()
        image.blit(item_image, [margin, self.height // 2 - image_size[1] // 2])
        current_y = margin
        for text in text_to_blit:
            image.blit(text, (margin * 2 + image_size[0], current_y))
            current_y += margin + text.get_size()[1]
        return image

    def blit_text_without_image(self, image, text_to_blit, margin):
        current_y = margin
        for text in text_to_blit:
            image.blit(text, (margin * 2, current_y))
            current_y += margin + text.get_size()[1]
        return image

    def get_empty_image(self, width, height, color=(0, 0, 0)):
        image = pygame.surface.Surface((width, height))
        image.fill(color)
        pygame.draw.rect(image, (0, 0, 0), [0, 0, width - 1, height - 1], width=2)
        return image

    def update(self, *args, **kwargs):
        x, y = self.pos
        self.rect.x = int(x)
        self.rect.y = int(y)
        self.update_lifetime()

class ItemNameLabel(ItemLabel):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, with_image=False, **kwargs)

    def get_text_to_blit(self, item, font, color, italic_font):
        self.item_name = font.render(item.name, True, color)
        return [self.item_name]
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
