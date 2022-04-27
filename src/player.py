import pygame
from src.actor import Actor
from src.camera import Camera
from src.groups import GameStateGroups
from src.ingame_label import ExpLabel

from src.projectile import Projectile


class Player(Actor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.camera: Camera = kwargs['camera']
        self.exp = 0
        self.level = 1
        self.exp_to_lvlup = 100
        self._low_damage = 100
        self._high_damage = 150

    def handle_keyboard_input(self):
        self.set_zero_speed()
        keyboard = pygame.key.get_pressed()
        if keyboard[pygame.K_w]:
            self.speed[1] = -1
        if keyboard[pygame.K_s]:
            self.speed[1] = 1
        if keyboard[pygame.K_a]:
            self.speed[0] = -1
        if keyboard[pygame.K_d]:
            self.speed[0] = 1

        self.normalize_speed()

    def handle_mouse_input(self, groups: GameStateGroups):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.shoot(groups)

    def update(self, *args, **kwargs) -> None:
        screen = kwargs['screen']
        dt = kwargs['dt']
        camera: Camera = kwargs['camera']
        groups: GameStateGroups = kwargs['groups']
        self.handle_keyboard_input()
        self.handle_mouse_input(groups)
        self.update_cooldown()

        self.move_world_coord(dt)
        self.update_screen_coord(screen, camera)

    def update_screen_coord(self, screen, camera: Camera):
        self.update_camera_pos(camera)
        super().update_screen_coord(screen, camera)

    def update_camera_pos(self, camera: Camera):
        camera.x = self.pos[0]
        camera.y = self.pos[1]

    def shoot(self, groups: GameStateGroups):
        p = Projectile.shoot(self, pygame.mouse.get_pos(), self.camera, self.projectile_image,
                             speed=self.stats.projectile_speed)
        groups.spawn_player_projectile(p)
        self.shooted()

    def increase_xp(self, new_exp):
        exp = self.stats.exp_gain(new_exp)
        self.exp += exp
        self.make_exp_label(exp)
        self.lvlup_if_needed()

    def make_exp_label(self, exp):
        exp_label = ExpLabel(f'+{int(exp)} XP', self.pos, self.camera)
        self.groups.spawn_ui(exp_label)

    def lvlup_if_needed(self):
        if self.exp >= self.exp_to_lvlup:
            # if exp is enough to lvlup multiple times
            self.level += self.exp // self.exp_to_lvlup
            self.exp = self.exp % self.exp_to_lvlup
