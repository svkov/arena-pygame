import pandas as pd

class StatsConfig:

    def __init__(self, path, sprites) -> None:
        self.path = path
        self.sprites = sprites
        self.df = pd.read_csv(path, sep=';', index_col=0)

    def get_by_name(self, name):
        d = self.df.loc[name].to_dict()
        d['image_size'] = d['image_size_x'], d['image_size_y']
        d['image'] = self.sprites[d['image']]
        d['name'] = name
        if d['projectile_image'] in self.sprites:
            d['projectile_image'] = self.sprites[d['projectile_image']]
        return d
