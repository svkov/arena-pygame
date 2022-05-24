import numpy as np
import pygame

from src.camera import Camera
import src.utils as utils

class GameObject(pygame.sprite.Sprite):

    def __init__(self, pos, image, image_size=None, pos_in_world_coord=True, **kwargs) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.pos = np.array(pos, dtype=np.float)
        self.camera: Camera = kwargs['camera']
        self.image_size = image_size
        if image_size is None:
            self.image_size = (128, 128)

        self.image: pygame.surface.Surface = image

        self.image_by_zoom = utils.preresize_image(self.image, self.camera, self.image_size)
        self.image = self.image_by_zoom[self.camera.zoom_factor]
        self.rect = self.image.get_rect()
        if pos_in_world_coord:
            self.update_screen_coord()
        else:
            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]

    def update(self, *args, **kwargs):
        camera = kwargs['camera']
        self.update_zoom(camera)
        self.update_screen_coord()

    def update_screen_coord(self):
        new_pos = self.camera.to_screen_coord(self.pos)
        self.rect.x = int(new_pos[0])
        self.rect.y = int(new_pos[1])

    def update_zoom(self, camera):
        if self.image != self.image_by_zoom[camera.zoom_factor]:
            self.image = self.image_by_zoom[camera.zoom_factor]
            new_width = int(self.camera.zoom_factor * self.image_size[0])
            new_height = int(self.camera.zoom_factor * self.image_size[1])
            self.rect.width = new_width
            self.rect.height = new_height

    def set_image_size(self, new_image_size):
        self.image_size = new_image_size
        self.image = pygame.transform.scale(self.image, self.image_size)

    @property
    def center_world(self):
        return (self.pos[0] + self.image_size[0] // 2,
                self.pos[1] + self.image_size[1] // 2)

    @property
    def center_screen(self):
        return (int(self.rect.x + self.image_size[0] // 2),
                int(self.rect.y + self.image_size[1]) // 2)

    @property
    def pos_right(self):
        return int(self.pos[0] + self.image_size[0])

    @pos_right.setter
    def pos_right(self, value):
        self.pos[0] = value - self.image_size[0]

    @property
    def pos_left(self):
        return int(self.pos[0])

    @pos_left.setter
    def pos_left(self, value):
        self.pos[0] = value

    @property
    def pos_top(self):
        return int(self.pos[1])

    @pos_top.setter
    def pos_top(self, value):
        self.pos[1] = value

    @property
    def pos_bottom(self):
        return int(self.pos[1] + self.image_size[1])

    @pos_bottom.setter
    def pos_bottom(self, value):
        self.pos[1] = value - self.image_size[1]

    def on_collision(self, obj):
        pass

    @property
    def damage(self):
        return 0
