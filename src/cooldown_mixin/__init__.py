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

class DamageRecieveMixin(CooldownMixin):
    def __init__(self, cooldown=None) -> None:
        super().__init__(cooldown)

    @property
    def can_recieve_damage(self):
        return self.is_cooldown_over

class ShootCooldownMixin(CooldownMixin):

    def __init__(self, cooldown=None) -> None:
        super().__init__(cooldown)

    @property
    def can_shoot(self):
        return self.is_cooldown_over

class HPPotionCooldownMixin(CooldownMixin):
    def __init__(self, cooldown=None) -> None:
        super().__init__(cooldown)

    @property
    def can_drink_hp_potion(self):
        return self.is_cooldown_over
