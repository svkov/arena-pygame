from src.game_object import GameObject
from src.game_object.actor import Actor


class StaticObject(GameObject):
    """
    This is the object which you can't go through
    """

    def __init__(self, pos, image, image_size=None, **kwargs) -> None:
        super().__init__(pos, image, image_size, **kwargs)

    def on_collision(self, obj: Actor, **kwargs):
        super().on_collision(obj)
