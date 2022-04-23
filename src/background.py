from src.game_object import GameObject


class Background(GameObject):

    def __init__(self, pos, image, image_size=None, **kwargs) -> None:
        super().__init__(pos, image, image_size, **kwargs)
        self.radius = kwargs['radius']
