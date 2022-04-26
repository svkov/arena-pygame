from pygame.sprite import Group

from src.collision_handler import CollisionHandler

class GameStateGroups:
    def __init__(self) -> None:
        self.static_objects = Group()
        self.background_group = Group()

        self.player_projectiles = Group()
        self.player_objects = Group()

        self.enemy_projectiles = Group()
        self.enemy_objects = Group()

    def update(self, update_kwargs):
        self.background_group.update(**update_kwargs)
        self.static_objects.update(**update_kwargs)
        self.player_objects.update(**update_kwargs)
        self.player_projectiles.update(**update_kwargs)
        self.enemy_objects.update(**update_kwargs)
        self.enemy_projectiles.update(**update_kwargs)

    def draw(self, screen):
        self.static_objects.draw(screen)
        self.player_objects.draw(screen)
        self.player_projectiles.draw(screen)
        self.enemy_objects.draw(screen)
        self.enemy_projectiles.draw(screen)

    def handle_collisions(self, update_kwargs):
        CollisionHandler.full_collision(self.player_objects, self.enemy_projectiles, self.static_objects, update_kwargs)
        CollisionHandler.full_collision(self.enemy_objects, self.player_projectiles, self.static_objects, update_kwargs)

    def spawn_enemy_projectile(self, obj):
        self.enemy_projectiles.add(obj)

    def spawn_enemy_object(self, obj):
        self.enemy_objects.add(obj)

    def spawn_static_object(self, obj):
        self.static_objects.add(obj)

    def spawn_background(self, obj):
        self.background_group.add(obj)

    def spawn_player_obj(self, obj):
        self.player_objects.add(obj)

    def spawn_player_projectile(self, obj):
        self.player_projectiles.add(obj)
