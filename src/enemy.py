import numpy as np
from src.actor import Actor

from src.projectile import Projectile
from src.utils import spawn_projectile


class Enemy(Actor):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.exp_after_death = 50

    def shoot(self):
        if self.can_shoot:
            self.shooted()
            p = Projectile.shoot(self, np.array(
                [0, 0]), 'assets/snow.png', speed=1)
            spawn_projectile(p)

    def update(self, *args, **kwargs) -> None:
        self.shoot()
        return super().update(*args, **kwargs)

    def on_death(self, death_from):
        death_from.owner.increase_xp(self.exp_after_death)
