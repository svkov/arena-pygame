from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

import numpy as np
import pygame
import src.utils as utils

if TYPE_CHECKING:
    from src.core.camera import Camera
    from src.config.game_config import GameConfig
    from src.core.groups import GameStateGroups

class GameObject(pygame.sprite.Sprite):

    def __init__(self,
                 pos: Tuple[int, int],
                 image: pygame.surface.Surface,
                 image_size: Tuple[int, int] = None,
                 camera: Camera = None,
                 pos_in_world_coord: bool = True,
                 angle: int = 0,
                 game_config: GameConfig = None,
                 groups: GameStateGroups = None,
                 **kwargs) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.pos = np.array(pos, dtype=np.float)
        self.rotation_angle = angle
        self.camera = camera
        self.image_size = image_size
        if image_size is None:
            self.image_size = (128, 128)
        self.groups = groups

        center = self.camera.to_screen_coord(self.pos)

        self.image: pygame.surface.Surface = image
        if self.rotation_angle == 0:
            self.image = image
            self.rect = self.image.get_rect()
        else:
            self.image, self.rect = self.rot_center(image, self.rotation_angle, center)

        self.image_by_zoom = utils.preresize_image(self.image, self.camera, self.image_size)
        self.game_config = game_config
        self.draw_debug_rects()

        if pos_in_world_coord:
            self.update_screen_coord()
        else:
            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]

    def update(self, *args, **kwargs):
        self.update_zoom()
        self.update_screen_coord()

    def update_screen_coord(self):
        new_pos = self.camera.to_screen_coord(self.pos)
        self.rect.x = int(new_pos[0])
        self.rect.y = int(new_pos[1])

    def draw_debug_rects(self):
        if self.game_config.draw_rects:
            for zoom_factor, image in self.image_by_zoom.items():
                zoomed_image_size = (
                    self.image_size[0] * zoom_factor,
                    self.image_size[1] * zoom_factor
                )
                rect = [0, 0, zoomed_image_size[0], zoomed_image_size[1]]
                pygame.draw.rect(image, (255, 0, 0), rect, width=3)
        self.image = self.image_by_zoom[self.camera.zoom_factor]

    def update_zoom(self):
        if self.image != self.image_by_zoom[self.camera.zoom_factor]:
            self.image = self.image_by_zoom[self.camera.zoom_factor]
            new_width = int(self.camera.zoom_factor * self.image_size[0])
            new_height = int(self.camera.zoom_factor * self.image_size[1])
            self.rect.width = new_width
            self.rect.height = new_height

    def set_image_size(self, new_image_size: Tuple[int, int]):
        self.image_size = new_image_size
        self.image = pygame.transform.scale(self.image, self.image_size)

    @property
    def current_image(self) -> pygame.surface.Surface:
        return self.image_by_zoom[self.camera.zoom_factor]

    def rot_center(self, image, angle, center) -> Tuple[pygame.surface.Surface, pygame.rect.Rect]:
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(center=center).center)
        return rotated_image, new_rect

    @property
    def center_world(self) -> Tuple[float, float]:
        return (self.pos[0] + self.image_size[0] // 2,
                self.pos[1] + self.image_size[1] // 2)

    @property
    def center_screen(self) -> Tuple[int, int]:
        return (int(self.rect.x + self.image_size[0] // 2),
                int(self.rect.y + self.image_size[1]) // 2)

    @property
    def pos_right(self) -> int:
        return self.pos[0] + self.image_size[0]

    @pos_right.setter
    def pos_right(self, value: float):
        self.pos[0] = value - self.image_size[0]

    @property
    def pos_left(self) -> float:
        return self.pos[0]

    @pos_left.setter
    def pos_left(self, value: float):
        self.pos[0] = value

    @property
    def pos_top(self) -> float:
        return self.pos[1]

    @pos_top.setter
    def pos_top(self, value: float):
        self.pos[1] = value

    @property
    def pos_bottom(self) -> float:
        return self.pos[1] + self.image_size[1]

    @pos_bottom.setter
    def pos_bottom(self, value: float):
        self.pos[1] = value - self.image_size[1]

    def on_collision(self, obj: GameObject):
        pass

    @property
    def damage(self) -> float:
        return 0
