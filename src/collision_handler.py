import pygame
from pygame.sprite import Group

class CollisionHandler:

    @staticmethod
    def full_collision(obj_group: Group, projectile_group: Group, static_group: Group, update_kwargs):
        CollisionHandler.collide_group_to_static(obj_group, static_group, update_kwargs)
        CollisionHandler.collide_projectiles_to_static(projectile_group, static_group)
        CollisionHandler.find_collision(obj_group, projectile_group)

    @staticmethod
    def find_collision(obj_group: Group, projectile_group: Group):
        for obj in obj_group:
            collided_objects = pygame.sprite.spritecollide(obj, projectile_group, False)
            for collided in collided_objects:
                CollisionHandler.collide_two_sprites_mask(obj, collided)

    @staticmethod
    def collide_group_to_static(obj_group: Group, static_group: Group, kwargs):
        for game_obj in obj_group:
            collided_objects = pygame.sprite.spritecollide(game_obj, static_group, False)
            for collided in collided_objects:
                CollisionHandler.collide_two_sprites_mask(game_obj, collided, kwargs)

    @staticmethod
    def collide_two_sprites_mask(game_obj, static_obj, kwargs=None):
        if kwargs is None:
            kwargs = {}
        col_point = pygame.sprite.collide_mask(game_obj, static_obj)
        if col_point:
            static_obj.on_collision(game_obj, **kwargs)
            game_obj.on_collision(static_obj)

    @staticmethod
    def collide_projectiles_to_static(projectile_group: Group, static_group: Group):
        for static in static_group:
            collided = pygame.sprite.spritecollide(static, projectile_group, False)
            for collided_obj in collided:
                CollisionHandler.collide_two_sprites_mask(static, collided_obj)

    @staticmethod
    def player_collision_to_items(player_group: Group, items_group: Group):
        for player in player_group:
            collided_objects = pygame.sprite.spritecollide(player, items_group, False)
            if collided_objects:
                item = collided_objects[0]
                player.collide_with_item(item)

    @staticmethod
    def player_collision_to_interactive_objects(player_group: Group, interactive_group: Group):
        for player in player_group:
            if not player.is_interacting:
                continue
            collided_objects = pygame.sprite.spritecollide(player, interactive_group, False)
            if collided_objects:
                obj = collided_objects[0]
                obj.on_interact(player)
