import numpy as np
import pygame
import pygame_menu

from src.core.camera import Camera
from src.core.groups import GameStateGroups
from src.core.spawner import Spawner
from src.hud import HUD
from src.config.level_config import LevelConfig, RandomLevelConfig
from src.config.stats_config import StatsConfig
from src.game_object.player import Player
from src.game_object.static_object import StaticObject
import gc

class GameState:
    def __init__(self, game, screen_resolution, fps, sprites) -> None:
        self.game = game
        self.hud_font = pygame.font.SysFont(pygame.font.get_default_font(), 28)
        self.pause_font = pygame.font.SysFont(pygame.font.get_default_font(), 72)
        self.screen_resolution = screen_resolution
        self.fps = fps
        self.sprites = sprites
        self.level_number = 1
        self.stats_config = StatsConfig('resources/stats.csv', self.sprites)
        self.camera = Camera(0, 0, self.screen_resolution)
        self.groups = GameStateGroups()
        self.spawner = Spawner(self.groups, self.camera, self.stats_config, self.fps, self.sprites, self.game.config)
        self.setup_scene()
        self.paused = False
        self.is_fading = False
        self.init_game_over_menu()
        self.init_pause_menu()

    def init_game_over_menu(self):
        self.game_over_menu = pygame_menu.Menu(
            width=self.screen_resolution[0] * 0.8,
            height=self.screen_resolution[1] * 0.8,
            theme=pygame_menu.themes.THEME_DEFAULT,
            title='Game Over',
        )
        self.game_over_menu.add.label(f'Score: {self.calculate_score()}')
        self.game_over_menu.add.label('Your name:')
        self.player_name_widget = self.game_over_menu.add.text_input('', default=self.game.config.last_player_name)
        self.game_over_menu.add.button('Start new game', self.game.restart_game)
        self.game_over_menu.add.button('Exit to main menu', self.game.game_over)

    def init_pause_menu(self):
        self.pause_menu = pygame_menu.Menu(
            width=self.screen_resolution[0] * 0.8,
            height=self.screen_resolution[1] * 0.8,
            theme=pygame_menu.themes.THEME_DEFAULT,
            title='Pause'
        )
        self.pause_menu.add.label(f'Score: {self.calculate_score()}')
        self.pause_menu.add.label(f'Realms closed: {self.level_number - 1}')
        self.pause_menu.add.button('Continue', self.unpause)
        self.pause_menu.add.button('Exit to main menu', self.game.game_over)

    def unpause(self):
        self.paused = False
        self.pause_menu.disable()

    def pause(self):
        self.paused = True
        self.pause_menu.enable()

    @property
    def player_name(self):
        return self.player_name_widget.get_value()

    def calculate_score(self):
        return int(sum(self.player.kills.values()) + (self.level_number - 1) * 1000)

    def setup_scene(self, keep_player=False):
        try:
            # raise FileNotFoundError()
            level_config = LevelConfig(self.level_number, self.spawner)
        except FileNotFoundError:
            level_config = RandomLevelConfig(self.level_number, self.spawner, self.game.config)
        level_config.setup_level()
        # setup_object_randomly(background, radius, sprites)
        # setup_object_randomly(background, radius, sprites, n_sample=10, sprite_name='tombstone')
        if keep_player and self.player is not None:
            old_player = self.player
            self.player = Player.recreate_player(old_player, level_config.player)
        else:
            self.player = level_config.player
        self.hud = HUD(self.player, self.hud_font)
        self.player.hud = self.hud

    def clear_scene(self):
        del self.camera
        del self.groups
        del self.spawner
        self.camera = Camera(0, 0, self.screen_resolution)
        self.groups = GameStateGroups()
        self.spawner = Spawner(self.groups, self.camera, self.stats_config, self.fps, self.sprites, self.game.config)
        # Run GC to collect old groups and spawner (they have cycles in player object and somewhere else)
        # If not to run, app will alloc more memory than needed
        # There is no memory leak, but it works better using GC
        gc.collect()

    def clear_scene_for_next_level(self):
        self.groups.clear_before_next_level()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    if self.paused:
                        self.unpause()
                    else:
                        self.pause()

    def update(self, **kwargs):
        events = pygame.event.get()
        self.handle_events(events)
        screen = kwargs['screen']

        update_kwargs = {
            **kwargs,
            'camera': self.camera,
            'groups': self.groups,
            'events': events
        }

        if not self.paused:
            self._update(screen, update_kwargs)
        else:
            self._update_paused(screen, events)

    def _update(self, screen, update_kwargs):
        if not self.player.is_alive and not self.is_fading:
            self._update_game_over(screen, update_kwargs)
            return
        if self.player.is_in_portal:
            self.clear_scene_for_next_level()
            self.level_number += 1
            self.setup_scene(keep_player=True)
        self._update_and_draw(screen, update_kwargs)

    def _update_and_draw(self, screen, update_kwargs):
        screen.fill((0, 0, 0))
        self.groups.update(update_kwargs)
        self.groups.handle_collisions(update_kwargs)

        self.groups.draw(screen)
        self.hud.update(screen=screen, screen_resolution=self.screen_resolution, font=self.hud_font)
        self.groups.items_in_inventory.draw(screen)
        self.groups.items_description.draw(screen)

    def _update_paused(self, screen, events):
        self.pause_menu.update(events)
        if self.pause_menu.is_enabled():
            self.pause_menu.draw(screen)

    def _update_game_over(self, screen, update_kwargs):
        self._update_and_draw(screen, update_kwargs)
        self._draw_game_over_menu(screen, update_kwargs['events'])

    def _draw_game_over_menu(self, screen, events):
        self.game_over_menu.update(events)
        veil = pygame.surface.Surface(self.screen_resolution, pygame.SRCALPHA)
        veil.fill((0, 0, 0, 128))
        screen.blit(veil, (0, 0))
        self.game_over_menu.draw(screen)

    def setup_object_randomly(self, background, radius, sprites, n_sample=15, sprite_name='cactus', image_size=None):
        if image_size is None:
            image_size = (128, 256)
        top_right_x = background.center[0] + np.sin(np.pi / 4) * radius
        top_right_y = background.center[1] + np.cos(np.pi / 4) * radius
        bottom_left_x = background.center[0] - np.sin(np.pi / 4) * radius
        bottom_left_y = background.center[1] - np.cos(np.pi / 4) * radius
        object_pos_x = np.random.randint(bottom_left_x, top_right_x, size=(n_sample, 1))
        object_pos_y = np.random.randint(bottom_left_y, top_right_y, size=(n_sample, 1))
        object_poses = np.hstack((object_pos_x, object_pos_y))
        for object_i in range(n_sample):
            pos = object_poses[object_i]
            obj = StaticObject(pos, sprites[sprite_name], image_size=image_size)
            self.spawn_static_object(obj)
