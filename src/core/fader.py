from itertools import cycle

import pygame


class Fader:

    def __init__(self, scenes, callback):
        self.callback = callback
        self.scenes = cycle(scenes)
        self.scene = next(self.scenes)
        self.fading = None
        self.alpha = 0
        sr = pygame.display.get_surface().get_rect()
        self.veil = pygame.Surface(sr.size)
        self.veil.fill((0, 0, 0))

    def next(self):
        if not self.fading:
            self.fading = 'OUT'
            self.alpha = 0

    def do_fading(self, update_kwargs):
        if self.fading == 'OUT':
            self.alpha += 8
            if self.alpha >= 255:
                self.fading = 'IN'
                self.scene = next(self.scenes)
        elif self.fading == 'IN':
            self.alpha -= 8
            if self.alpha <= 0:
                self.fading = None
                self.callback()

    def draw(self, screen, kwargs):
        self.scene.update(**kwargs)
        if self.fading:
            self.veil.set_alpha(self.alpha)
            screen.blit(self.veil, (0, 0))

    def update(self, **kwargs):
        screen = kwargs['screen']
        self.draw(screen, kwargs)
        self.do_fading(kwargs)
