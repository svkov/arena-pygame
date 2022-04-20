import numpy as np
from src.hud_config import HUDConfig


class Camera:

    def __init__(self, x, y, screen_resolution) -> None:
        self.x = x
        self.y = y
        screen_x = screen_resolution[0] * (1 - HUDConfig.percent_to_hud)
        self.screen_resolution = np.array([screen_x, screen_resolution[1]])

    def get_pos(self):
        return (self.x, self.y)

    def get_pos_arr(self):
        return np.array(self.get_pos())

    def to_screen_coord(self, pos):
        return np.array(pos) - self.get_pos_arr() + self.screen_resolution // 2 - 64

    def to_world_coord(self, pos):
        return np.array(pos) + self.get_pos_arr() - self.screen_resolution // 2 - 64
