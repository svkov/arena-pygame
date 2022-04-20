class ShootCooldownMixin:

    def __init__(self, cooldown) -> None:
        self.shoot_cooldown = cooldown
        if cooldown is None:
            self.shoot_cooldown = 30
        self.shoot_cooldown_counter = 0

    def update_shoot_cooldown(self):
        if self.shoot_cooldown_counter < self.shoot_cooldown:
            self.shoot_cooldown_counter += 1

    def shooted(self):
        self.shoot_cooldown_counter = 0

    @property
    def can_shoot(self):
        return self.shoot_cooldown_counter == self.shoot_cooldown
