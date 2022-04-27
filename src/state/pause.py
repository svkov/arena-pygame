import pygame
from src.hud import HUD


class PauseState:

    def __init__(self, groups, hud, screen_resolution, pause_font) -> None:
        self.groups = groups
        self.hud: HUD = hud
        self.screen_resolution = screen_resolution
        self.pause_font = pause_font
        self.veil = pygame.surface.Surface(screen_resolution).convert_alpha()
        self.veil.fill((0, 0, 0))
        self.veil.set_alpha(150)

    def update(self, *args, **kwargs):
        screen = kwargs['screen']

        screen.fill((0, 0, 0))
        self.groups.background_group.draw(screen)
        self.groups.draw(screen)
        self.hud.update(screen=screen, screen_resolution=self.screen_resolution)
        text_surface = self.pause_font.render('Paused', False, (255, 255, 255))
        text_size = text_surface.get_size()

        rect_x = (((1 - self.hud.hud_config.percent_to_hud) * self.screen_resolution[0]) - text_size[0]) // 2
        rect_y = int(self.screen_resolution[1] * 0.1 + text_size[1])
        screen.blit(self.veil, (0, 0))
        screen.blit(text_surface, [rect_x, rect_y])
