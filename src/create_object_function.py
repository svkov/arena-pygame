from src.actor_stats import ActorStats
from src.animated_enemy import AnimatedEnemy
from src.background import Background
from src.player import Player
from src.skeleton import generate_skeleton_states
from src.static_object import StaticObject
from src.utils import spawn_background, spawn_object, spawn_static_object
import numpy as np

def skeleton(*args, **kwargs):
    sprites = kwargs['sprites']
    fps = kwargs['fps']
    skeleton_states = generate_skeleton_states(sprites, fps)
    stats = ActorStats(**kwargs)

    skeleton = AnimatedEnemy(*args, animation_states=skeleton_states, stats=stats, **kwargs)
    spawn_object(skeleton)
    return skeleton

def player(*args, **kwargs):
    stats = ActorStats(**kwargs)
    player = Player(*args, stats=stats, **kwargs)
    spawn_object(player)
    return player

def static_object(*args, **kwargs):
    static = StaticObject(*args, **kwargs)
    spawn_static_object(static)
    return static

def background(*args, **kwargs):
    background = Background(*args, **kwargs)
    spawn_background(background)
    sprites = kwargs['sprites']
    setup_arena(background, background.radius, sprites)
    return background


def setup_arena(background, radius, sprites):
    for alpha in np.linspace(0, 2 * np.pi, 500):
        pos = background.center
        new_pos_x = pos[0] + np.sin(alpha) * radius
        new_pos_y = pos[1] + np.cos(alpha) * radius
        pos = [new_pos_x, new_pos_y]
        static_object(pos, sprites['wall_without_contour'], (512, 512))
