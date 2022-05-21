import numpy as np
import pandas as pd
from src.spawner import Spawner

class LevelConfig:

    def __init__(self, level_number, spawner: Spawner) -> None:
        self.level_number = level_number
        self.path = f'resources/level{self.level_number}.csv'
        self.df = pd.read_csv(self.path, sep=';')
        self.spawner = spawner

    def setup_level(self):
        for i, row in self.df.iterrows():
            obj_dict = row.to_dict()
            name = obj_dict['object_name']
            pos = (obj_dict['pos_x'], obj_dict['pos_y'])
            spawned_obj = self.spawner.spawn_object(name, pos=pos)
            if name == 'player':
                self.player = spawned_obj

class RandomLevelConfig:
    radius = 3500
    player_default_pos = (3500, 3500)
    portal_default_pos = (3500, 2000)

    def __init__(self, level_number, spawner: Spawner) -> None:
        self.level_number = level_number
        self.spawner = spawner
        self.number_of_enemies = level_number * 5
        self.number_of_static = 3

    def setup_level(self):
        self.spawner.spawn_object('background', pos=(0, 0))
        self.player = self.spawner.spawn_object('player', pos=self.player_default_pos)

        self.spawn_enemies()
        self.spawn_static()
        self.spawn_portal()

    def spawn_enemies(self):
        for _ in range(self.number_of_enemies):
            x, y = self.generate_random_point_inside_circle()
            self.spawner.spawn_object('skeleton', pos=(x, y))

    def spawn_static(self):
        for _ in range(self.number_of_static):
            x, y = self.generate_random_point_inside_circle()
            self.spawner.spawn_object('cactus', pos=(x, y))

    def spawn_portal(self):
        self.spawner.spawn_object('portal', pos=self.portal_default_pos)

    def generate_random_point_inside_circle(self):
        distance_from_center = np.random.randint(1, self.radius - 300)
        alpha = np.random.uniform(0, np.pi * 2)
        x = distance_from_center * np.cos(alpha) + self.radius
        y = distance_from_center * np.sin(alpha) + self.radius
        return x, y
