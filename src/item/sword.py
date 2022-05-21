from src.item import InventoryItem


class SwordItem(InventoryItem):
    description = "This sword looks powerful"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.stats = kwargs.get('stats', None)

    def on_use(self):
        super().on_use()
        self.owner.weapon = self
        return False

class ItemStats:
    def __init__(self, **stats) -> None:
        self._stats = stats
