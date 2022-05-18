from src.item import Item


class Potion(Item):
    cooldown = 50

    def __init__(self, owner, hp=50) -> None:
        super().__init__(owner)
        self.hp_recover = hp

    def on_use(self):
        hp_to_recover = self.owner.stats.max_hp - self.owner.hp
        self.owner.hp += min(self.hp_recover, hp_to_recover)
        return super().on_use()
