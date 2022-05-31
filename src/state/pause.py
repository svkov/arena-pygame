from typing import Tuple
import pygame
from src.hud import HUD


class PauseState:

    def __init__(self, groups, hud, screen_resolution, pause_font) -> None:
        self.groups = groups
        self.hud: HUD = hud
        self.screen_resolution = screen_resolution
        self.font = pause_font
        self.veil = pygame.surface.Surface(screen_resolution).convert_alpha()
        self.veil.fill((0, 0, 0))
        self.veil.set_alpha(150)

    def update(self, *args, **kwargs):
        screen = kwargs['screen']

        screen.fill((0, 0, 0))
        self.groups.background_group.draw(screen)
        self.groups.draw(screen)
        self.hud.update(screen=screen, screen_resolution=self.screen_resolution)
        text_surface = self.font.render('Paused', False, (255, 255, 255))
        text_size = text_surface.get_size()

        rect_x = self.center_x(text_size)
        rect_y = int(self.screen_resolution[1] * 0.1 + text_size[1])
        screen.blit(self.veil, (0, 0))
        screen.blit(text_surface, [rect_x, rect_y])
        screen.blit(*self.get_realm_info())
        screen.blit(*self.get_score_info())

    def center_x(self, text_size):
        content_percent = 1 - self.hud.hud_config.percent_to_hud
        content_pixels = content_percent * self.screen_resolution[0]
        return (content_pixels - text_size[0]) // 2

    def get_realm_info(self) -> Tuple[pygame.surface.Surface, Tuple[int, int]]:
        realms_surface = self.font.render(f'Closed Realms: {10}', False, (255, 255, 255))
        text_size = realms_surface.get_size()
        rect_x = self.screen_resolution[0] * 0.1
        rect_y = self.screen_resolution[1] * 0.25 + text_size[1]
        return realms_surface, [rect_x, rect_y]

    def get_score_info(self) -> Tuple[pygame.surface.Surface, Tuple[int, int]]:
        scores_surface = self.font.render(f'Score: {100000}', False, (255, 255, 255))
        text_size = scores_surface.get_size()
        rect_x = self.screen_resolution[0] * 0.1
        rect_y = self.screen_resolution[1] * 0.4 + text_size[1]
        return scores_surface, [rect_x, rect_y]
