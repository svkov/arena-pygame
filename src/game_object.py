import numpy as np
import pygame

class GameObject(pygame.sprite.Sprite):

    def __init__(self, pos, image, image_size=None) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.pos = np.array(pos, dtype=np.float)
        self.image_size = image_size
        if image_size is None:
            self.image_size = (128, 128)

        self.image: pygame.surface.Surface = image
        self.image = pygame.transform.scale(self.image, self.image_size)

        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def update(self, *args, **kwargs):
        camera = kwargs['camera']
        new_pos = camera.to_screen_coord(self.pos)
        self.rect.x = int(new_pos[0])
        self.rect.y = int(new_pos[1])

    @property
    def center(self):
        return (self.rect.x + self.image_size[0] // 2, self.rect.y + self.image_size[1] // 2)

    def on_collision(self, obj):
        pass

    @property
    def damage(self):
        return 0
