from src.game_object import GameObject


class Portal(GameObject):

    def __init__(self, *args, **kwargs) -> None:
        self.is_activated = True
        self.deactivated_image = kwargs.get('deactivated_image')
        self.activated_image = kwargs.get('activated_image')
        super().__init__(*args, **kwargs)
        self.deactivate_portal()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.set_image_size(self.image_size)

    def activate_portal(self):
        self.image = self.activated_image

    def deactivate_portal(self):
        self.image = self.deactivated_image

    @classmethod
    def create_portal(cls, *args, portal_color='portal_pink', **kwargs):
        sprites = kwargs.get('sprites')
        kwargs['activated_image'] = sprites[portal_color]
        kwargs['deactivated_image'] = sprites['portal_deactivated']
        return Portal(*args, **kwargs)
