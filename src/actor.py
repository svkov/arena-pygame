import numpy as np
from src.actor_stats import ActorStats
from src.animation import Animation
from src.camera import Camera
from src.collision_mixin import CollisionMixin
from src.cooldown_mixin import CooldownMixin
from src.game_object import GameObject
from src.groups import GameStateGroups
from src.hp_bar import HpBar
from src.ingame_label import DamageLabel
from src.inventory import Inventory
from src.item.wieldable import WieldableItem
from src.projectile import Projectile


class Actor(GameObject, CollisionMixin):

    def __init__(self, pos, image, image_size=None,
                 damage_recieve_cooldown=None,
                 projectile_image=None, stats: ActorStats = None,
                 groups: GameStateGroups = None, **kwargs):
        super().__init__(pos, image, image_size, **kwargs)
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
        self.death_animation: Animation = kwargs.get('death_animation', None)
        self.lifetime_after_death = kwargs.get('lifetime_after_death', 3.0)
        self.lifetime_after_death_counter = self.lifetime_after_death * self.game_config.fps
        self.colliding_objects = []
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
        if issubclass(inventory_item.__class__, WieldableItem):
            inventory_item.unwield()
        inventory_item.kill()
        self.inventory.remove(inventory_item)
        self.groups.items_on_floor.add(inventory_item)
        inventory_item.on_drop(self.pos)

    def update(self, *args, **kwargs) -> None:
        self.update_cooldown()
        dt = kwargs['dt']
        self.camera: Camera = kwargs['camera']
        self.normalize_speed()
        self.update_collision(dt)
        self.move_world_coord(dt)
        self.update_zoom(self.camera)
        self.update_screen_coord()
        self.update_animation_if_needed()

    def update_collision(self, dt):
        for obj in self.colliding_objects:
            self._collision(obj, dt=dt)
        self.colliding_objects.clear()

    def _right(self, obj, *args, **kwargs):
        pos = np.array(self.center_world)
        dt = kwargs['dt']
        self.cut_speed_by_axis(obj.center_world, pos, self.speed, dt, 0)

    def _left(self, obj, *args, **kwargs):
        pos = np.array(self.center_world)
        dt = kwargs['dt']
        self.cut_speed_by_axis(obj.center_world, pos, self.speed, dt, 0)

    def _top(self, obj, *args, **kwargs):
        pos = np.array(self.center_world)
        dt = kwargs['dt']
        self.cut_speed_by_axis(obj.center_world, pos, self.speed, dt, 1)

    def _bottom(self, obj, *args, **kwargs):
        pos = np.array(self.center_world)
        dt = kwargs['dt']
        self.cut_speed_by_axis(obj.center_world, pos, self.speed, dt, 1)

    def cut_speed_by_axis(self, obj_pos, pos, speed, dt, axis):
        distance_before = int(abs(pos[axis] - obj_pos[axis]))
        pos_after = self.calculate_pos_by_axis(pos, speed, dt, axis)
        distance_after = int(abs(pos_after - obj_pos[axis]))
        if distance_before > distance_after:
            self.speed[axis] = 0

    def calculate_pos_by_axis(self, pos, speed, dt, axis):
        pos_after = pos[axis] + speed[axis] * dt
        return pos_after

    def update_animation_if_needed(self):
        if not self.is_alive and self.death_animation is not None:
            self.image = self.death_animation.get_image()
            self.death_animation.update()
            if not self.death_animation.is_playing:
                self.lifetime_after_death_counter -= 1
                if self.lifetime_after_death_counter < 0:
                    self.kill()
            return True
        return False

    def normalize_speed(self):
        if np.linalg.norm(self.speed) < self.stats.movement_speed:
            return
        if np.linalg.norm(self.speed) > 0:
            self.speed = self.speed / np.linalg.norm(self.speed)
            self.speed = self.speed * self.stats.movement_speed

    def move_world_coord(self, dt):
        self.pos = self.pos + self.speed * dt

    def on_collision(self, obj):
        if isinstance(obj, Projectile):
            self.on_projectile_collision(obj)
        else:
            self.on_static_collision(obj)

    def on_projectile_collision(self, obj):
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
            self.cooldowns['damage'].reset_counter()

    def on_death(self, death_from):
        self.hp_bar.on_death()
        self.kill()
        self.groups.enemy_dying.add(self)

    def on_static_collision(self, obj):
        self.colliding_objects.append(obj)
        return super().on_collision(obj)
