import pygame

from typing import List

from src.utils import crop_spritesheet_by_image_size, crop_spritesheet_by_matrix_size

class Animation:

    def __init__(self, spritesheet, duration, fps, image_size=None, matrix_size=None, scene_image_size=None):
        if scene_image_size is None:
            scene_image_size = (128, 128)
        self.scene_image_size = scene_image_size
        self.sprites: List[pygame.surface.Surface] = self.get_sprites(spritesheet, image_size, matrix_size)
        self.resize_sprites()
        self._counter = 0
        self.image_counter = 0
        self.images_in_anim = len(self.sprites)
        self.duration = duration
        self.one_frame_duration = self.duration / self.images_in_anim
        self.fps = fps
        self.one_frame_counter = int(self.one_frame_duration * self.fps)
        self.total_frames_to_play = self.duration * self.fps

    def get_sprites(self, spritesheet, image_size, matrix_size):
        sprites = []
        if image_size is not None:
            sprites = crop_spritesheet_by_image_size(spritesheet, image_size)
        if matrix_size is not None:
            sprites = crop_spritesheet_by_matrix_size(spritesheet, matrix_size)
        if sprites is None:
            raise ValueError('must specify image size or matrix size')
        return sprites

    def resize_sprites(self):
        for i, sprite in enumerate(self.sprites):
            self.sprites[i] = pygame.transform.scale(sprite, self.scene_image_size)

    def update(self):
        self._counter += 1
        if self.one_frame_counter == self._counter:
            self.next_image()
            self._counter = 0

    def next_image(self):
        self.image_counter += 1
        if self.image_counter == self.images_in_anim:
            self.image_counter = 0

    def get_image(self):
        return self.sprites[self.image_counter]
