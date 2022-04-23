import os
from typing import Dict
import numpy as np
import pygame
from src.camera import Camera
from src.hud import HUD
from src.level_config import LevelConfig
from src.static_object import StaticObject
from src.stats_config import StatsConfig
from src.utils import spawn_static_object, background_group
from src.global_objects import game_objects, projectile_objects, static_objects

running = True

def load_sprites(path_to_assets) -> Dict[str, pygame.surface.Surface]:
    sprites = {}
    for asset in os.listdir(path_to_assets):
        if '.png' in asset:
            path = os.path.join(path_to_assets, asset)
            sprite_name = os.path.splitext(asset)[0]
            sprites[sprite_name] = pygame.image.load(path).convert_alpha()
    return sprites


def setup_object_randomly(background, radius, sprites, n_sample=15, sprite_name='cactus', image_size=None):
    if image_size is None:
        image_size = (128, 256)
    top_right_x = background.center[0] + np.sin(np.pi / 4) * radius
    top_right_y = background.center[1] + np.cos(np.pi / 4) * radius
    bottom_left_x = background.center[0] - np.sin(np.pi / 4) * radius
    bottom_left_y = background.center[1] - np.cos(np.pi / 4) * radius
    object_pos_x = np.random.randint(bottom_left_x, top_right_x, size=(n_sample, 1))
    object_pos_y = np.random.randint(bottom_left_y, top_right_y, size=(n_sample, 1))
    object_poses = np.hstack((object_pos_x, object_pos_y))
    for object_i in range(n_sample):
        pos = object_poses[object_i]
        obj = StaticObject(pos, sprites[sprite_name], image_size=image_size)
        spawn_static_object(obj)

def setup_scene(camera, sprites, fps):
    stats_config = StatsConfig('resources/stats.csv', sprites)
    level_config = LevelConfig('resources/level1.csv', camera, fps, stats_config)
    level_config.setup_level()
    # setup_object_randomly(background, radius, sprites)
    # setup_object_randomly(background, radius, sprites, n_sample=10, sprite_name='tombstone')
    return level_config.player


def handle_input_keyboard():
    global running
    keyboard = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if keyboard[pygame.K_q]:
        running = False


def main():
    pygame.init()
    pygame.display.set_caption("Arena")
    pygame.font.init()
    my_font = pygame.font.SysFont(pygame.font.get_default_font(), 28)
    fps = 30

    clock = pygame.time.Clock()
    screen_resolution = (1920, 1080)
    screen = pygame.display.set_mode(screen_resolution)
    sprites = load_sprites('assets')
    camera = Camera(0, 0, screen_resolution)
    player = setup_scene(camera, sprites, fps)
    hud = HUD(player)

    while running:
        dt = clock.tick(fps)
        handle_input_keyboard()

        update_kwargs = {
            'screen': screen,
            'dt': dt,
            'camera': camera,
            'sprites': sprites
        }

        game_objects.update(**update_kwargs)
        background_group.update(**update_kwargs)
        static_objects.update(**update_kwargs)
        projectile_objects.update(**update_kwargs)

        for game_obj in game_objects:
            collided_objects = pygame.sprite.spritecollide(game_obj, static_objects, False)
            for collided in collided_objects:
                collided.on_collision(game_obj, dt, screen, camera)

        for static in static_objects:
            pygame.sprite.spritecollide(static, projectile_objects, True)

        for projectile in projectile_objects:
            for game_obj in game_objects:
                collide = projectile.rect.colliderect(game_obj.rect)
                if collide:
                    projectile.on_collision(game_obj)
                    game_obj.on_collision(projectile)

        screen.fill((0, 0, 0))
        background_group.draw(screen)
        static_objects.draw(screen)
        game_objects.draw(screen)
        projectile_objects.draw(screen)

        hud.update(screen=screen, screen_resolution=screen_resolution, font=my_font)
        pygame.display.flip()


if __name__ == "__main__":
    main()
