from __future__ import annotations
from typing import TYPE_CHECKING

import pygame
if TYPE_CHECKING:
    from src.game_object.player import Player


class InputHandler:

    def __init__(self, player: Player) -> None:
        self.player = player

    def handle_input(self, events):
        keyboard = pygame.key.get_pressed()
        self.handle_events(events)
        self.handle_keyboard_input(keyboard)
        self.handle_mouse_input()

    def handle_events(self, events):
        self.player.is_interacting = False
        for event in events:
            self.handle_zoom_event(event)
            self.handle_mouse_event(event)
            self.handle_interacting_event(event)

    def handle_keyboard_input(self, keyboard):
        self.player.set_zero_speed()
        if keyboard[pygame.K_w]:
            self.player.speed[1] = -1
        if keyboard[pygame.K_s]:
            self.player.speed[1] = 1
        if keyboard[pygame.K_a]:
            self.player.speed[0] = -1
            self.player.is_going_left = True
        if keyboard[pygame.K_d]:
            self.player.speed[0] = 1
        self.player.normalize_speed()

    def handle_mouse_input(self):
        if pygame.mouse.get_pressed()[0] and self.player.cooldowns['shoot'].is_cooldown_over:
            self.player.shoot()
        self.player.check_item_description_spawn()

    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.player.check_if_item_used()
            if event.button == 3:
                self.player.check_if_item_dropped()

    def handle_zoom_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.player.camera.zoom_out()
            elif event.button == 5:
                self.player.camera.zoom_in()

    def handle_interacting_event(self, event):
        if event.type == pygame.KEYUP and event.key == pygame.K_f:
            self.player.is_interacting = True
