
from typing import List, Tuple
import pygame
from src.global_objects import game_objects, projectile_objects

def spawn_object(obj):
    game_objects.add(obj)

def spawn_projectile(obj):
    projectile_objects.add(obj)

def crop_spritesheet_by_image_size(image: pygame.surface.Surface,
                                   image_size: Tuple[int, int]) -> List[pygame.surface.Surface]:
    width, height = image_size
    full_width, full_height = image.get_size()
    rows = full_width // width
    cols = full_height // height
    matrix_size = (rows, cols)
    return crop_by_matrix_size_and_image_size(image, matrix_size, image_size)


def crop_spritesheet_by_matrix_size(image: pygame.surface.Surface,
                                    matrix_size: Tuple[int, int]) -> List[pygame.surface.Surface]:
    rows, cols = matrix_size
    full_height, full_width = image.get_size()
    width = full_width // rows
    height = full_height // cols
    image_size = (width, height)
    return crop_by_matrix_size_and_image_size(image, matrix_size, image_size)

def crop_by_matrix_size_and_image_size(image: pygame.surface.Surface,
                                       matrix_size: Tuple[int, int],
                                       image_size: Tuple[int, int]) -> List[pygame.surface.Surface]:
    rows, cols = matrix_size
    width, height = image_size
    sprites = []
    for row in range(rows):
        for col in range(cols):
            x = row * width
            x = x - 1 if x > 0 else x
            y = col * height
            y = y - 1 if y > 0 else y
            rect = [x, y, width - 1, height - 1]
            print(rect, image.get_size())
            sprite = image.subsurface(rect)
            sprites.append(sprite)
    return sprites
