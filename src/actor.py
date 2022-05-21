import numpy as np
from src.actor_stats import ActorStats
from src.camera import Camera
from src.cooldown_mixin import CooldownMixin
from src.game_object import GameObject
from src.groups import GameStateGroups
from src.hp_bar import HpBar
from src.ingame_label import DamageLabel
from src.inventory import Inventory


class Actor(GameObject):

    def __init__(self, pos, image, image_size=None,
                 damage_recieve_cooldown=None,
                 projectile_image=None, stats: ActorStats = None,
                 groups: GameStateGroups = None, **kwargs):
        super().__init__(pos, image, image_size)
        self.stats: ActorStats = stats
        self.groups: GameStateGroups = groups
        self.speed = np.array([0, 0])
        self.projectile_image = projectile_image
        self.hp = self.max_hp
        self.hp_bar = HpBar(self, groups=groups)
        self.camera = kwargs['camera']
        self.inventory = Inventory()
        self.weapon = kwargs.get('weapon', None)
        self.armor = kwargs.get('armor', None)
        attack_speed_in_frames = stats.attack_speed_in_frames(kwargs['fps'])
        # TODO: integrate with potion module
        hp_potion_cooldown = 50
        self.cooldowns = {
            'damage': CooldownMixin(damage_recieve_cooldown),
            'shoot': CooldownMixin(attack_speed_in_frames),
            'hp_potion': CooldownMixin(hp_potion_cooldown)
        }

    def shoot(self, camera: Camera):
        pass

    @property
    def is_alive(self):
        return self.hp > 0

    @property
    def max_hp(self):
        return self.stats.max_hp

    @property
    def damage(self):
        if self.weapon:
            return self.stats.damage + self.weapon.stats.damage
        return self.stats.damage

    def set_zero_speed(self):
        self.speed = np.array([0, 0])

    def update_cooldown(self):
        for key, val in self.cooldowns.items():
            val.update_cooldown()

    def drop_item(self, inventory_item):
        inventory_item.kill()
        self.inventory.remove(inventory_item)
        self.groups.items_on_floor.add(inventory_item)
        inventory_item.on_drop(self.pos)

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
        if self.cooldowns['damage'].is_cooldown_over:
            damage = obj.damage
            if self.armor is not None:
                damage = self.stats.damage_take(damage, self.armor.stats.defense)
            else:
                damage = self.stats.damage_take(damage)
            damage_label = DamageLabel(f'-{int(damage)}', self.pos, self.camera)
            self.groups.spawn_ui(damage_label)
            self.hp -= damage
            if self.hp <= 0:
                self.on_death(obj)
                self.kill()
            self.cooldowns['damage'].reset_counter()

    def on_death(self, death_from):
        self.hp_bar.on_death()
