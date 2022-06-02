import pygame
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
        return GameState(self, self.screen_resolution, self.fps, self.sprites)

    def create_menu_game_fader(self):
        return Fader([self.states['menu'], self.states['game']], callback=self.set_game_state)

    def handle_input_keyboard(self):
        keyboard = pygame.key.get_pressed()
        if keyboard[pygame.K_ESCAPE]:
            self.running = False

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
        score = game.calculate_score()
        self.high_scores.add('player', game.level_number, score)
        self.states['game'] = None
        self.fader.next()
        self.go_to_menu()

    def win(self):
        self.go_to_menu()
        self.init_level()

    def restart_game(self):
        game: GameState = self.states['game']
        score = game.calculate_score()
        self.high_scores.add(game.player_name, game.level_number, score)
        self.states['game'] = None
        self.start_game()
