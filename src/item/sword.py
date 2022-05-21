from src.item import InventoryItem


class SwordItem(InventoryItem):
    description = "This sword looks powerful"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.stats = kwargs.get('stats', ItemStats(damage=10))

    def on_use(self):
        super().on_use()
        if self.is_using_now:
            self.unwield()
        else:
            self.wield()
        return False

    def wield(self):
        if self.owner.weapon is not None:
            self.owner.weapon.unwield()
        self.owner.weapon = self
        self.is_using_now = True

    def unwield(self):
        self.owner.weapon = None
        self.is_using_now = False

class ItemStats:
    def __init__(self, **stats) -> None:
        self._stats = stats

    @property
    def damage(self):
        return self._stats['damage']
