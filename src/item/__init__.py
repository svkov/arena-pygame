from src.game_object import GameObject


class InventoryItem(GameObject):

    def __init__(self, pos, image, image_size, owner, **kwargs) -> None:
        super().__init__(pos, image, image_size, **kwargs)
        self.owner = owner

    def on_use(self):
        pass

    def on_collision(self, obj):
        return super().on_collision(obj)
