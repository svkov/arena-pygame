import os
from typing import Dict
import numpy as np
import pygame
from src.animated_enemy import AnimatedEnemy
from src.camera import Camera
from src.container import Container
from src.game_object import GameObject
from src.hud import HUD
from src.skeleton import generate_skeleton_states
from src.utils import spawn_background, spawn_object, spawn_static_object, background_group
from src.global_objects import game_objects, projectile_objects, static_objects
from src.player import Player

running = True

def load_sprites(path_to_assets) -> Dict[str, pygame.surface.Surface]:
    sprites = {}
    for asset in os.listdir(path_to_assets):
        if '.png' in asset:
            path = os.path.join(path_to_assets, asset)
            sprite_name = os.path.splitext(asset)[0]
            sprites[sprite_name] = pygame.image.load(path).convert_alpha()
    return sprites

def setup_scene(camera, sprites, fps):
    background = GameObject((0, 0), sprites['background'], (8000, 8000))
    spawn_background(background)

    player = Player(background.center, sprites['knight'], max_hp=100, hp=100,
                    camera=camera, projectile_image=sprites['snow'])
    spawn_object(player)

    for alpha in np.linspace(0, 2 * np.pi, 100):
        pos = background.center
        new_pos_x = pos[0] + np.sin(alpha) * 3600
        new_pos_y = pos[1] + np.cos(alpha) * 3600
        pos = [new_pos_x, new_pos_y]
        wall = GameObject(pos, sprites['wall_without_contour'], (512, 512))
        spawn_static_object(wall)

    chest = Container((500, 500), sprites['chest'], max_hp=100, hp=50)
    spawn_object(chest)

    skeleton_states = generate_skeleton_states(sprites, fps)

    anim_skeleton = AnimatedEnemy((player.pos[0] + 200, player.pos[1] + 300), sprites['skeleton'],
                                  max_hp=100, hp=100, animation_states=skeleton_states,
                                  projectile_image=sprites['snow'])
    spawn_object(anim_skeleton)

    return player


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
        screen.fill((0, 0, 0))

        update_kwargs = {
            'screen': screen,
            'dt': dt,
            'camera': camera,
            'sprites': sprites
        }

        background_group.update(**update_kwargs)
        background_group.draw(screen)

        static_objects.update(**update_kwargs)
        static_objects.draw(screen)

        game_objects.update(**update_kwargs)
        game_objects.draw(screen)

        projectile_objects.update(**update_kwargs)
        projectile_objects.draw(screen)

        for projectile in projectile_objects:
            for game_obj in game_objects:
                collide = projectile.rect.colliderect(game_obj.rect)
                if collide:
                    projectile.on_collision(game_obj)
                    game_obj.on_collision(projectile)

        hud.update(screen=screen, screen_resolution=screen_resolution, font=my_font)
        pygame.display.flip()


if __name__ == "__main__":
    main()
