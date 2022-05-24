
from typing import List, Tuple
import pygame

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
            sprite = image.subsurface(rect)
            sprites.append(sprite)
    return sprites

def preresize_image(image, camera, default_image_size):
    zoom_factors = camera.get_all_zoom_factors()
    image_by_zoom = {}
    for zoom in zoom_factors:
        new_image_size = (int(default_image_size[0] * zoom), int(default_image_size[1] * zoom))
        image_by_zoom[float(zoom)] = pygame.transform.scale(image, new_image_size)
    return image_by_zoom

def preresize_image_list(image_list, camera, default_image_size):
    image_sheet_by_zoom = {}
    zoom_factors = camera.get_all_zoom_factors()
    for zoom in zoom_factors:
        image_list_ = []
        for image in image_list:
            new_image_size = (int(default_image_size[0] * zoom), int(default_image_size[1] * zoom))
            image_list_.append(pygame.transform.scale(image, new_image_size))
        image_sheet_by_zoom[zoom] = image_list_
    return image_sheet_by_zoom
