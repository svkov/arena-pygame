import pygame
from src.config.stats_config import StatsConfig
from src.core.fader import Fader
from src.core.high_score import HighScores
from src.core.sprite_loader import SpriteLoader
from src.config.game_config import GameConfig
from src.state.game import GameState
from src.state.menu import MenuState

class Game:

    def __init__(self) -> None:
        self.config = GameConfig('config.yaml')
        self.high_scores = HighScores()
        self.fps = self.config.fps
        self.screen_resolution = self.config.screen_resolution
        self.screen = pygame.display.set_mode(self.screen_resolution, pygame.SRCALPHA)
        self.sprites = SpriteLoader('assets')
        self.sprites.load()
        self.stats_config = StatsConfig('resources/stats.csv', self.sprites)
        self.running = True
        self.init_level()
        self.clock = pygame.time.Clock()

    def init_level(self):
        menu = MenuState(self, self.screen_resolution)
        self.states = {
            'game': self.create_game_state(),
            'menu': menu,
            # TODO: make game over screen
            'game_over': menu,
        }
        self.go_to_menu()
        self.fader = self.create_menu_game_fader()

    def create_game_state(self):
        return GameState(self, self.screen_resolution, self.fps, self.sprites, self.stats_config)

    def create_menu_game_fader(self):
        return Fader([self.states['menu'], self.states['game']], callback=self.set_game_state)

    def update(self):
        dt = self.clock.tick(self.fps)

        update_kwargs = {
            'screen': self.screen,
            'dt': dt,
            'sprites': self.sprites,
            'draw_enemy_attention': self.config.draw_enemy_attention,
            'debug': self.config.debug
        }
        self.fader.update(**update_kwargs)
        # pygame.display.flip()
        pygame.display.update()

    def start_game(self):
        if self.states['game'] is None:
            self.states['game'] = self.create_game_state()
            self.fader = self.create_menu_game_fader()
        self.fader.next()

    def set_game_state(self):
        self.state = self.states['game']

    def go_to_menu(self):
        self.state = self.states['menu']

    def game_over(self):
        game: GameState = self.states['game']
        self.update_high_score(game)
        self.states['game'] = None
        self.fader.next()
        self.go_to_menu()

    def win(self):
        self.go_to_menu()
        self.init_level()

    def restart_game(self):
        game: GameState = self.states['game']
        self.update_high_score(game)
        self.states['game'] = None
        self.start_game()

    def update_high_score(self, game):
        new_player_name = game.player_name
        if new_player_name != self.config.last_player_name:
            self.config.last_player_name = new_player_name
            self.config.save()
        self.high_scores.add(new_player_name, game.level_number, game.calculate_score())
