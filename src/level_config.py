import numpy as np
import pandas as pd
from src.camera import Camera
from src.groups import GameStateGroups
from src.spawner import Spawner
from src.stats_config import StatsConfig

class LevelConfig:

    def __init__(self, level_number, camera: Camera, fps, stats_config: StatsConfig,
                 spawner: Spawner, groups: GameStateGroups) -> None:
        self.level_number = level_number
        self.path = f'resources/level{self.level_number}.csv'
        self.df = pd.read_csv(self.path, sep=';')
        self.camera = camera
        self.fps = fps
        self.stats_config = stats_config
        self.spawner = spawner
        self.groups = groups

    def setup_level(self):
        shared_args = {
            'camera': self.camera,
            'fps': self.fps,
            'sprites': self.stats_config.sprites,
            'groups': self.groups
        }
        for i, row in self.df.iterrows():
            obj_dict = row.to_dict()
            name = obj_dict['object_name']
            pos = (obj_dict['pos_x'], obj_dict['pos_y'])
            obj_stats = self.stats_config.get_by_name(name)
            spawned_obj = self.spawner.spawn_object(name, pos=pos, **shared_args, **obj_stats)
            if name == 'player':
                self.player = spawned_obj

class RandomLevelConfig:

    def __init__(self, level_number, camera: Camera, fps, stats_config: StatsConfig,
                 spawner: Spawner, groups: GameStateGroups) -> None:
        self.level_number = level_number
        self.camera = camera
        self.fps = fps
        self.stats_config = stats_config
        self.spawner = spawner
        self.groups = groups
        self.number_of_enemies = level_number * 3
        self.number_of_static = 3

    def setup_level(self):
        shared_args = {
            'camera': self.camera,
            'fps': self.fps,
            'sprites': self.stats_config.sprites,
            'groups': self.groups
        }

        background_stats = self.stats_config.get_by_name('background')
        self.spawner.spawn_object('background', pos=(0, 0), **shared_args, **background_stats)
        self.radius = background_stats.get('radius', 3500)

        player_stats = self.stats_config.get_by_name('player')
        self.player = self.spawner.spawn_object('player', pos=(3500, 3500), **shared_args, **player_stats)

        self.spawn_enemies(shared_args)
        self.spawn_static(shared_args)
        self.spawn_portal(shared_args)

    def spawn_enemies(self, shared_args):
        skeleton_stats = self.stats_config.get_by_name('skeleton')
        for _ in range(self.number_of_enemies):
            x, y = self.generate_random_point_inside_circle()
            self.spawner.spawn_object('skeleton', pos=(x, y), **shared_args, **skeleton_stats)

    def spawn_static(self, shared_args):
        obj_stats = self.stats_config.get_by_name('cactus')
        for _ in range(self.number_of_static):
            x, y = self.generate_random_point_inside_circle()
            self.spawner.spawn_object('cactus', pos=(x, y), **shared_args, **obj_stats)

    def spawn_portal(self, shared_args):
        portal_stats = self.stats_config.get_by_name('portal')
        self.spawner.spawn_object('portal', pos=(3500, 2000), **shared_args, **portal_stats)

    def generate_random_point_inside_circle(self):
        distance_from_center = np.random.randint(1, self.radius - 300)
        alpha = np.random.uniform(0, np.pi * 2)
        x = distance_from_center * np.cos(alpha) + self.radius
        y = distance_from_center * np.sin(alpha) + self.radius
        return x, y
