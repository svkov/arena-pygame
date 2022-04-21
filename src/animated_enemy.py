from enum import Enum
from src.animation import AnimationManager
from src.camera import Camera
from src.enemy import Enemy


class EnemyStates(Enum):
    IDLE = 0
    WALK = 1
    ATTACK = 2

class AnimatedEnemy(Enemy):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.animation_manager = AnimationManager(kwargs['animation_states'])
        self.animation_manager.set_state(EnemyStates.WALK)
        self.image = self.animation_manager.image

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)
        self.animation_manager.update()
        self.image = self.animation_manager.image

    def shoot(self, camera: Camera):
        if self.can_shoot:
            self.animation_manager.set_state(EnemyStates.ATTACK)
        super().shoot(camera)
