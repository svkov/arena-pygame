from typing import Tuple
import numpy as np
import pygame
from src.hud_config import HUDConfig

from src.player import Player


class HUD(pygame.sprite.Sprite):

    def __init__(self, player, font) -> None:
        self.player: Player = player
        self.font = font
        self.hud_config: HUDConfig = HUDConfig()
        self.info_description = ''
        self.current_y = 0

    def update(self, *args, **kwargs):
        screen = kwargs['screen']
        resolution = kwargs['screen_resolution']
        self.draw_hud_area(screen, resolution)
        self.current_y = self.hud_config.hp_pivot * (self.y_start + self.height)
        self.draw_stats(screen)
        self.draw_hp(screen)
        self.draw_exp(screen)
        self.draw_inventory(screen)
        self.draw_info_field(screen, self.info_description)
        self.info_description = ''

    def draw_hud_area(self, screen, resolution):
        self.x_start = (1 - self.hud_config.percent_to_hud) * resolution[0]
        self.y_start = 0
        self.width = self.hud_config.percent_to_hud * resolution[0]
        self.height = resolution[1]
        pygame.draw.rect(screen, (255, 255, 255),
                         (self.x_start, self.y_start, self.width, self.height))

    def draw_hp(self, screen):
        self.hp_progress = self.player.hp / self.player.max_hp
        self.draw_progress_bar(
            screen=screen,
            progress=self.hp_progress,
            y_start=self.current_y,
            height=self.hud_config.hp_height,
            color_back=(255, 0, 0),
            color_front=(0, 255, 0)
        )
        text_content = f'{int(self.player.hp)}/{int(self.player.max_hp)}'
        text_surface = self.font.render(text_content, False, (255, 255, 255))
        self.draw_text_in_progress_bar(
            screen, self.current_y, self.hud_config.hp_height, text_surface)

        self.current_y += self.hud_config.hp_height + self.hud_config.margin

    def draw_exp(self, screen: pygame.surface.Surface):
        self.exp_y_start = self.current_y
        self.exp_progress = self.player.exp / self.player.exp_to_lvlup
        self.draw_progress_bar(
            screen=screen,
            progress=self.exp_progress,
            y_start=self.exp_y_start,
            height=self.hud_config.hp_height,
            color_back=self.hud_config.panel_color,
            color_front='#a32cb8'
        )
        text_content = f'{int(self.player.exp)}/{int(self.player.exp_to_lvlup)}'
        text_surface = self.font.render(text_content, False, (255, 255, 255))
        self.draw_text_in_progress_bar(screen, self.exp_y_start, self.hud_config.hp_height, text_surface)
        self.current_y += self.hud_config.hp_height + self.hud_config.margin

    def draw_inventory(self, screen):
        height = self.hud_config.inventory_height_percent * self.height
        rect = [
            self.x_start,
            self.current_y,
            self.width,
            height
        ]
        pygame.draw.rect(screen, self.hud_config.panel_color, rect)
        inventory_height = self.player.inventory.height
        inventory_width = self.player.inventory.width
        one_cell_width = self.width // inventory_width
        one_cell_height = height // inventory_height
        for cell_i in range(inventory_width):
            for cell_j in range(inventory_height):
                rect = [
                    self.x_start + cell_i * one_cell_width,
                    self.current_y + cell_j * one_cell_height,
                    one_cell_width,
                    one_cell_height
                ]
                item = self.player.inventory.get_item(cell_j, cell_i)
                self.draw_inventory_cell(screen, rect, item)
        self.current_y += height + self.hud_config.margin * 2

    def draw_inventory_cell(self, screen, rect, item):
        pygame.draw.rect(screen, self.hud_config.inventory_cell_color, rect, 1)
        if item is not None:
            item.set_image_size((rect[2] - 2, rect[3] - 2))
            item.pos = [rect[0], rect[1]]

    def draw_info_field(self, screen, content):
        rect = [
            self.x_start,
            self.current_y,
            self.width,
            self.hud_config.info_height_percent * self.height
        ]
        pygame.draw.rect(screen, self.hud_config.panel_color, rect)
        if len(content) == 0:
            return
        self.current_y += self.hud_config.margin
        text_surface = self.font.render(content, False, (255, 255, 255))
        width, height = text_surface.get_size()
        num_of_lines = int(np.ceil(width / self.width))
        content_per_line = len(content) // num_of_lines
        for line in range(num_of_lines):
            start_of_line = line * content_per_line
            end_of_line = (line + 1) * content_per_line
            if line == num_of_lines - 1:
                line_content = content[start_of_line:]
            else:
                line_content = content[start_of_line:end_of_line]
            line_surface = self.font.render(line_content, False, (255, 255, 255))
            self.draw_text(screen, line_surface, self.current_y, self.x_start)
            self.current_y += height

    def draw_stats(self, screen: pygame.surface.Surface):
        self.draw_stats_area(screen)
        content_str = f'STR: {int(self.player.stats.strength)}'
        content_def = f'DEF: {int(self.player.stats.defense)}'
        content_int = f'INT: {int(self.player.stats.intelligence)}'
        content_agi = f'AGI: {int(self.player.stats.agility)}'
        content_spd = f'SPD: {int(self.player.stats.speed)}'
        content_lvl = f'LVL: {int(self.player.level)}'
        indent = 100
        text_size = self.draw_text_tuple(
            screen,
            self.font,
            self.current_y,
            self.x_start,
            [content_str, content_def],
            indent=indent
        )
        self.current_y += text_size[1] + self.hud_config.margin
        text_size = self.draw_text_tuple(
            screen,
            self.font,
            self.current_y,
            self.x_start,
            [content_int, content_agi],
            indent=indent
        )
        self.current_y += text_size[1] + self.hud_config.margin
        text_size = self.draw_text_tuple(
            screen,
            self.font,
            self.current_y,
            self.x_start,
            [content_spd, content_lvl],
            indent=indent
        )
        self.current_y += text_size[1] + self.hud_config.margin

    def draw_stats_area(self, screen: pygame.surface.Surface):
        pygame.draw.rect(screen, self.hud_config.panel_color,
                         (self.x_start, self.current_y - 5, self.width,
                          (self.hud_config.hp_height + self.hud_config.margin) * 2 + 5))

    def draw_text_tuple(self, screen, font, y_start, x_start, content: Tuple[str, str], color=None, indent=10):
        if color is None:
            color = (255, 255, 255)
        full_width = 0
        full_height = 0
        for content_i in content:
            text_surface = font.render(content_i, False, color)
            text_size = text_surface.get_size()
            x_start += indent
            full_width += indent
            full_height = max(full_height, text_size[1])
            self.draw_text(screen, text_surface, y_start, x_start)
        full_width -= indent
        return (full_width, full_height)

    def draw_text(self, screen, text_surface, y_start, x_start):
        rect = [x_start, y_start]
        screen.blit(text_surface, rect)

    def draw_level(self, screen: pygame.surface.Surface, font: pygame.font.Font):
        text_content = f'Level: {int(self.player.level)}'
        text_surface = font.render(text_content, False, (0, 0, 0))
        text_size = text_surface.get_size()
        rect = [self.x_start + 5, self.current_y]
        screen.blit(text_surface, rect)
        self.current_y += text_size[1] + self.hud_config.margin

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
