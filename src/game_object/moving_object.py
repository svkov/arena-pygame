from typing import Tuple

import numpy as np
from src.game_object import GameObject


class MovingObject(GameObject):

    def __init__(self,
                 pos: Tuple[int, int],
                 **kwargs) -> None:
        super().__init__(pos, **kwargs)
        self.speed = np.array([0, 0])

    def set_zero_speed(self):
        self.speed = np.array([0, 0])

    def normalize_speed(self):
        if self.speed_value < self.stats.movement_speed:
            return
        if self.speed_value > 0:
            self.speed = self.speed * self.stats.movement_speed / self.speed_value

    def move_world_coord(self, dt: float):
        self.pos = self.pos + self.speed * dt

    @property
    def speed_value(self):
        return np.linalg.norm(self.speed)

    @property
    def is_moving(self):
        return any(abs(self.speed) > 0)
