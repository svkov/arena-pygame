from src.item.wieldable import ItemStats, WieldableItem


class SwordItem(WieldableItem):
    name = 'Sword'
    description = "This sword looks powerful"

    def __init__(self, *args, **kwargs) -> None:
        stats = kwargs.get('stats', ItemStats(damage=10))
        kwargs['stats'] = stats
        super().__init__(*args, **kwargs)

    def get_owner_wield_slot(self):
        return self.owner.weapon

    def set_owner_wield_slot(self, val):
        self.owner.weapon = val

class ArmorItem(WieldableItem):
    name = 'Armor'
    description = "Looks like it can protect you"

    def __init__(self, *args, **kwargs) -> None:
        stats = kwargs.get('stats', ItemStats(defense=10))
        kwargs['stats'] = stats
        super().__init__(*args, **kwargs)

    def get_owner_wield_slot(self):
        return self.owner.armor

    def set_owner_wield_slot(self, val):
        self.owner.armor = val
