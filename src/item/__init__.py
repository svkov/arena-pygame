from src.game_object import GameObject
from src.hud.ingame_label import ItemNameLabel
from src.item.item_rare import ItemRare, rare_to_color, rare_to_name


class InventoryItem(GameObject):
    name = ''
    description = ''
    item_rare = ItemRare.COMMON

    def __init__(self, pos, image, image_size, owner, **kwargs) -> None:
        super().__init__(pos, image, image_size, **kwargs)
        self.owner = owner
        self.is_using_now = False

    def update(self, *args, **kwargs):
        show_items = kwargs.get('show_items', False)
        if self.owner is None:
            if show_items:
                self.spawn_item_name_label()
            return super().update(*args, **kwargs)
        self.rect.x = int(self.pos[0])
        self.rect.y = int(self.pos[1])

    def spawn_item_name_label(self):
        label = ItemNameLabel(self, self.camera.to_screen_coord(self.pos), self.camera)
        self.groups.ui_objects.add(label)

    def update_zoom(self):
        if self.owner is None:
            return super().update_zoom()

    def on_use(self):
        pass

    def on_collision(self, obj):
        return super().on_collision(obj)

    def on_pickup(self, owner):
        self.owner = owner
        self.image = self.image_by_zoom[1]

    def on_drop(self, pos):
        self.owner = None
        self.pos = pos

    @property
    def item_rare_name(self):
        return rare_to_name[self.item_rare]

    @property
    def item_rare_color(self):
        return rare_to_color[self.item_rare]
