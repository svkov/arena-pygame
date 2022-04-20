import pygame

from src.player import Player


class HUD(pygame.sprite.Sprite):

    def __init__(self, player) -> None:
        self.percent_to_hud = 0.2
        self.hp_pivot = 0.5
        self.hp_height = 30
        self.player: Player = player

    def update(self, *args, **kwargs):
        screen = kwargs['screen']
        resolution = kwargs['screen_resolution']
        font = kwargs['font']
        self.draw_hud_area(screen, resolution)
        # TODO: drawing order should not be fixed
        self.draw_hp(screen, font)
        self.draw_exp(screen, font)
        self.draw_level(screen, font)

    def draw_hud_area(self, screen, resolution):
        self.x_start = (1 - self.percent_to_hud) * resolution[0]
        self.y_start = 0
        self.width = self.percent_to_hud * resolution[0]
        self.height = resolution[1]
        pygame.draw.rect(screen, (255, 255, 255),
                         (self.x_start, self.y_start, self.width, self.height))

    def draw_hp(self, screen, font):
        self.hp_y_start = self.hp_pivot * (self.y_start + self.height)
        self.hp_progress = self.player.hp / self.player.max_hp
        self.draw_progress_bar(
            screen=screen,
            progress=self.hp_progress,
            y_start=self.hp_y_start,
            height=self.hp_height,
            color_back=(255, 0, 0),
            color_front=(0, 255, 0)
        )
        text_content = f'{self.player.hp}/{self.player.max_hp}'
        text_surface = font.render(text_content, False, (255, 255, 255))
        self.draw_text_in_progress_bar(
            screen, self.hp_y_start, self.hp_height, text_surface)

    def draw_exp(self, screen: pygame.surface.Surface, font: pygame.font.Font):
        self.exp_y_start = self.hp_y_start + self.hp_height
        self.exp_progress = self.player.exp / self.player.exp_to_lvlup
        self.draw_progress_bar(
            screen=screen,
            progress=self.exp_progress,
            y_start=self.exp_y_start,
            height=self.hp_height,
            color_back='#b8b8b8',
            color_front='#a32cb8'
        )
        text_content = f'{self.player.exp}/{self.player.exp_to_lvlup}'
        text_surface = font.render(text_content, False, (255, 255, 255))
        self.draw_text_in_progress_bar(screen, self.exp_y_start, self.hp_height, text_surface)

    def draw_level(self, screen: pygame.surface.Surface, font: pygame.font.Font):
        text_content = f'Level: {self.player.level}'
        text_surface = font.render(text_content, False, (0, 0, 0))
        text_size = text_surface.get_size()
        rect = [self.x_start + 5, self.hp_y_start - text_size[1] - 5]
        screen.blit(text_surface, rect)

    def draw_progress_bar(self, screen: pygame.surface.Surface, progress, y_start, height, color_back, color_front):
        rect = [self.x_start, y_start, self.width, height]
        fill_rect = [self.x_start, y_start, self.width * progress, height]

        pygame.draw.rect(screen, color_back, rect)
        pygame.draw.rect(screen, color_front, fill_rect)

    def draw_text_in_progress_bar(self, screen: pygame.surface.Surface, y_start, height, text_surface):
        text_size = text_surface.get_size()
        text_x = self.x_start + (self.width - text_size[0]) // 2
        text_y = y_start + (height - text_size[1]) // 2
        rect = [text_x, text_y, self.width, height]
        screen.blit(text_surface, rect)
