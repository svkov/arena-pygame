from src.item import InventoryItem


class Potion(InventoryItem):
    cooldown = 50
    name = 'HP Potion'
    description = "Drink this potion to recover some HP"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.hp_recover = kwargs.get('hp', 30)

    def on_use(self):
        """
        Return True if need to be removed from inventory
        """
        hp_to_recover = self.owner.stats.max_hp - self.owner.hp
        if hp_to_recover > 0:
            self.owner.hp += min(self.hp_recover, hp_to_recover)
            super().on_use()
            self.kill()
            return True
        else:
            return False
