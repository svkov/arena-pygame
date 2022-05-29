import pygame
from src.camera import Camera

from src.game_object import GameObject
from src.groups import GameStateGroups


class RectangleSurface(pygame.sprite.Sprite):
    def __init__(self,
                 owner,
                 color,
                 size=None) -> None:
        super().__init__()
        self.size = size
        self.owner = owner
        if size is None:
            self.size = [self.owner.image_size[0], 10]
        self.color = color
        self.set_image()

    def set_image(self):
        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

    def update(self, camera: Camera, **kwargs):
        pass

    def update_rect(self):
        self.rect.x = int(self.pos[0])
        self.rect.y = int(self.pos[1])
        if self.size[0] != self.owner.rect.width:
            self.size[0] = self.owner.rect.width
            self.set_image()

    def set_rect_size(self, rect_size):
        self.rect.width = int(rect_size[0])
        self.rect.height = int(rect_size[1])

    def update_pos(self, camera: Camera):
        pos_x = int(self.owner.pos[0])
        pos_y = int(self.owner.pos[1] - self.owner.image_size[1] // 2)
        self.pos = camera.to_screen_coord([pos_x, pos_y])

class RedSurface(RectangleSurface):
    def __init__(self, owner, color, size=None) -> None:
        color = (255, 0, 0)
        super().__init__(owner, color, size)

    def update(self, camera: Camera, **kwargs):
        self.update_pos(camera)
        self.update_rect()


class GreenSurface(RectangleSurface):
    def __init__(self, owner, size=None) -> None:
        color = (0, 255, 0)
        super().__init__(owner, color, size)

    def update(self, camera: Camera, **kwargs):
        self.update_pos(camera)
        self.image = pygame.Surface(self.new_size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.update_rect()

    @property
    def new_size(self):
        progress = self.owner.hp / self.owner.max_hp
        width = int(self.size[0] * progress)
        height = self.size[1]
        return (width, height)

class HpBar:

    def __init__(self, owner: GameObject, size=None, groups: GameStateGroups = None):
        super().__init__()
        self.owner = owner
        self.groups = groups

        self.green = GreenSurface(owner, size)
        self.red = RedSurface(owner, size)
        groups.ui_objects.add(self.red)
        groups.ui_objects.add(self.green)

    def on_death(self):
        self.red.kill()
        self.green.kill()
