from src.item import InventoryItem


class SwordItem(InventoryItem):
    description = "This sword looks powerful"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.stats = kwargs.get('stats', ItemStats(damage=10))

    def on_use(self):
        super().on_use()
        self.owner.weapon = self
        self.is_using_now = True
        return False

class ItemStats:
    def __init__(self, **stats) -> None:
        self._stats = stats

    @property
    def damage(self):
        return self._stats['damage']
