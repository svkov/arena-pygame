class CollisionMixin:
    def _collision(self, obj, *args, **kwargs):
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
            self._simple_collision(right_collision,
                                   left_collision,
                                   top_collision,
                                   bottom_collision,
                                   obj,
                                   *args,
                                   **kwargs)
        else:
            self._complex_collision(right_collision,
                                    left_collision,
                                    top_collision,
                                    bottom_collision,
                                    obj,
                                    *args,
                                    **kwargs)
        if right_collision or left_collision or top_collision or bottom_collision:
            obj.update_screen_coord()

    def _simple_collision(self,
                          right_collision,
                          left_collision,
                          top_collision,
                          bottom_collision,
                          obj,
                          *args,
                          **kwargs):
        if right_collision:
            self._right(obj, *args, **kwargs)
        if left_collision:
            self._left(obj, *args, **kwargs)
        if top_collision:
            self._top(obj, *args, **kwargs)
        if bottom_collision:
            self._bottom(obj, *args, **kwargs)

    def _right(self, obj, *args, **kwargs):
        raise NotImplementedError()

    def _left(self, obj, *args, **kwargs):
        raise NotImplementedError()

    def _top(self, obj, *args, **kwargs):
        raise NotImplementedError()

    def _bottom(self, obj, *args, **kwargs):
        raise NotImplementedError()

    def _complex_collision(self,
                           right_collision,
                           left_collision,
                           top_collision,
                           bottom_collision,
                           obj,
                           *args,
                           **kwargs):
        right_top_check = obj.pos_bottom - self.pos_top > self.pos_right - obj.pos_left
        right_bottom_check = self.pos_bottom - obj.pos_top > self.pos_right - obj.pos_left
        left_top_check = obj.pos_bottom - self.pos_top > obj.pos_right - self.pos_left
        left_bottom_check = self.pos_bottom - obj.pos_top > obj.pos_right - self.pos_left
        if right_collision and top_collision:
            if right_top_check:
                self._right(obj, *args, **kwargs)
            else:
                self._top(obj, *args, **kwargs)
        if right_collision and bottom_collision:
            if right_bottom_check:
                self._right(obj, *args, **kwargs)
            else:
                self._bottom(obj, *args, **kwargs)
        if left_collision and top_collision:
            if left_top_check:
                self._left(obj, *args, **kwargs)
            else:
                self._top(obj, *args, **kwargs)
        if left_collision and bottom_collision:
            if left_bottom_check:
                self._left(obj, *args, **kwargs)
            else:
                self._bottom(obj, *args, **kwargs)
