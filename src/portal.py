from src.game_object import GameObject
from src.item.quest_item import StoneSoulItem


class Portal(GameObject):

    def __init__(self, *args, **kwargs) -> None:
        self.is_activated = False
        self.deactivated_image = kwargs.get('image')
        self.activated_image = kwargs.get('activated_image')
        super().__init__(*args, **kwargs)
        self.deactivate_portal()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

    def activate_portal(self):
        self.is_activated = True
        self.image = self.activated_image
        self.set_image_size(self.image_size)

    def deactivate_portal(self):
        self.is_activated = False
        self.image = self.deactivated_image
        self.set_image_size(self.image_size)

    def on_interact(self, actor):
        if not self.is_activated:
            self.try_to_activate(actor)
        else:
            self.go_to_portal(actor)

    def try_to_activate(self, actor):
        stone_soul = actor.inventory.contains(StoneSoulItem)
        if stone_soul:
            actor.use_quest_item(stone_soul)
            self.activate_portal()

    def go_to_portal(self, actor):
        actor.go_to_portal()

    @classmethod
    def create_portal(cls, *args, portal_color='portal_pink', **kwargs):
        sprites = kwargs.get('sprites')
        kwargs['activated_image'] = sprites[portal_color]
        return Portal(*args, **kwargs)
