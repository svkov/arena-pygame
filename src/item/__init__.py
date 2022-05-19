from src.game_object import GameObject


class InventoryItem(GameObject):

    def __init__(self, pos, image, image_size, owner, **kwargs) -> None:
        super().__init__(pos, image, image_size, **kwargs)
        self.owner = owner

    def update(self, *args, **kwargs):
        if self.owner is None:
            return super().update(*args, **kwargs)
        self.rect.x = int(self.pos[0])
        self.rect.y = int(self.pos[1])

    def on_use(self):
        pass

    def on_collision(self, obj):
        return super().on_collision(obj)

    def on_pickup(self, owner):
        self.owner = owner
