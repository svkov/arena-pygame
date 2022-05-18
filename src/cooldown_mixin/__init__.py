class CooldownMixin:

    def __init__(self, cooldown=None) -> None:
        self.cooldown = cooldown
        if self.cooldown is None:
            self.cooldown = 1
        self.counter = 0

    def update_cooldown(self):
        if self.counter < self.cooldown:
            self.counter += 1

    def reset_counter(self):
        self.counter = 0

    @property
    def is_cooldown_over(self):
        return self.counter == self.cooldown
