from src.actor import Actor
from src.game_object import GameObject


class StaticObject(GameObject):
    """
    This is the object which you can't go through
    """

    def __init__(self, pos, image, image_size=None) -> None:
        super().__init__(pos, image, image_size)

    def on_collision(self, obj: Actor, dt):
        self._collision(obj, dt)

    def _collision(self, obj: Actor, dt):
        right_collision = obj.pos_left < self.pos_right and obj.speed[0] > 0
        left_collision = obj.pos_right > self.pos_left and obj.speed[0] < 0
        top_collision = obj.pos_top < self.pos_bottom and obj.speed[1] > 0
        bottom_collision = obj.pos_bottom > self.pos_top and obj.speed[1] < 0
        if right_collision or left_collision:
            obj.pos[0] = obj.pos[0] - obj.speed[0] * dt
        if top_collision or bottom_collision:
            obj.pos[1] = obj.pos[1] - obj.speed[1] * dt
