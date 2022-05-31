import pygame

from typing import Dict, List
from src.core.camera import Camera

from src.utils import crop_spritesheet_by_image_size, crop_spritesheet_by_matrix_size, preresize_image_list

class Animation:

    def __init__(self, spritesheet, duration, fps, camera: Camera,
                 image_size=None, matrix_size=None, scene_image_size=None, times_to_play=None):
        self.camera = camera
        if scene_image_size is None:
            scene_image_size = (128, 128)
        self.scene_image_size = scene_image_size
        self.sprites: List[pygame.surface.Surface] = self.get_sprites(spritesheet, image_size, matrix_size)
        self.sprites_by_zoom = preresize_image_list(self.sprites, self.camera, self.scene_image_size)
        self._counter = 0
        self.image_counter = 0
        self.duration = duration
        self.fps = fps
        self.times_played = 0
        self.times_to_play = times_to_play
        if times_to_play is not None:
            self.times_to_play = times_to_play
        self._is_playing = True

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

    def update(self):
        if self._is_playing:
            self._counter += 1
            if self.one_frame_counter == self._counter:
                self.next_image()
                self._counter = 0
        else:
            self.image_counter = self.images_in_anim - 1

    def next_image(self):
        self.image_counter += 1
        if self.image_counter == self.images_in_anim:
            self.image_counter = 0
            self.times_played += 1
            self.stop_play_if_enough()

    def stop_play_if_enough(self):
        if self.times_to_play is None:
            return
        if self.times_played == self.times_to_play:
            self.image_counter = self.images_in_anim - 1
            self._is_playing = False

    @property
    def is_playing(self):
        return self._is_playing and self.times_to_play is not None

    def get_image(self):
        return self.sprites_by_zoom[self.camera.zoom_factor][self.image_counter]

    def reset_animation(self):
        self._counter = 0
        self.times_played = 0
        self.image_counter = 0
        self._is_playing = True


class AnimationManager:

    def __init__(self, state_to_animation: Dict[int, Animation], default_state) -> None:
        self.state_to_animation = state_to_animation
        self._state = list(self.state_to_animation.keys())[0]
        self.next_state = self._state
        self.default_state = default_state

    @property
    def current_animation(self):
        return self.state_to_animation[self._state]

    @property
    def next_animation(self):
        return self.state_to_animation[self.next_state]

    @property
    def image(self):
        return self.current_animation.get_image()

    @property
    def is_busy(self):
        return self.current_animation.is_playing

    def set_state(self, new_state, force=False):
        if force:
            self._state = new_state
            self.next_state = None
            self.current_animation.reset_animation()
        if self.current_animation.is_playing:
            self.next_state = new_state
            return
        self._state = new_state
        self.current_animation.reset_animation()

    def update(self):
        if not self.is_busy:
            if self.next_state is None:
                self._state = self.default_state
            else:
                self._state = self.next_state
                self.next_state = None
        self.current_animation.update()
