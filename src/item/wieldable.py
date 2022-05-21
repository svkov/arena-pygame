from src.item import InventoryItem

class ItemStats:
    def __init__(self, **stats) -> None:
        self._stats = stats

    @property
    def damage(self):
        return self._stats.get('damage', 0)

    @property
    def defense(self):
        return self._stats.get('defense', 0)

class WieldableItem(InventoryItem):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.stats = kwargs.get('stats', ItemStats())

    def on_use(self):
        super().on_use()
        if self.is_using_now:
            self.unwield()
        else:
            self.wield()
        return False

    def wield(self):
        if self.get_owner_wield_slot() is not None:
            self.get_owner_wield_slot().unwield()
        self.set_owner_wield_slot(self)
        self.is_using_now = True

    def unwield(self):
        self.set_owner_wield_slot(None)
        self.is_using_now = False

    def get_owner_wield_slot(self):
        pass

    def set_owner_wield_slot(self, val):
        pass
