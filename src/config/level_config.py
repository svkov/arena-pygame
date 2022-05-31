from typing import List
import numpy as np
import pandas as pd
from src.config.game_config import GameConfig
from src.core.spawner import Spawner
from src.game_object.boss import BossEnemy
from src.game_object.enemy import Enemy

class LevelConfig:

    def __init__(self, level_number, spawner: Spawner) -> None:
        self.level_number = level_number
        self.path = f'resources/level{self.level_number}.csv'
        raise FileNotFoundError()
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
    boss_default_pos = (3500, 5000)

    def __init__(self, level_number, spawner: Spawner, game_config: GameConfig) -> None:
        self.level_number = level_number
        self.spawner = spawner
        self.number_of_enemies = level_number * 5
        self.number_of_static = 3
        self.game_config = game_config

    def setup_level(self):
        self.spawner.spawn_object('background', pos=(0, 0))
        self.player = self.spawner.spawn_object('player', pos=self.player_default_pos)

        if self.game_config.spawn_enemies:
            self.spawn_enemies()
        if self.game_config.spawn_static:
            self.spawn_static()
        self.spawn_portal()

    def spawn_enemies(self):
        enemies = []
        for _ in range(self.number_of_enemies):
            x, y = self.generate_random_point_inside_circle()
            enemy: Enemy = self.spawner.spawn_object('skeleton', pos=(x, y))
            enemy.level_up(self.level_number)
            enemies.append(enemy)
        boss = self.spawner.spawn_object('priestess', pos=self.boss_default_pos)
        self.generate_drop(enemies, boss)

    def generate_drop(self, enemies: List[Enemy], boss: BossEnemy):
        pos = (-1000, -1000)
        self.generate_debug_drop()
        soul_stone = self.spawner.soul_stone(pos)
        boss.inventory.add(soul_stone)

        number_of_potions = self.number_of_enemies // 5
        potion_indices = np.random.choice(self.number_of_enemies - 1, number_of_potions)
        for i in potion_indices:
            potion = self.spawner.hp_potion_in_inventory(pos, enemies[i])
            enemies[i].inventory.add(potion)

        if np.random.randint(1, 10) == 1:
            # generate sword
            enemy_number = np.random.randint(0, self.number_of_enemies - 1)
            sword = self.spawner.sword_in_inventory(pos, enemies[enemy_number])
            enemies[enemy_number].inventory.add(sword)

        if np.random.randint(1, 20) == 1:
            # generate armor
            enemy_number = np.random.randint(0, self.number_of_enemies - 1)
            armor = self.spawner.armor_in_inventory(pos, enemies[enemy_number])
            enemies[enemy_number].inventory.add(armor)

    def generate_debug_drop(self):
        if self.game_config.debug:
            self.spawner.spawn_object('soul_stone', self.player.pos)
            self.spawner.spawn_object('sword', self.player.pos)
            self.spawner.spawn_object('armor', self.player.pos)

    def spawn_static(self):
        for _ in range(self.number_of_static):
            x, y = self.generate_random_point_inside_circle()
            self.spawner.spawn_object('cactus', pos=(x, y))

    def spawn_portal(self):
        self.spawner.spawn_object('portal', pos=self.portal_default_pos)

    def generate_random_point_inside_circle(self):
        distance_from_center = np.random.randint(1000, self.radius - 600)
        alpha = np.random.uniform(0, np.pi * 2)
        x = distance_from_center * np.cos(alpha) + self.radius
        y = distance_from_center * np.sin(alpha) + self.radius
        return x, y
