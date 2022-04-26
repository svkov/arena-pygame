import numpy as np
from src.animated_enemy import AnimatedEnemy
from src.groups import GameStateGroups
from src.skeleton import generate_skeleton_states
from src.actor_stats import ActorStats, EnemyStats
from src.player import Player
from src.background import Background
from src.static_object import StaticObject

class Spawner:

    def __init__(self, groups: GameStateGroups) -> None:
        self.groups = groups
        self._map_object_name_to_create_function = {
            'skeleton': self.skeleton,
            'player': self.player,
            'background': self.background,
            'cactus': self.static_object,
            'tombstone': self.static_object
        }

    def spawn_object(self, name, *args, **kwargs):
        return self._map_object_name_to_create_function[name](*args, **kwargs)

    def skeleton(self, *args, **kwargs):
        sprites = kwargs['sprites']
        fps = kwargs['fps']
        skeleton_states = generate_skeleton_states(sprites, fps)
        stats = EnemyStats(**kwargs)

        skeleton = AnimatedEnemy(*args, animation_states=skeleton_states, stats=stats, **kwargs)
        self.groups.spawn_enemy_object(skeleton)
        return skeleton

    def player(self, *args, **kwargs):
        stats = ActorStats(**kwargs)
        player = Player(*args, stats=stats, **kwargs)
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
