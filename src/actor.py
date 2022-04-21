import numpy as np
from src.camera import Camera
from src.damage_recieve_mixin import DamageRecieveMixin
from src.game_object import GameObject
from src.hp_bar import HpBar
from src.shoot_cooldown_mixin import ShootCooldownMixin


class Actor(GameObject, DamageRecieveMixin, ShootCooldownMixin):

    def __init__(self, pos, image_path, image_size=None,
                 damage_recieve_cooldown=None, shoot_cooldown=None,
                 max_hp=None, hp=None, projectile_image=None, **kwargs):
        super().__init__(pos, image_path, image_size)
        DamageRecieveMixin.__init__(self, damage_recieve_cooldown)
        ShootCooldownMixin.__init__(self, shoot_cooldown)
        self.speed = np.array([0, 0])
        self.projectile_image = projectile_image
        self.max_hp = max_hp
        self.hp = hp
        self.hp_bar = HpBar(self)
        self._low_damage = 10
        self._high_damage = 20

    @property
    def damage(self):
        return np.random.randint(self._low_damage, self._high_damage)

    def set_zero_speed(self):
        self.speed = np.array([0, 0])

    def update_cooldown(self):
        self.update_damage_cooldown()
        self.update_shoot_cooldown()

    def update(self, *args, **kwargs) -> None:
        self.update_cooldown()
        screen = kwargs['screen']
        dt = kwargs['dt']
        camera: Camera = kwargs['camera']
        self.hp_bar.update(screen, camera)

        self.pos = self.pos + self.speed * dt

        super().update(*args, **kwargs)

    def on_collision(self, obj):
        if self.can_recieve_damage:
            damage = obj.damage
            self.hp -= damage
            if self.hp <= 0:
                self.on_death(obj)
                self.kill()
            self.damaged()

    def on_death(self, death_from):
        pass
