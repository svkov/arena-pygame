import numpy as np


class ActorStats:

    def __init__(self, base_hp, base_atk, strength, intelligence, agility, defense, speed, **kwargs) -> None:
        self.base_hp = base_hp
        self.base_atk = base_atk
        # bonus HP and attack power
        self.strength = strength
        # mana pool and bonus exp from enemies
        self.intelligence = intelligence
        # attack speed
        self.agility = agility
        # damage reduction
        self.defense = defense
        # movement speed
        self.speed = speed

    @property
    def damage(self):
        return self.base_atk + self.strength

    @property
    def max_hp(self):
        return self.base_hp + self.strength * 25

    def damage_take(self, raw_damage) -> float:
        return raw_damage - self.defense

    def exp_gain(self, raw_exp) -> float:
        return raw_exp * (1 + self.intelligence / 100)

    @property
    def attack_speed(self):
        # values get by wolfram exponential fit
        # 1 agi = 1.5s / attack
        # 10 - 1s
        # 20 - 0.7
        # 30 - 0.5
        # 100 - 0.04 (~once per frame if 30 fps)
        return 1.54 * np.exp(-0.035 * self.agility)

    @property
    def attack_speed_in_frames(self):
        return int(1 / self.attack_speed)
