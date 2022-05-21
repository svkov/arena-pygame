import numpy as np
import pygame

from src.camera import Camera
from src.groups import GameStateGroups
from src.hud import HUD
from src.level_config import LevelConfig
from src.player import Player
from src.spawner import Spawner
from src.state.pause import PauseState
from src.static_object import StaticObject
from src.stats_config import StatsConfig
import gc

class GameState:
    def __init__(self, game, screen_resolution, fps, sprites) -> None:
        self.game = game
        self.hud_font = pygame.font.SysFont(pygame.font.get_default_font(), 28)
        self.pause_font = pygame.font.SysFont(pygame.font.get_default_font(), 72)
        self.screen_resolution = screen_resolution
        self.fps = fps
        self.sprites = sprites
        self.camera = Camera(0, 0, screen_resolution)
        self.groups = GameStateGroups()
        self.spawner = Spawner(self.groups)
        self.setup_scene()
        self.paused = False
        self.pause = PauseState(self.groups, self.hud, self.screen_resolution, self.pause_font)

    def setup_scene(self, keep_player=False):
        stats_config = StatsConfig('resources/stats.csv', self.sprites)
        level_config = LevelConfig('resources/level2.csv', self.camera, self.fps,
                                   stats_config, self.spawner, self.groups)
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
        del self.groups
        del self.spawner
        self.groups = GameStateGroups()
        self.spawner = Spawner(self.groups)
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
                if event.key == pygame.K_p:
                    self.paused = not self.paused

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
            self._update_paused(screen=screen)

    def _update(self, screen, update_kwargs):
        if not self.player.is_alive:
            self.game.game_over()
        if self.player.is_in_portal:
            self.clear_scene_for_next_level()
            self.setup_scene(keep_player=True)
        screen.fill((0, 0, 0))
        self.groups.background_group.draw(screen)
        self.groups.update(update_kwargs)
        self.groups.handle_collisions(update_kwargs)

        self.groups.draw(screen)
        self.hud.update(screen=screen, screen_resolution=self.screen_resolution, font=self.hud_font)
        self.groups.items_in_inventory.draw(screen)
        self.groups.items_description.draw(screen)

    def _update_paused(self, *args, **kwargs):
        self.pause.update(*args, **kwargs)

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
