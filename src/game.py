import os
from typing import Dict
import pygame
from src.fader import Fader
from src.game_config import GameConfig
from src.state.game import GameState
from src.state.menu import MenuState

class Game:

    def __init__(self) -> None:
        self.config = GameConfig('config.yaml')
        self.fps = self.config.fps
        self.screen_resolution = self.config.screen_resolution
        self.screen = pygame.display.set_mode(self.screen_resolution)
        self.sprites = Game.load_sprites('assets')
        self.running = True
        self.init_level()
        self.clock = pygame.time.Clock()

    def init_level(self):
        self.states = {
            'game': GameState(self, self.screen_resolution, self.fps, self.sprites),
            'menu': MenuState(self, self.screen_resolution),
            # TODO: make game over screen
            'game_over': MenuState(self, self.screen_resolution),
        }
        self.go_to_menu()
        self.fader = Fader([self.states['menu'], self.states['game']], callback=self.set_game_state)

    def handle_input_keyboard(self):
        keyboard = pygame.key.get_pressed()
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
            'sprites': self.sprites,
            'draw_enemy_attention': self.config.draw_enemy_attention,
            'debug': self.config.debug
        }
        self.fader.update(**update_kwargs)
        pygame.display.flip()

    def start_game(self):
        self.fader.next()

    def set_game_state(self):
        self.state = self.states['game']

    def go_to_menu(self):
        self.state = self.states['menu']

    def game_over(self):
        self.go_to_menu()
        self.fader.next()

    def win(self):
        self.go_to_menu()
        self.init_level()
