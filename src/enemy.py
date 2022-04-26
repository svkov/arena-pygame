from src.actor import Actor
from src.behavior import Behavior
from src.camera import Camera
from src.groups import GameStateGroups
from src.projectile import Projectile


class Enemy(Actor):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.exp_after_death = 50
        self.behavior = kwargs.get('behavior', Behavior(self))

    def shoot(self, camera: Camera, groups: GameStateGroups):
        if self.can_shoot:
            self.shooted()
            p = Projectile.shoot(self, camera.to_screen_coord(camera.get_pos()), camera, self.projectile_image,
                                 speed=self.stats.projectile_speed)
            groups.spawn_enemy_projectile(p)

    def update(self, *args, **kwargs) -> None:
        camera: Camera = kwargs['camera']
        groups: GameStateGroups = kwargs['groups']
        self.shoot(camera, groups)
        self.behavior.update(*args, **kwargs)
        return super().update(*args, **kwargs)

    def on_death(self, death_from):
        super().on_death(death_from)
        death_from.owner.increase_xp(self.exp_after_death)

    def increase_xp(self):
        pass
