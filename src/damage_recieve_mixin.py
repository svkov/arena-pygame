class DamageRecieveMixin:

    def __init__(self, cooldown) -> None:
        self.damage_recieve_cooldown = cooldown
        if self.damage_recieve_cooldown is None:
            self.damage_recieve_cooldown = 1
        self.damage_recieve_counter = 0

    def update_damage_cooldown(self):
        if self.damage_recieve_counter < self.damage_recieve_cooldown:
            self.damage_recieve_counter += 1

    def damaged(self):
        self.damage_recieve_counter = 0

    @property
    def can_recieve_damage(self):
        return self.damage_recieve_counter == self.damage_recieve_cooldown
