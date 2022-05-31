from src.item import InventoryItem


class StoneSoulItem(InventoryItem):
    name = 'Soul Stone'
    description = 'Vibrates near the portal'

    def on_use(self):
        return False

    def activate(self):
        self.kill()
