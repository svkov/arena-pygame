import pygame

from src.game_object import GameObject


class HpBar:

    def __init__(self, owner: GameObject, size=None):
        self.owner = owner

        self.size = size
        if size is None:
            self.size = (self.owner.image_size[0], 10)

    def update(self, screen):
        pos_x = int(self.owner.pos[0])
        pos_y = int(self.owner.pos[1] - self.owner.image_size[1] // 2)
        pos = [pos_x, pos_y]
        progress = self.owner.hp / self.owner.max_hp
        new_size = [int(self.size[0] * progress), self.size[1]]
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(*pos, *self.size))
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(*pos, *new_size))
