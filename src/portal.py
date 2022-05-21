from src.game_object import GameObject


class Portal(GameObject):

    def __init__(self, *args, **kwargs) -> None:
        self.is_activated = True
        self.deactivated_image = kwargs.get('image')
        self.activated_image = kwargs.get('activated_image')
        super().__init__(*args, **kwargs)
        self.deactivate_portal()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

    def activate_portal(self):
        self.image = self.activated_image
        self.set_image_size(self.image_size)

    def deactivate_portal(self):
        self.image = self.deactivated_image
        self.set_image_size(self.image_size)

    def on_interact(self, actor):
        if not actor.inventory.is_empty():
            self.activate_portal()
        else:
            self.deactivate_portal()

    @classmethod
    def create_portal(cls, *args, portal_color='portal_pink', **kwargs):
        sprites = kwargs.get('sprites')
        kwargs['activated_image'] = sprites[portal_color]
        return Portal(*args, **kwargs)
