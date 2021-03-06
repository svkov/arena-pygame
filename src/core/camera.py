import numpy as np
from src.hud.hud_config import HUDConfig


class Camera:

    def __init__(self, x, y, screen_resolution) -> None:
        self.zoom_factor = 1
        self.min_zoom_factor = 0.1
        self.max_zoom_factor = 1.5
        self.zoom_step = 0.1
        self.x = x
        self.y = y
        screen_x = screen_resolution[0] * (1 - HUDConfig.percent_to_hud)
        self.screen_resolution = np.array([screen_x, screen_resolution[1]])

    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def get_pos(self):
        return (self.x, self.y)

    def get_pos_arr(self):
        return np.array(self.get_pos())

    def to_screen_coord(self, pos):
        self_pos = self.get_pos_arr()
        pos = np.array(pos)
        return (pos - self_pos - 64) * self.zoom_factor + self.screen_resolution // 2

    def to_world_coord(self, pos):
        self_pos = self.get_pos_arr()
        pos = np.array(pos)
        # works ALMOST properly
        return (pos - self.screen_resolution // 2) / self.zoom_factor + self_pos + 64 * self.zoom_factor

    def image_size_with_zoom(self, original_image_size):
        return (np.array(original_image_size) * self.zoom_factor).astype(np.int)

    def get_all_zoom_factors(self):
        lower_bound = int(self.min_zoom_factor * 10)
        upper_bound = int(self.max_zoom_factor * 10)
        return [round(zoom / 10, 1) for zoom in range(lower_bound, upper_bound + 1)]

    def zoom_in(self):
        self.clip_zoom(self.zoom_factor - self.zoom_step)

    def zoom_out(self):
        self.clip_zoom(self.zoom_factor + self.zoom_step)

    def clip_zoom(self, new_zoom_factor):
        self.zoom_factor = round(np.clip(new_zoom_factor, self.min_zoom_factor, self.max_zoom_factor), 1)
