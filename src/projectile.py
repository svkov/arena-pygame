import numpy as np

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
        if self.dist < self.range:
            self.pos = self.pos + self.speed * dt
            self.rect.x = int(self.pos[0])
            self.rect.y = int(self.pos[1])
            self.dist += np.linalg.norm(self.speed)
        else:
            self.kill()

    def on_collision(self, obj):
        pass

    @classmethod
    def shoot(cls, owner_obj, target_pos,
              image_path, speed=1, image_size=None):
        if image_size is None:
            image_size = (32, 32)
        direction = np.array(target_pos) - owner_obj.pos
        direction = direction / np.linalg.norm(direction)
        pos = owner_obj.center + direction * \
            np.array(owner_obj.image_size) + direction * np.array(image_size)
        speed_vector = direction * speed
        return cls(pos, speed_vector, image_path=image_path,
                   image_size=image_size, owner=owner_obj)

    @property
    def damage(self):
        return self.owner.damage
