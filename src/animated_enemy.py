from enum import Enum
from src.animation import Animation
from src.enemy import Enemy


class EnemyStates(Enum):
    IDLE = 0
    WALK = 1
    ATTACK = 2

class AnimatedEnemy(Enemy):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.animation = Animation(self.image.copy(), duration=0.4, fps=30, image_size=(512, 512))
        self.image = self.animation.get_image()
        self.state_to_animation = {
            EnemyStates.WALK: self.animation
        }

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)
        self.animation.update()
        self.image = self.animation.get_image()
