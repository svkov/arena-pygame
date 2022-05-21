import numpy as np
from src.animated_enemy import AnimatedEnemy
from src.camera import Camera
from src.enemy import Enemy
from src.groups import GameStateGroups
import src.animation.generate_state as generate_state
from src.actor_stats import ActorStats, EnemyStats
from src.item.potion import Potion
from src.item.quest_item import StoneSoulItem
from src.item.sword import ArmorItem, SwordItem
from src.player import Player
from src.background import Background
from src.portal import Portal
from src.static_object import StaticObject
from src.stats_config import StatsConfig

class Spawner:

    def __init__(self, groups: GameStateGroups, camera: Camera, stats_config: StatsConfig, fps, sprites) -> None:
        self.camera = camera
        self.fps = fps
        self.sprites = sprites
        self.groups = groups
        self.stats_config = stats_config
        self.shared_args = {
            'camera': self.camera,
            'fps': self.fps,
            'sprites': self.sprites,
            'groups': self.groups
        }
        self._map_object_name_to_create_function = {
            'skeleton': self.skeleton,
            'vampire': self.vampire,
            'player': self.player,
            'background': self.background,
            'cactus': self.static_object,
            'tombstone': self.static_object,
            'priestess': self.priestess,
            'hp_potion': self.hp_potion,
            'sword': self.sword,
            'armor': self.armor,
            'portal': self.portal,
            'soul_stone': self.soul_stone
        }

    def spawn_object(self, name, pos):
        func = self._map_object_name_to_create_function[name]
        if func.__name__ == 'static_object':
            return func(pos, name)
        return func(pos)

    def generate_actor_kwargs(self, name):
        all_stats = self.stats_config.get_by_name(name)
        stats = ActorStats(**all_stats)
        return dict(**all_stats, stats=stats, **self.shared_args)

    def generate_enemy_kwargs(self, name):
        all_stats = self.stats_config.get_by_name(name)
        stats = EnemyStats(**all_stats)
        return dict(**all_stats, stats=stats, **self.shared_args)

    def generate_item_kwargs(self, name, owner):
        stats = self.stats_config.get_by_name(name)
        return dict(**stats, **self.shared_args, owner=owner)

    def generate_static_object_kwargs(self, name):
        stats = self.stats_config.get_by_name(name)
        return dict(**stats, **self.shared_args)

    def skeleton(self, pos, **kwargs):
        kwargs = self.generate_enemy_kwargs('skeleton')

        skeleton_states = generate_state.skeleton(self.sprites, self.fps)
        skeleton = AnimatedEnemy(pos, animation_states=skeleton_states, **kwargs)
        self.groups.spawn_enemy_object(skeleton)
        return skeleton

    def priestess(self, pos, **kwargs):
        kwargs = self.generate_enemy_kwargs('priestess')
        priestess = Enemy(pos, **kwargs)
        self.groups.spawn_enemy_object(priestess)
        return priestess

    def vampire(self, pos, **kwargs):
        kwargs = self.generate_enemy_kwargs('vampire')
        vampire = Enemy(pos, **kwargs)
        self.groups.spawn_enemy_object(vampire)
        return vampire

    def hp_potion(self, pos):
        potion = self.get_hp_potion(pos, None)
        self.groups.spawn_item(potion)
        return potion

    def hp_potion_in_inventory(self, pos, owner=None):
        potion = self.get_hp_potion(pos, owner)
        self.groups.items_in_inventory.add(potion)
        return potion

    def get_hp_potion(self, pos, owner):
        return self.get_item(pos, 'hp_potion', owner, Potion)

    def sword(self, pos, owner=None):
        sword = self.get_sword(pos, owner)
        self.groups.spawn_item(sword)
        return sword

    def sword_in_inventory(self, pos, owner=None):
        sword = self.get_sword(pos, owner)
        self.groups.items_in_inventory.add(sword)
        return sword

    def get_sword(self, pos, owner):
        return self.get_item(pos, 'sword', owner, SwordItem)

    def armor(self, pos, owner=None):
        armor = self.get_armor(pos, owner)
        self.groups.spawn_item(armor)
        return armor

    def armor_in_inventory(self, pos, owner=None):
        armor = self.get_armor(pos, owner)
        self.groups.items_in_inventory.add(armor)
        return armor

    def get_armor(self, pos, owner):
        return self.get_item(pos, 'armor', owner, ArmorItem)

    def get_item(self, pos, name, owner, class_):
        kwargs = self.generate_item_kwargs(name, owner)
        return class_(pos, **kwargs)

    def portal(self, pos, **kwargs):
        kwargs = self.generate_static_object_kwargs('portal')
        portal = Portal.create_portal(pos, **kwargs)
        self.groups.interactive_objects.add(portal)
        return portal

    def soul_stone(self, pos, owner=None):
        kwargs = self.generate_item_kwargs('soul_stone', owner)
        soul_stone = StoneSoulItem(pos, **kwargs)
        self.groups.items_on_floor.add(soul_stone)
        return soul_stone

    def player(self, pos):
        kwargs = self.generate_actor_kwargs('player')
        states = generate_state.player(self.sprites, self.fps)
        player = Player(pos, animation_states=states, **kwargs)
        self.groups.spawn_player_obj(player)
        return player

    def static_object(self, pos, name):
        kwargs = self.generate_static_object_kwargs(name)
        static = StaticObject(pos, **kwargs)
        self.groups.spawn_static_object(static)
        return static

    def background(self, pos):
        kwargs = self.generate_static_object_kwargs('background')
        background = Background(pos, **kwargs)
        self.groups.spawn_background(background)
        self.setup_arena(background, background.radius)
        return background

    def setup_arena(self, background, radius):
        for alpha in np.linspace(0, 2 * np.pi, 500):
            pos = background.center
            new_pos_x = pos[0] + np.sin(alpha) * radius
            new_pos_y = pos[1] + np.cos(alpha) * radius
            pos = [new_pos_x, new_pos_y]
            self.static_object(pos, 'wall_without_contour')
