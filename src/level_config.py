import pandas as pd
from src.camera import Camera
from src.create_object_function import background, static_object, skeleton, player
from src.stats_config import StatsConfig

map_object_name_to_create_function = {
    'skeleton': skeleton,
    'player': player,
    'background': background,
    'cactus': static_object,
    'tombstone': static_object
}

class LevelConfig:

    def __init__(self, path, camera: Camera, fps, stats_config: StatsConfig) -> None:
        self.path = path
        self.df = pd.read_csv(path, sep=';')
        self.camera = camera
        self.fps = fps
        self.stats_config = stats_config

    def setup_level(self):
        shared_args = {
            'camera': self.camera,
            'fps': self.fps,
            'sprites': self.stats_config.sprites
        }
        for i, row in self.df.iterrows():
            obj_dict = row.to_dict()
            func = map_object_name_to_create_function[obj_dict['object_name']]
            pos = (obj_dict['pos_x'], obj_dict['pos_y'])
            obj_stats = self.stats_config.get_by_name(obj_dict['object_name'])
            spawned_obj = func(pos=pos, **shared_args, **obj_stats)
            if obj_dict['object_name'] == 'player':
                self.player = spawned_obj
