from src.actor import Actor
from src.game_object import GameObject


class StaticObject(GameObject):
    """
    This is the object which you can't go through
    """

    def __init__(self, pos, image, image_size=None) -> None:
        super().__init__(pos, image, image_size)

    def on_collision(self, obj: Actor):
        if obj.rect.left < self.rect.right and obj.speed[0] > 0:
            obj.rect.right = self.rect.left
        if obj.rect.right > self.rect.left and obj.speed[0] < 0:
            obj.rect.left = self.rect.right
        if obj.rect.top < self.rect.bottom and obj.speed[1] > 0:
            obj.rect.bottom = self.rect.top
        if obj.rect.bottom > self.rect.top and obj.speed[1] < 0:
            obj.rect.top = self.rect.bottom
