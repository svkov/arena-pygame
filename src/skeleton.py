from src.animated_enemy import EnemyStates
from src.animation import Animation

def generate_skeleton_states(sprites, fps):
    return {
        EnemyStates.IDLE: Animation(sprites['skeleton'], duration=0.3, fps=fps, image_size=(512, 512)),
        EnemyStates.WALK: Animation(sprites['skeleton_walk'], duration=0.3, fps=fps, image_size=(512, 512)),
        EnemyStates.ATTACK: Animation(sprites['skeleton_attack'], duration=0.3,
                                      fps=fps, image_size=(512, 512), times_to_play=1)
    }
