from src.item import InventoryItem
from src.item.item_rare import ItemRare


class StoneSoulItem(InventoryItem):
    name = 'Soul Stone'
    description = 'Vibrates near the portal'
    item_rare = ItemRare.LEGENDARY

    def on_use(self):
        return False

    def activate(self):
        self.kill()
