from src.animation import AnimationManager
from src.animation.states import EnemyStates
from src.game_object.enemy import Enemy

class AnimatedEnemy(Enemy):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.animation_manager = AnimationManager(kwargs['animation_states'], default_state=EnemyStates.WALK)
        self.animation_manager.set_state(EnemyStates.WALK)
        self.image = self.animation_manager.image

    def update_animation_if_needed(self):
        if super().update_animation_if_needed():
            return
        self.set_walk_animation()
        self.animation_manager.update()
        self.image = self.animation_manager.image

    def set_walk_animation(self):
        not_attack = self.animation_manager._state != EnemyStates.ATTACK
        not_next_attack = self.animation_manager.next_state != EnemyStates.ATTACK
        if self.is_moving and not_attack and not_next_attack:
            self.animation_manager.set_state(EnemyStates.WALK)

    def shooted(self):
        self.animation_manager.set_state(EnemyStates.ATTACK, force=True)
        return super().shooted()
