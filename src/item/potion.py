from src.hud.ingame_label import DamageLabel
from src.item import InventoryItem
from src.item.item_rare import ItemRare


class Potion(InventoryItem):
    cooldown = 50
    name = 'HP Potion'
    description = "Drink this potion to recover some HP"
    item_rare = ItemRare.COMMON

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.hp_recover = kwargs.get('hp', 30)

    def on_use(self):
        """
        Return True if need to be removed from inventory
        """
        hp_to_recover = self.owner.stats.max_hp - self.owner.hp
        if hp_to_recover > 0:
            self.make_heal_label(hp_to_recover)
            self.owner.hp += min(self.hp_recover, hp_to_recover)
            super().on_use()
            self.kill()
            return True
        else:
            return False

    def make_heal_label(self, hp_recover):
        label_content = f'+{int(hp_recover)}'
        label = DamageLabel(label_content, self.owner.pos, self.camera, (0, 255, 0))
        self.groups.ui_objects.add(label)
