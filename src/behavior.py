import numpy as np

from src.actor import Actor

class Behavior:

    def __init__(self, actor: Actor) -> None:
        self.actor = actor
        self.is_see_player = False
        self.player_pos = False
        self.destination = self.actor.pos
        self.prev_pos = self.actor.pos
        self.new_pos = self.actor.pos
        self.max_iter = 50
        self.current_iter = 0

    def update(self, *args, **kwargs):
        self.prev_pos = self.new_pos
        self.new_pos = self.actor.pos
        self.current_iter += 1
        if self.is_see_player:
            self.update_on_see_player()
        else:
            self.update_idle()

    def update_on_see_player(self):
        pass

    def update_idle(self):
        self.choose_destination()
        self.actor.speed = self.destination - self.actor.pos

    def choose_destination(self):
        close_to_destination = np.linalg.norm(self.destination - self.actor.pos) < 20
        is_stuck = self.current_iter == self.max_iter
        if close_to_destination or is_stuck:
            self.current_iter = 0
            shift = (np.random.random(size=2) - 0.5) * 500
            self.destination = self.actor.pos + shift
            print('new destination', self.destination)
