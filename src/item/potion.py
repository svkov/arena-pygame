from src.item import InventoryItem


class Potion(InventoryItem):
    cooldown = 50
    description = "Drink this potion to recover some HP"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.hp_recover = kwargs.get('hp', 30)

    def on_use(self):
        hp_to_recover = self.owner.stats.max_hp - self.owner.hp
        self.owner.hp += min(self.hp_recover, hp_to_recover)
        return super().on_use()
