import pygame
from src.animated_enemy import AnimatedEnemy
from src.camera import Camera
from src.container import Container
from src.enemy import Enemy
from src.hud import HUD
from src.utils import spawn_object
from src.global_objects import game_objects, projectile_objects
from src.player import Player

running = True


def setup_scene(camera):

    player = Player((0, 0), 'assets/knight.png', max_hp=100, hp=100, camera=camera)
    spawn_object(player)

    skeleton = Enemy((300, 300), 'assets/skeleton.png', max_hp=100, hp=100)
    spawn_object(skeleton)

    skeleton = Enemy((500, 300), 'assets/skeleton.png', max_hp=100, hp=100)
    spawn_object(skeleton)

    chest = Container((500, 500), 'assets/chest.png', max_hp=100, hp=50)
    spawn_object(chest)

    anim_skeleton = AnimatedEnemy(
        (600, 600), 'assets/skeleton_walk.png', max_hp=100, hp=100, image_size=(1536, 512))
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

    clock = pygame.time.Clock()
    screen_resolution = (1920, 1080)
    screen = pygame.display.set_mode(screen_resolution)
    camera = Camera(0, 0, screen_resolution)
    player = setup_scene(camera)
    hud = HUD(player)

    while running:
        dt = clock.tick(30)
        handle_input_keyboard()
        screen.fill((0, 0, 0))

        game_objects.update(screen=screen, dt=dt, camera=camera)
        game_objects.draw(screen)

        projectile_objects.update(dt=dt, camera=camera)
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
