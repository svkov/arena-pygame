import os
import pygame


class SpriteLoader:

    def __init__(self, path) -> None:
        self.path = path
        self.sprites = {}

    def load(self):
        for asset in os.listdir(self.path):
            if '.png' in asset:
                path = os.path.join(self.path, asset)
                sprite_name = os.path.splitext(asset)[0]
                self.sprites[sprite_name] = pygame.image.load(path).convert_alpha()

    def get_sprite(self, name, image_size):
        return pygame.transform.smoothscale(self.sprites[name], image_size)

    def __getitem__(self, item):
        return self.sprites[item]

    def __contains__(self, item):
        return item in self.sprites
