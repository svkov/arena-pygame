
from src.global_objects import game_objects, projectile_objects

def spawn_object(obj):
    game_objects.add(obj)

def spawn_projectile(obj):
    projectile_objects.add(obj)
    
def crop_spritesheet(image):
    print(image.get_size())
    im1 = image.subsurface([0, 0, 512, 512])
    im2 = image.subsurface([512, 0, 512, 512])
    return im1, im2