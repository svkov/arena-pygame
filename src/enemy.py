import pygame
from src.actor import Actor
from src.behavior import Behavior
from src.camera import Camera
from src.projectile import Projectile


class Enemy(Actor):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.exp_after_death = 50
        self.behavior = kwargs.get('behavior', Behavior(self))

    def shoot(self, camera: Camera):
        if self.cooldowns['shoot'].is_cooldown_over:
            self.cooldowns['shoot'].reset_counter()
            p = Projectile.shoot(self, camera.to_screen_coord(camera.get_pos()), camera, self.projectile_image,
                                 speed=self.stats.projectile_speed)
            self.groups.spawn_enemy_projectile(p)

    def update(self, *args, **kwargs) -> None:
        camera: Camera = kwargs['camera']
        screen = kwargs['screen']
        draw_enemy_attention = kwargs['draw_enemy_attention']
        self.behavior.update(*args, **kwargs)
        super().update(*args, **kwargs)
        self.draw_attention_circle(screen, camera, draw_enemy_attention)

    def draw_attention_circle(self, screen, camera, draw_enemy_attention):
        if not draw_enemy_attention:
            return
        if self.behavior.is_see_player:
            color = (255, 0, 0)
        else:
            color = (0, 255, 0)
        pygame.draw.circle(screen, color, camera.to_screen_coord(self.pos), self.behavior.attention_radius, 5)

    def on_death(self, death_from):
        super().on_death(death_from)
        death_from.owner.increase_xp(self.exp_after_death)

    def increase_xp(self):
        pass
