from enum import Enum


class EnemyStates(Enum):
    IDLE = 0
    WALK = 1
    ATTACK = 2


class PlayerStates(Enum):
    IDLE = 0
    WALK = 1
    ATTACK = 2
    BACK = 3
    LVLUP = 4
