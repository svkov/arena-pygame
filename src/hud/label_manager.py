from __future__ import annotations
from typing import TYPE_CHECKING
from src.hud.ingame_label import ExpLabel, ItemLabel, LevelUpLabel

if TYPE_CHECKING:
    from src.core.groups import GameStateGroups
    from src.game_object.player import Player
    from src.core.camera import Camera

class LabelManager:

    def __init__(self,
                 player: Player,
                 groups: GameStateGroups,
                 camera: Camera) -> None:
        self.player = player
        self.groups = groups
        self.camera = camera

    def spawn_item_label(self, item, mouse_pos):
        exp_label = ItemLabel(item.description, mouse_pos, self.camera)
        self.groups.items_description.add(exp_label)

    def spawn_level_up_label(self):
        lvlup_label = LevelUpLabel(self.player.pos, self.camera, self.player.game_config)
        self.groups.spawn_ui(lvlup_label)

    def spawn_exp_label(self, exp):
        exp_label = ExpLabel(f'+{int(exp)} XP', self.player.pos, self.camera)
        self.groups.spawn_ui(exp_label)
