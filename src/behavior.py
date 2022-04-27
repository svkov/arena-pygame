import numpy as np

from src.actor import Actor
from src.camera import Camera

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
        self.distance_for_dest = 500
        self.attention_radius = 500

    def update(self, *args, **kwargs):
        camera: Camera = kwargs['camera']
        self.player_pos = camera.get_pos()
        self.prev_pos = self.new_pos
        self.new_pos = self.actor.pos
        self.update_attention_for_player()
        self.current_iter += 1
        if self.is_see_player:
            self.update_on_see_player(camera)
        else:
            self.update_idle()

    def update_on_see_player(self, camera):
        self.destination = self.player_pos
        self.set_actor_speed()
        self.actor.shoot(camera)

    def update_idle(self):
        self.choose_random_destination()
        self.set_actor_speed()

    def update_attention_for_player(self):
        if np.linalg.norm(self.player_pos - self.actor.pos) < self.attention_radius:
            self.is_see_player = True
        else:
            self.is_see_player = False

    def set_actor_speed(self):
        self.actor.speed = self.destination - self.actor.pos

    def choose_random_destination(self):
        close_to_destination = np.linalg.norm(self.destination - self.actor.pos) < 20
        is_stuck = self.current_iter == self.max_iter
        if close_to_destination or is_stuck:
            self.current_iter = 0
            shift = (np.random.random(size=2) - 0.5) * self.distance_for_dest
            self.destination = self.actor.pos + shift
