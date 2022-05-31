import numpy as np
from src.game_object import GameObject
from src.core.groups import GameStateGroups


class Background(GameObject):

    def __init__(self,
                 pos,
                 radius=3500,
                 groups: GameStateGroups = None,
                 **kwargs) -> None:
        super().__init__(pos, **kwargs)
        self.radius = radius
        self.groups_global: GameStateGroups = groups
        self.max_distance_from_player = max(self.game_config.screen_resolution)

    def update(self, *args, **kwargs):
        self.show_if_close_to_player()
        super().update(*args, **kwargs)

    def show_if_close_to_player(self):
        if self.is_far_from_player():
            self.unmount_from_screen()
        else:
            self.mount_to_screen()

    def is_far_from_player(self):
        camera_screen_pos = self.camera.to_screen_coord(self.camera.get_pos_arr())
        screen_center = np.linalg.norm(np.array(self.center_screen) - camera_screen_pos)
        return screen_center > self.max_distance_from_player

    def unmount_from_screen(self):
        self.groups_global.visible_background_group.remove(self)

    def mount_to_screen(self):
        self.groups_global.visible_background_group.add(self)
