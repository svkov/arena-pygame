from __future__ import annotations
import numpy as np
import pygame
from typing import TYPE_CHECKING
from src.game_object import GameObject
from src.collision_mixin import CollisionMixin
from src.cooldown_mixin import CooldownMixin
from src.game_object.moving_object import MovingObject
from src.game_object.projectile import Projectile
from src.hud.ingame_label import DamageLabel
from src.core.inventory import Inventory
from src.item.wieldable import WieldableItem
from src.hud.hp_bar import HpBar

if TYPE_CHECKING:
    from typing import Tuple
    from src.actor_stats import ActorStats
    from src.core.groups import GameStateGroups
    from src.animation import Animation
    from src.item import InventoryItem

class Actor(MovingObject, CollisionMixin):

    def __init__(self,
                 pos: Tuple[int, int],
                 image: pygame.surface.Surface,
                 image_size: Tuple[int, int] = None,
                 damage_recieve_cooldown: int = None,
                 projectile_image: pygame.surface.Surface = None,
                 stats: ActorStats = None,
                 groups: GameStateGroups = None,
                 weapon: InventoryItem = None,
                 armor: InventoryItem = None,
                 death_animation: Animation = None,
                 name: str = 'unknown',
                 lifetime_after_death: float = 3.0,
                 **kwargs):
        super().__init__(pos, image=image, image_size=image_size, **kwargs)
        self.stats = stats
        self.groups = groups
        self.projectile_image = projectile_image
        self.hp = self.max_hp
        self.hp_bar = HpBar(self, groups=groups)
        self.inventory = Inventory()
        self.weapon = weapon
        self.armor = armor
        self.death_animation = death_animation
        self.name = name
        self.lifetime_after_death = lifetime_after_death
        self.lifetime_after_death_counter = self.lifetime_after_death * self.game_config.fps
        self.colliding_objects = []
        self.is_going_left = False
        self.kills = {}
        attack_speed_in_frames = stats.attack_speed_in_frames(self.game_config.fps)
        # TODO: integrate with potion module
        hp_potion_cooldown = 50
        self.cooldowns = {
            'damage': CooldownMixin(damage_recieve_cooldown),
            'shoot': CooldownMixin(attack_speed_in_frames),
            'hp_potion': CooldownMixin(hp_potion_cooldown)
        }

    def shoot(self):
        pass

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    @property
    def max_hp(self) -> float:
        return self.stats.max_hp

    @property
    def damage(self) -> float:
        if self.weapon:
            return self.stats.damage + self.weapon.stats.damage
        return self.stats.damage

    def set_zero_speed(self):
        super().set_zero_speed()
        self.is_going_left = False

    def update_cooldown(self):
        for key, val in self.cooldowns.items():
            val.update_cooldown()

    def drop_item(self, inventory_item: InventoryItem):
        if issubclass(inventory_item.__class__, WieldableItem):
            inventory_item.unwield()
        inventory_item.kill()
        self.inventory.remove(inventory_item)
        self.groups.items_on_floor.add(inventory_item)
        inventory_item.on_drop(self.pos)

    def update(self, *args, **kwargs) -> None:
        dt: float = kwargs['dt']
        self.update_cooldown()
        self.normalize_speed()
        self.update_collision(dt)
        self.move_world_coord(dt)
        self.update_zoom()
        self.update_screen_coord()
        self.update_animation_if_needed()
        self.flip_image_if_needed()

    def flip_image_if_needed(self):
        if self.is_going_left:
            self.image = pygame.transform.flip(self.image, True, False)

    def update_collision(self, dt: float):
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
        if not self.is_alive:
            if self.death_animation is None:
                self.kill()
                return True
            self.image = self.death_animation.get_image()
            self.death_animation.update()
            if not self.death_animation.is_playing:
                self.lifetime_after_death_counter -= 1
                if self.lifetime_after_death_counter < 0:
                    self.kill()
            return True
        return False

    def on_collision(self, obj: GameObject):
        if isinstance(obj, Projectile):
            self.on_projectile_collision(obj)
        else:
            self.on_static_collision(obj)

    def on_projectile_collision(self, obj: Projectile):
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

    def on_death(self, death_from: Projectile):
        death_from.owner.on_kill(self)
        self.hp_bar.on_death()
        self.kill()
        self.groups.enemy_dying.add(self)

    def on_static_collision(self, obj: GameObject):
        self.colliding_objects.append(obj)
        return super().on_collision(obj)

    def on_kill(self, killed: Actor):
        score = killed.stats.scores_when_killed()
        self.kills[killed.name] = self.kills.get(killed.name, 0) + score
