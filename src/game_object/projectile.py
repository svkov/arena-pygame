from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
import numpy as np
import pygame
from src.game_object.moving_object import MovingObject

if TYPE_CHECKING:
    from src.game_object.actor import Actor
    from src.core.camera import Camera
    from src.game_object import GameObject
    from src.config.game_config import GameConfig

class Projectile(MovingObject):

    def __init__(self,
                 pos: Tuple[int, int],
                 speed: np.ndarray,
                 image: pygame.surface.Surface,
                 image_size: Tuple[int, int] = None,
                 range: float = 500,
                 owner: Actor = None,
                 **kwargs):
        super().__init__(pos, image=image, image_size=image_size, **kwargs)
        self.speed = speed
        self.dist = 0
        self.range = range
        self.owner = owner

    def update(self, *args, **kwargs):
        dt = kwargs['dt']
        if self.dist < self.range:
            self.move_world_coord(dt)
            new_pos = self.camera.to_screen_coord(self.pos)
            self.rect.x = int(new_pos[0])
            self.rect.y = int(new_pos[1])
            self.dist += np.linalg.norm(self.speed * dt)
        else:
            self.kill()

    def on_collision(self, obj):
        self.kill()

    @property
    def damage(self):
        return self.owner.damage

    @classmethod
    def shoot(cls: Projectile,
              owner_obj: GameObject,
              target_pos: Tuple[float, float],
              camera: Camera,
              image: pygame.surface.Surface,
              speed: float = 1,
              image_size: Tuple[int, int] = None,
              config: GameConfig = None):
        if image_size is None:
            image_size = (32, 32)
        image_size = np.array(image_size)
        target_pos = np.array(target_pos)
        target_world_pos = camera.to_world_coord(target_pos)

        corrected_image_size = image_size * camera.zoom_factor
        target_world_pos = target_world_pos - corrected_image_size / 2
        direction = target_world_pos - owner_obj.center_world
        speed_vector = direction * speed / np.linalg.norm(direction)
        return cls(owner_obj.center_world,
                   speed_vector,
                   image=image,
                   image_size=image_size,
                   owner=owner_obj,
                   camera=camera,
                   game_config=config)
