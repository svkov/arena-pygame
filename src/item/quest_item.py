from src.item import InventoryItem


class StoneSoulItem(InventoryItem):
    description = 'Vibrates near the portal'

    def on_use(self):
        # Delete on use
        self.kill()
        return True
