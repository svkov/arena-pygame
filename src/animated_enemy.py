from src.animation import AnimationManager
from src.animation.states import EnemyStates
from src.enemy import Enemy

class AnimatedEnemy(Enemy):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.animation_manager = AnimationManager(kwargs['animation_states'], default_state=EnemyStates.WALK)
        self.animation_manager.set_state(EnemyStates.WALK)
        self.image = self.animation_manager.image

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)
        self.set_walk_animation()
        self.animation_manager.update()
        self.image = self.animation_manager.image

    def set_walk_animation(self):
        moving = abs(self.speed[0]) > 0 or abs(self.speed[1]) > 0
        not_attacking = self.animation_manager._state != EnemyStates.ATTACK or \
            self.animation_manager.next_state != EnemyStates.ATTACK
        print(moving, not_attacking)
        if moving and not not_attacking:
            self.animation_manager.set_state(EnemyStates.WALK)

    def shooted(self):
        self.animation_manager.set_state(EnemyStates.ATTACK)
        return super().shooted()
