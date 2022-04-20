from src.enemy import Enemy
from src.utils import crop_spritesheet


class AnimatedEnemy(Enemy):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.spritesheet_image = self.image.copy()
        self.images = crop_spritesheet(self.spritesheet_image)
        self.image = self.images[0]
        self.anim_counter = 0

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)
        self.anim_counter = (self.anim_counter + 1) % len(self.images)
        self.image = self.images[self.anim_counter]
