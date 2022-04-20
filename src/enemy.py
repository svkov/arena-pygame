import numpy as np
from src.actor import Actor
from src.camera import Camera

from src.projectile import Projectile
from src.utils import spawn_projectile


class Enemy(Actor):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.exp_after_death = 50

    def shoot(self, camera: Camera):
        if self.can_shoot:
            self.shooted()
            p = Projectile.shoot(self, np.array([0, 0]), camera, 'assets/snow.png', speed=1)
            spawn_projectile(p)

    def update(self, *args, **kwargs) -> None:
        camera: Camera = kwargs['camera']
        self.shoot(camera)
        return super().update(*args, **kwargs)

    def on_death(self, death_from):
        death_from.owner.increase_xp(self.exp_after_death)

    def increase_xp(self):
        pass
