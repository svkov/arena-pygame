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

    def save(self):
        with open(self.path, 'w') as stream:
            yaml.safe_dump(self.to_dict(), stream)

    def to_dict(self):
        return {
            'fps': self.fps,
            'resolution_x': self.screen_resolution[0],
            'resolution_y': self.screen_resolution[1],
            'draw_enemy_attention': self.draw_enemy_attention
        }
