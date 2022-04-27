import yaml

class GameConfig:

    def __init__(self, path) -> None:
        self.path = path
        self.cfg = self.load_file()
        self.fps = self.cfg['fps']
        self.screen_resolution = (self.cfg['resolution_x'], self.cfg['resolution_y'])
        self.draw_enemy_attention = self.cfg['draw_enemy_attention']

    def load_file(self):
        with open(self.path, "r") as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
