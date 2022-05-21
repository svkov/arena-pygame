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
        stats = self.stats_config.get_by_name(name)
        return self._map_object_name_to_create_function[name](pos=pos, **stats, **self.shared_args)

    def skeleton(self, *args, **kwargs):
        skeleton_states = generate_state.skeleton(self.sprites, self.fps)
        stats = EnemyStats(**kwargs)

        skeleton = AnimatedEnemy(*args, animation_states=skeleton_states, stats=stats, **kwargs)
        self.groups.spawn_enemy_object(skeleton)

        potion_stats = self.stats_config.get_by_name('hp_potion')
        potion = self.hp_potion_in_inventory(pos=(0, 0), **potion_stats, **self.shared_args)
        skeleton.inventory.add(potion)
        return skeleton

    def priestess(self, *args, **kwargs):
        stats = EnemyStats(**kwargs)
        priestess = Enemy(*args, stats=stats, **kwargs)
        self.groups.spawn_enemy_object(priestess)
        return priestess

    def vampire(self, *args, **kwargs):
        stats = EnemyStats(**kwargs)
        vampire = Enemy(*args, stats=stats, **kwargs)
        self.groups.spawn_enemy_object(vampire)
        return vampire

    def hp_potion(self, pos):
        stats = self.stats_config.get_by_name('hp_potion')
        potion = Potion(pos, **stats, owner=None)
        self.groups.spawn_item(potion)
        return potion

    def hp_potion_in_inventory(self, pos, owner=None):
        stats = self.stats_config.get_by_name('hp_potion')
        potion = Potion(pos, **stats, owner=owner)
        self.groups.items_in_inventory.add(potion)
        return potion

    def sword(self, *args, **kwargs):
        sword = SwordItem(*args, **kwargs, owner=None)
        self.groups.spawn_item(sword)
        return sword

    def armor(self, *args, **kwargs):
        armor = ArmorItem(*args, **kwargs, owner=None)
        self.groups.spawn_item(armor)
        return armor

    def portal(self, *args, **kwargs):
        portal = Portal.create_portal(*args, **kwargs)
        self.groups.interactive_objects.add(portal)
        return portal

    def soul_stone(self, *args, **kwargs):
        soul_stone = StoneSoulItem(*args, **kwargs, owner=None)
        self.groups.items_on_floor.add(soul_stone)
        return soul_stone

    def player(self, *args, **kwargs):
        stats = ActorStats(**kwargs)
        states = generate_state.player(kwargs['sprites'], kwargs['fps'])
        player = Player(*args, animation_states=states, stats=stats, **kwargs)
        self.groups.spawn_player_obj(player)
        return player

    def static_object(self, *args, **kwargs):
        static = StaticObject(*args, **kwargs)
        self.groups.spawn_static_object(static)
        return static

    def background(self, *args, **kwargs):
        background = Background(*args, **kwargs)
        self.groups.spawn_background(background)
        sprites = kwargs['sprites']
        self.setup_arena(background, background.radius, sprites)
        return background

    def setup_arena(self, background, radius, sprites):
        for alpha in np.linspace(0, 2 * np.pi, 500):
            pos = background.center
            new_pos_x = pos[0] + np.sin(alpha) * radius
            new_pos_y = pos[1] + np.cos(alpha) * radius
            pos = [new_pos_x, new_pos_y]
            self.static_object(pos, sprites['wall_without_contour'], (512, 512))
