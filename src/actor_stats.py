import numpy as np


class ActorStats:

    def __init__(self, base_hp, base_atk, strength, intelligence, agility, defense, speed, **kwargs) -> None:
        self.base_hp = max(base_hp, 1)
        self.base_atk = max(base_atk, 0)
        # bonus HP and attack power
        self.strength = np.clip(strength, 0, 100)
        # mana pool and bonus exp from enemies
        self.intelligence = np.clip(intelligence, 0, 100)
        # attack speed
        self.agility = np.clip(agility, 1, 100)
        # damage reduction
        self.defense = np.clip(defense, 0, 100)
        # movement speed
        self.speed = np.clip(speed, 1, 100)

    @property
    def damage(self):
        return self.base_atk + self.strength

    @property
    def max_hp(self):
        return max(self.base_hp + self.strength * 25, 1)

    def damage_take(self, raw_damage, equipment_defence=0) -> float:
        return max(raw_damage - (self.defense + equipment_defence), 1)

    def exp_gain(self, raw_exp) -> float:
        return raw_exp * (1 + self.intelligence / 100)

    @property
    def attack_speed(self):
        # values get by wolfram exponential fit
        # 1 agi = 1.5 attack/s
        # 10 - 1 attack/s
        # 20 - 0.7 attack/s
        # 30 - 0.5 attack/s
        # 100 - 0.04 (~once per frame if 30 fps)
        return 1.54 * np.exp(-0.035 * self.agility)

    def attack_speed_in_frames(self, fps):
        return max(1, int(self.attack_speed * fps))

    @property
    def movement_speed(self):
        return self.speed * 0.05

    @property
    def projectile_speed(self):
        return self.speed * 0.1


class EnemyStats(ActorStats):

    @property
    def movement_speed(self):
        return super().movement_speed
