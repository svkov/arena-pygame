import pandas as pd
from src.camera import Camera
from src.groups import GameStateGroups
from src.spawner import Spawner
from src.stats_config import StatsConfig

class LevelConfig:

    def __init__(self, path, camera: Camera, fps, stats_config: StatsConfig,
                 spawner: Spawner, groups: GameStateGroups) -> None:
        self.path = path
        self.df = pd.read_csv(path, sep=';')
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
