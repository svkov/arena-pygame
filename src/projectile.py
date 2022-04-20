import numpy as np
from src.camera import Camera

from src.game_object import GameObject


class Projectile(GameObject):

    def __init__(self,
                 pos,
                 speed,
                 image_path,
                 image_size=None,
                 range=500,
                 owner=None):
        super().__init__(pos, image_path, image_size)
        self.speed = np.array(speed)
        self.dist = 0
        self.range = range
        self.owner = owner

    def update(self, *args, **kwargs):
        dt = kwargs['dt']
        camera: Camera = kwargs['camera']
        if self.dist < self.range:
            self.pos = self.pos + self.speed * dt
            new_pos = camera.to_screen_coord(self.pos)
            self.rect.x = int(new_pos[0])
            self.rect.y = int(new_pos[1])
            self.dist += np.linalg.norm(self.speed * dt)
        else:
            self.kill()

    def on_collision(self, obj):
        pass

    @classmethod
    def shoot(cls, owner_obj, target_pos, camera, image_path, speed=1, image_size=None):
        if image_size is None:
            image_size = (32, 32)
        target_pos = np.array(target_pos) - np.array(image_size) / 2
        target_world_pos = camera.to_world_coord(target_pos)
        owner_world_pos = camera.to_world_coord(owner_obj.center)
        direction = np.array(target_world_pos) - owner_world_pos
        direction = direction / np.linalg.norm(direction)
        pos = owner_world_pos + direction * np.array(owner_obj.image_size) + direction * np.array(image_size)
        speed_vector = direction * speed
        return cls(pos, speed_vector, image_path=image_path,
                   image_size=image_size, owner=owner_obj)

    @property
    def damage(self):
        return self.owner.damage
