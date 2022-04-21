import pygame

from typing import Dict, List

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
        self.duration = duration
        self.fps = fps

    @property
    def images_in_anim(self):
        return len(self.sprites)

    @property
    def one_frame_duration(self):
        return self.duration / self.images_in_anim

    @property
    def one_frame_counter(self):
        return int(self.one_frame_duration * self.fps)

    @property
    def total_frames_to_play(self):
        return self.duration * self.fps

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

    def reset_animation(self):
        self._counter = 0


class AnimationManager:

    def __init__(self, state_to_animation: Dict[int, Animation]) -> None:
        self.state_to_animation = state_to_animation
        self._state = list(self.state_to_animation.keys())[0]

    @property
    def current_animation(self):
        return self.state_to_animation[self._state]

    def set_state(self, new_state):
        self._state = new_state
        self.current_animation.reset_animation()

    def update(self):
        self.current_animation.update()
