import os
from typing import Dict
import pygame
from src.state.game import GameState

class Game:

    def __init__(self) -> None:
        self.fps = 30
        self.screen_resolution = (1920, 1080)
        self.screen = pygame.display.set_mode(self.screen_resolution)
        self.sprites = Game.load_sprites('assets')
        self.running = True
        self.state = GameState(self.screen_resolution, self.fps, self.sprites)
        self.clock = pygame.time.Clock()

    def handle_input_keyboard(self):
        keyboard = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        if keyboard[pygame.K_q]:
            self.running = False

    @staticmethod
    def load_sprites(path_to_assets) -> Dict[str, pygame.surface.Surface]:
        sprites = {}
        for asset in os.listdir(path_to_assets):
            if '.png' in asset:
                path = os.path.join(path_to_assets, asset)
                sprite_name = os.path.splitext(asset)[0]
                sprites[sprite_name] = pygame.image.load(path).convert_alpha()
        return sprites

    def update(self):
        dt = self.clock.tick(self.fps)
        self.handle_input_keyboard()

        update_kwargs = {
            'screen': self.screen,
            'dt': dt,
            'sprites': self.sprites
        }
        self.state.update(**update_kwargs)
