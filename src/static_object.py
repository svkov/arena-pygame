from src.actor import Actor
from src.game_object import GameObject


class StaticObject(GameObject):
    """
    This is the object which you can't go through
    """

    def __init__(self, pos, image, image_size=None, **kwargs) -> None:
        super().__init__(pos, image, image_size, **kwargs)

    def on_collision(self, obj: Actor, **kwargs):
        dt = kwargs['dt']
        camera = kwargs['camera']
        screen = kwargs['screen']
        self._collision(obj, dt, screen, camera)

    def _collision(self, obj: Actor, dt, screen, camera):
        obj.pos_right - self.pos_left
        right_collision = obj.pos_left < self.pos_right and obj.pos_left > self.pos_left \
            and obj.pos_right > self.pos_right
        left_collision = obj.pos_right > self.pos_left and obj.pos_right < self.pos_right \
            and obj.pos_left < self.pos_left
        top_collision = obj.pos_bottom > self.pos_top and obj.pos_bottom < self.pos_bottom \
            and obj.pos_top < self.pos_top
        bottom_collision = obj.pos_top < self.pos_bottom and obj.pos_top > self.pos_top \
            and obj.pos_bottom > self.pos_bottom
        if sum([right_collision, left_collision, top_collision, bottom_collision]) == 1:
            self._simple_collision(right_collision, left_collision, top_collision, bottom_collision, obj)
        else:
            self._complex_collision(right_collision, left_collision, top_collision, bottom_collision, obj)
        if right_collision or left_collision or top_collision or bottom_collision:
            obj.update_screen_coord()

    def _simple_collision(self, right_collision, left_collision, top_collision, bottom_collision, obj: Actor):
        if right_collision:
            self._right(obj)
        if left_collision:
            self._left(obj)
        if top_collision:
            self._top(obj)
        if bottom_collision:
            self._bottom(obj)

    def _right(self, obj):
        obj.pos_left = self.pos_right

    def _left(self, obj):
        obj.pos_right = self.pos_left

    def _top(self, obj):
        obj.pos_bottom = self.pos_top

    def _bottom(self, obj):
        obj.pos_top = self.pos_bottom

    def _complex_collision(self, right_collision, left_collision, top_collision, bottom_collision, obj: Actor):
        right_top_check = obj.pos_bottom - self.pos_top > self.pos_right - obj.pos_left
        right_bottom_check = self.pos_bottom - obj.pos_top > self.pos_right - obj.pos_left
        left_top_check = obj.pos_bottom - self.pos_top > obj.pos_right - self.pos_left
        left_bottom_check = self.pos_bottom - obj.pos_top > obj.pos_right - self.pos_left
        if right_collision and top_collision:
            if right_top_check:
                self._right(obj)
            else:
                self._top(obj)
        if right_collision and bottom_collision:
            if right_bottom_check:
                self._right(obj)
            else:
                self._bottom(obj)
        if left_collision and top_collision:
            if left_top_check:
                self._left(obj)
            else:
                self._top(obj)
        if left_collision and bottom_collision:
            if left_bottom_check:
                self._left(obj)
            else:
                self._bottom(obj)
