from pygame.sprite import Group

from src.collision_handler import CollisionHandler

class GameStateGroups:
    def __init__(self) -> None:
        self.static_objects = Group()
        self.background_group = Group()
        self.items_on_floor = Group()

        self.player_projectiles = Group()
        self.player_objects = Group()

        self.enemy_projectiles = Group()
        self.enemy_objects = Group()

        self.ui_objects = Group()
        self.items_in_inventory = Group()
        self.update_groups_order = [
            self.background_group,
            self.static_objects,
            self.items_on_floor,
            self.player_objects,
            self.player_projectiles,
            self.enemy_objects,
            self.enemy_projectiles,
            self.ui_objects,
            self.items_in_inventory
        ]
        self.draw_groups_order = [
            self.static_objects,
            self.items_on_floor,
            self.player_objects,
            self.player_projectiles,
            self.enemy_objects,
            self.enemy_projectiles,
            self.ui_objects,
            self.items_in_inventory
        ]

    def update(self, update_kwargs):
        for group in self.update_groups_order:
            group.update(**update_kwargs)

    def draw(self, screen):
        for group in self.draw_groups_order:
            group.draw(screen)

    def handle_collisions(self, update_kwargs):
        CollisionHandler.full_collision(self.player_objects, self.enemy_projectiles, self.static_objects, update_kwargs)
        CollisionHandler.full_collision(self.enemy_objects, self.player_projectiles, self.static_objects, update_kwargs)
        CollisionHandler.player_collision_to_items(self.player_objects, self.items_on_floor)

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

    def spawn_ui(self, obj):
        self.ui_objects.add(obj)

    def spawn_item(self, obj):
        self.items_on_floor.add(obj)
