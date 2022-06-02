import yaml

class GameConfig:

    def __init__(self, path) -> None:
        self.path = path
        self.cfg = self.load_file()
        self.fps = self.cfg['fps']
        self.screen_resolution = (self.cfg['resolution_x'], self.cfg['resolution_y'])
        self.draw_enemy_attention = self.cfg['draw_enemy_attention']
        self.debug = self.cfg['debug']
        self.draw_rects = self.cfg['draw_rects']
        self.spawn_enemies = self.cfg['spawn_enemies']
        self.spawn_static = self.cfg['spawn_static']
        self.last_player_name = self.cfg['last_player_name']

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
            'draw_enemy_attention': self.draw_enemy_attention,
            'debug': self.debug,
            'draw_rects': self.draw_rects,
            'spawn_enemies': self.spawn_enemies,
            'spawn_static': self.spawn_static,
            'last_player_name': self.last_player_name
        }
