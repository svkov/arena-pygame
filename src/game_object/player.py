import pygame
from src.animation import AnimationManager
from src.animation.states import PlayerStates
from src.core.input_handler import InputHandler
from src.game_object.actor import Actor
from src.game_object.projectile import Projectile
from src.hud.label_manager import LabelManager
from src.item import InventoryItem

class Player(Actor):

    def __init__(self,
                 *args,
                 level=1,
                 exp_to_lvlup=100,
                 animation_states=None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.exp = 0
        self.level = level
        self.exp_to_lvlup = exp_to_lvlup
        self.animation_manager = AnimationManager(animation_states, default_state=PlayerStates.IDLE)
        self.animation_manager.set_state(PlayerStates.IDLE)
        self.image = self.animation_manager.image
        self.input_handler = InputHandler(self)
        self.label_manager = LabelManager(self, self.groups, self.camera)
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

    def update(self, *args, **kwargs) -> None:
        self.show_items = kwargs.get('show_items', False)
        events = kwargs.get('events', [])
        self.input_handler.handle_input(events)
        super().update(*args, **kwargs)

    def update_animation_if_needed(self):
        if super().update_animation_if_needed():
            return True
        self.set_animation_state()
        self.animation_manager.update()
        self.image = self.animation_manager.image

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

    def go_to_portal(self):
        self.is_in_portal = True

    def set_animation_state(self):
        if self.is_moving:
            if self.speed[1] < 0:
                self.animation_manager.set_state(PlayerStates.BACK)
            else:
                self.animation_manager.set_state(PlayerStates.WALK)
        if not self.animation_manager.is_busy:
            self.animation_manager.set_state(PlayerStates.IDLE)

    def update_screen_coord(self):
        self.camera.set_pos(self.pos)
        super().update_screen_coord()

    def shoot(self):
        mouse_pos = pygame.mouse.get_pos()
        p = Projectile.shoot(self, mouse_pos, self.camera, self.projectile_image,
                             speed=self.stats.projectile_speed, config=self.game_config,
                             image_size=(64, 64))
        self.groups.spawn_player_projectile(p)
        self.cooldowns['shoot'].reset_counter()
        self.set_attack_animation_state(mouse_pos)

    def set_attack_animation_state(self, mouse_pos):
        if mouse_pos[1] > self.center_screen[1]:
            self.animation_manager.set_state(PlayerStates.ATTACK, force=True)
        else:
            self.animation_manager.set_state(PlayerStates.BACK, force=True)

    def increase_xp(self, new_exp):
        exp = self.stats.exp_gain(new_exp)
        self.exp += exp
        self.label_manager.spawn_exp_label(exp)
        self.lvlup_if_needed()

    def lvlup_if_needed(self):
        if self.exp >= self.exp_to_lvlup:
            # if exp is enough to lvlup multiple times
            levels_up = int(self.exp // self.exp_to_lvlup)
            self.level += levels_up
            self.level_up(levels_up)
            self.exp = self.exp % self.exp_to_lvlup
            self.label_manager.spawn_level_up_label()
            self.exp_to_lvlup += levels_up * 100

    def collide_with_item(self, item: InventoryItem):
        self.hud.info_description = item.description
        if self.is_interacting and self.inventory.is_enough_space():
            item.on_pickup(self)
            self.groups.items_on_floor.remove(item)
            self.groups.items_in_inventory.add(item)
            self.inventory.add(item)
