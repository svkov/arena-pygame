import pygame
from src.behavior import Behavior
from src.game_object.actor import Actor
from src.game_object.projectile import Projectile


class Enemy(Actor):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.exp_after_death = 50
        self.behavior = kwargs.get('behavior', Behavior(self))

    def shoot(self):
        if self.cooldowns['shoot'].is_cooldown_over:
            self.cooldowns['shoot'].reset_counter()
            camera_screen_pos = self.camera.to_screen_coord(self.camera.get_pos())
            p = Projectile.shoot(self,
                                 camera_screen_pos,
                                 self.camera,
                                 self.projectile_image,
                                 speed=self.stats.projectile_speed,
                                 config=self.game_config)
            self.groups.spawn_enemy_projectile(p)

    def update(self, *args, **kwargs) -> None:
        screen: pygame.surface.Surface = kwargs['screen']
        if self.is_alive:
            self.behavior.update(*args, **kwargs)
        else:
            self.speed = self.speed * 0
        super().update(*args, **kwargs)
        self.draw_attention_circle(screen)

    def draw_attention_circle(self, screen: pygame.surface.Surface):
        if not self.game_config.draw_enemy_attention:
            return
        if self.behavior.is_see_player:
            color = (255, 0, 0)
        else:
            color = (0, 255, 0)
        pygame.draw.circle(screen, color, self.camera.to_screen_coord(self.pos), self.behavior.attention_radius, 5)

    def on_death(self, death_from: Projectile):
        super().on_death(death_from)
        death_from.owner.increase_xp(self.exp_after_death)
        self.drop_all_items()

    def increase_xp(self):
        pass

    def drop_all_items(self):
        for item in self.inventory.as_list():
            self.drop_item(item)
