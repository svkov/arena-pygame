import pygame
from src.animation import AnimationManager
from src.animation.states import PlayerStates
from src.camera import Camera
from src.game_object.actor import Actor
from src.game_object.projectile import Projectile
from src.groups import GameStateGroups
from src.ingame_label import ExpLabel, ItemLabel, LevelUpLabel
from src.item import InventoryItem

class Player(Actor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.camera: Camera = kwargs['camera']
        self.exp = 0
        self.level = kwargs.get('level', 1)
        self.exp_to_lvlup = kwargs.get('exp_tp_lvlup', 100)
        self.animation_manager = AnimationManager(kwargs['animation_states'], default_state=PlayerStates.IDLE)
        self.animation_manager.set_state(PlayerStates.IDLE)
        self.image = self.animation_manager.image
        self.is_interacting = False
        self.is_in_portal = False
        # TODO: connect to HUD more obviously
        # You must specify HUD after creating the player
        self.hud = None

    @classmethod
    def recreate_player(cls, old_player, new_player):
        new_player.inventory = old_player.inventory
        new_player.inventory.set_new_owner(new_player)
        new_player.weapon = old_player.weapon
        new_player.armor = old_player.armor
        new_player.hp = old_player.hp
        new_player.stats = old_player.stats
        new_player.exp = old_player.exp
        new_player.exp_to_lvlup = old_player.exp_to_lvlup
        new_player.level = old_player.level
        new_player.kills = old_player.kills
        return new_player

    def handle_keyboard_input(self, keyboard):
        self.set_zero_speed()
        if keyboard[pygame.K_w]:
            self.speed[1] = -1
        if keyboard[pygame.K_s]:
            self.speed[1] = 1
        if keyboard[pygame.K_a]:
            self.speed[0] = -1
            self.is_going_left = True
        if keyboard[pygame.K_d]:
            self.speed[0] = 1
        self.normalize_speed()

    def handle_mouse_input(self, groups: GameStateGroups):
        if pygame.mouse.get_pressed()[0] and self.cooldowns['shoot'].is_cooldown_over:
            self.shoot(groups)
        if pygame.mouse.get_pressed()[2] and self.cooldowns['hp_potion'].is_cooldown_over:
            self.cooldowns['hp_potion'].reset_counter()

        mouse_pos = pygame.mouse.get_pos()
        inventory_item = self.find_inventory_item_collision(mouse_pos)
        if inventory_item is not None:
            self.spawn_item_description(inventory_item, mouse_pos)

    def handle_events(self, events):
        self.is_interacting = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    inventory_item = self.find_inventory_item_collision(mouse_pos)
                    if inventory_item is not None:
                        self.use_inventory_item(inventory_item)
                if event.button == 3:
                    mouse_pos = pygame.mouse.get_pos()
                    inventory_item = self.find_inventory_item_collision(mouse_pos)
                    if inventory_item is not None:
                        self.drop_item(inventory_item)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_f:
                    self.is_interacting = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.camera.zoom_out()
                elif event.button == 5:
                    self.camera.zoom_in()

    def use_inventory_item(self, item):
        must_delete = item.on_use()
        if must_delete:
            self.inventory.remove(item)

    def use_quest_item(self, item):
        item.activate()
        self.inventory.remove(item)

    def find_inventory_item_collision(self, pos):
        for inventory_item in self.groups.items_in_inventory:
            if inventory_item.rect.collidepoint(pos):
                return inventory_item

    def update(self, *args, **kwargs) -> None:
        dt = kwargs['dt']
        groups: GameStateGroups = kwargs['groups']
        events = kwargs['events']
        keyboard = pygame.key.get_pressed()
        self.handle_events(events)
        self.handle_keyboard_input(keyboard)
        self.handle_mouse_input(groups)
        self.handle_animation()
        self.update_cooldown()

        self.update_collision(dt)
        self.move_world_coord(dt)
        self.update_zoom()
        self.update_screen_coord()

        self.animation_manager.update()
        self.image = self.animation_manager.image
        self.flip_image_if_needed()

    def go_to_portal(self):
        self.is_in_portal = True

    def handle_animation(self):
        if not self.animation_manager.is_busy:
            if self.speed[1] < 0:
                self.animation_manager.set_state(PlayerStates.BACK)
            else:
                self.animation_manager.set_state(PlayerStates.IDLE)

    def update_screen_coord(self):
        self.update_camera_pos(self.camera)
        super().update_screen_coord()

    def update_camera_pos(self, camera: Camera):
        camera.x = self.pos[0]
        camera.y = self.pos[1]

    def shoot(self, groups: GameStateGroups):
        p = Projectile.shoot(self, pygame.mouse.get_pos(), self.camera, self.projectile_image,
                             speed=self.stats.projectile_speed, config=self.game_config)
        groups.spawn_player_projectile(p)
        self.cooldowns['shoot'].reset_counter()
        self.animation_manager.set_state(PlayerStates.ATTACK)

    def increase_xp(self, new_exp):
        exp = self.stats.exp_gain(new_exp)
        self.exp += exp
        self.make_exp_label(exp)
        self.lvlup_if_needed()

    def make_exp_label(self, exp):
        exp_label = ExpLabel(f'+{int(exp)} XP', self.pos, self.camera)
        self.groups.spawn_ui(exp_label)

    def make_lvlup_label(self):
        lvlup_label = LevelUpLabel(self.pos, self.camera, self.game_config)
        self.groups.spawn_ui(lvlup_label)

    def spawn_item_description(self, item, mouse_pos):
        exp_label = ItemLabel(item.description, mouse_pos, self.camera)
        self.groups.items_description.add(exp_label)

    def lvlup_if_needed(self):
        if self.exp >= self.exp_to_lvlup:
            # if exp is enough to lvlup multiple times
            levels_up = int(self.exp // self.exp_to_lvlup)
            self.level += levels_up
            hp_percent_before = self.hp / self.max_hp
            [self.stats.on_level_up() for _ in range(levels_up)]
            self.hp = self.max_hp * hp_percent_before
            self.exp = self.exp % self.exp_to_lvlup
            self.make_lvlup_label()
            self.exp_to_lvlup += levels_up * 100

    def collide_with_item(self, item: InventoryItem):
        if self.hud is None:
            pass
        self.hud.info_description = item.description
        if self.is_interacting and self.inventory.is_enough_space():
            item.on_pickup(self)
            self.groups.items_on_floor.remove(item)
            self.groups.items_in_inventory.add(item)
            self.inventory.add(item)