import numpy as np
from src.actor_stats import ActorStats
from src.camera import Camera
from src.damage_recieve_mixin import DamageRecieveMixin
from src.game_object import GameObject
from src.groups import GameStateGroups
from src.hp_bar import HpBar
from src.ingame_label import DamageLabel
from src.shoot_cooldown_mixin import ShootCooldownMixin


class Actor(GameObject, DamageRecieveMixin, ShootCooldownMixin):

    def __init__(self, pos, image, image_size=None,
                 damage_recieve_cooldown=None,
                 projectile_image=None, stats: ActorStats = None,
                 groups: GameStateGroups = None, **kwargs):
        super().__init__(pos, image, image_size)
        DamageRecieveMixin.__init__(self, damage_recieve_cooldown)
        self.stats: ActorStats = stats
        self.groups: GameStateGroups = groups
        attack_speed_in_frames = stats.attack_speed_in_frames(kwargs['fps'])
        ShootCooldownMixin.__init__(self, attack_speed_in_frames)
        self.speed = np.array([0, 0])
        self.projectile_image = projectile_image
        self.hp = self.max_hp
        self.hp_bar = HpBar(self, groups=groups)
        self.camera = kwargs['camera']

    @property
    def max_hp(self):
        return self.stats.max_hp

    @property
    def damage(self):
        return self.stats.damage

    def set_zero_speed(self):
        self.speed = np.array([0, 0])

    def update_cooldown(self):
        self.update_damage_cooldown()
        self.update_shoot_cooldown()

    def update(self, *args, **kwargs) -> None:
        self.update_cooldown()
        screen = kwargs['screen']
        dt = kwargs['dt']
        self.camera: Camera = kwargs['camera']
        self.normalize_speed()
        self.move_world_coord(dt)
        self.update_screen_coord(screen, self.camera)

    def normalize_speed(self):
        if np.linalg.norm(self.speed) < self.stats.movement_speed:
            return
        if np.linalg.norm(self.speed) > 0:
            self.speed = self.speed / np.linalg.norm(self.speed)
            self.speed = self.speed * self.stats.movement_speed

    def move_world_coord(self, dt):
        self.pos = self.pos + self.speed * dt

    def update_screen_coord(self, screen, camera: Camera):
        super().update_screen_coord(camera)

    def on_collision(self, obj):
        if self.can_recieve_damage:
            damage = obj.damage
            damage = self.stats.damage_take(damage)
            damage_label = DamageLabel(f'-{damage}', self.pos, self.camera)
            self.groups.spawn_hp_bar(damage_label)
            self.hp -= damage
            if self.hp <= 0:
                self.on_death(obj)
                self.kill()
            self.damaged()

    def on_death(self, death_from):
        self.hp_bar.on_death()
