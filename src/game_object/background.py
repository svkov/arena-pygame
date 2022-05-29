import numpy as np
from src.game_object import GameObject
from src.groups import GameStateGroups


class Background(GameObject):

    def __init__(self, pos, image, image_size=None, **kwargs) -> None:
        super().__init__(pos, image, image_size, **kwargs)
        self.radius = kwargs['radius']
        self.groups_global: GameStateGroups = kwargs['groups']
        self.distance_from_player = max(self.game_config.screen_resolution)

    def update(self, *args, **kwargs):
        if self.is_far_from_player():
            self.unmount_from_screen()
        else:
            self.mount_to_screen()
        super().update(*args, **kwargs)

    def is_far_from_player(self):
        camera_screen_pos = self.camera.to_screen_coord(self.camera.get_pos_arr())
        return np.linalg.norm(np.array(self.center_screen) - camera_screen_pos) > self.distance_from_player

    def unmount_from_screen(self):
        self.groups_global.visible_background_group.remove(self)

    def mount_to_screen(self):
        self.groups_global.visible_background_group.add(self)
