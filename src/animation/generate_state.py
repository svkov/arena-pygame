from src.animation import Animation
from src.animation.states import EnemyStates, PlayerStates


def skeleton(sprites, fps, camera):
    return {
        EnemyStates.IDLE: Animation(sprites['skeleton'], duration=0.3, fps=fps, camera=camera, image_size=(512, 512)),
        EnemyStates.WALK: Animation(sprites['skeleton_walk'], duration=0.3, fps=fps, camera=camera,
                                    image_size=(512, 512), times_to_play=1),
        EnemyStates.ATTACK: Animation(sprites['skeleton_attack'], duration=0.2, camera=camera,
                                      fps=fps, image_size=(512, 512), times_to_play=1)
    }

def player(sprites, fps, camera):
    shared_args = dict(
        fps=fps,
        camera=camera,
        image_size=(512, 512)
    )
    return {
        PlayerStates.IDLE: Animation(sprites['knight_idle'],
                                     duration=0.4,
                                     times_to_play=1,
                                     **shared_args),
        PlayerStates.ATTACK: Animation(sprites['knight_attack'],
                                       duration=0.2,
                                       times_to_play=1,
                                       **shared_args),
        PlayerStates.BACK: Animation(sprites['knight_back'],
                                     duration=0.4,
                                     times_to_play=1,
                                     **shared_args),
        PlayerStates.WALK: Animation(sprites['knight_walk'],
                                     duration=0.5,
                                     times_to_play=1,
                                     **shared_args)
    }

def skeleton_die(sprites, fps, camera):
    return Animation(sprites['skeleton_die'], duration=0.8, fps=fps,
                     camera=camera, matrix_size=(4, 1), times_to_play=1)
