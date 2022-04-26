import numpy as np
import pygame

from src.camera import Camera
from src.groups import GameStateGroups
from src.hud import HUD
from src.level_config import LevelConfig
from src.spawner import Spawner
from src.static_object import StaticObject
from src.stats_config import StatsConfig

class GameState:
    def __init__(self, screen_resolution, fps, sprites) -> None:
        self.my_font = pygame.font.SysFont(pygame.font.get_default_font(), 28)
        self.screen_resolution = screen_resolution
        self.fps = fps
        self.sprites = sprites
        self.camera = Camera(0, 0, screen_resolution)
        self.groups = GameStateGroups()
        self.spawner = Spawner(self.groups)
        self.setup_scene()
        self.hud = HUD(self.player)

    def setup_scene(self):
        stats_config = StatsConfig('resources/stats.csv', self.sprites)
        level_config = LevelConfig('resources/level1.csv', self.camera, self.fps, stats_config, self.spawner)
        level_config.setup_level()
        # setup_object_randomly(background, radius, sprites)
        # setup_object_randomly(background, radius, sprites, n_sample=10, sprite_name='tombstone')
        self.player = level_config.player

    def update(self, **kwargs):
        screen = kwargs['screen']

        update_kwargs = {
            **kwargs,
            'camera': self.camera,
            'groups': self.groups
        }

        screen.fill((0, 0, 0))
        self.groups.background_group.draw(screen)
        self.groups.update(update_kwargs)
        self.groups.handle_collisions(update_kwargs)

        self.groups.draw(screen)
        self.hud.update(screen=screen, screen_resolution=self.screen_resolution, font=self.my_font)

        pygame.display.flip()

    def setup_object_randomly(self, background, radius, sprites, n_sample=15, sprite_name='cactus', image_size=None):
        if image_size is None:
            image_size = (128, 256)
        top_right_x = background.center[0] + np.sin(np.pi / 4) * radius
        top_right_y = background.center[1] + np.cos(np.pi / 4) * radius
        bottom_left_x = background.center[0] - np.sin(np.pi / 4) * radius
        bottom_left_y = background.center[1] - np.cos(np.pi / 4) * radius
        object_pos_x = np.random.randint(bottom_left_x, top_right_x, size=(n_sample, 1))
        object_pos_y = np.random.randint(bottom_left_y, top_right_y, size=(n_sample, 1))
        object_poses = np.hstack((object_pos_x, object_pos_y))
        for object_i in range(n_sample):
            pos = object_poses[object_i]
            obj = StaticObject(pos, sprites[sprite_name], image_size=image_size)
            self.spawn_static_object(obj)
