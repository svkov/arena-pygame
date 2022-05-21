from src.item import InventoryItem


class Inventory:

    def __init__(self) -> None:
        self.width = 6
        self.height = 3
        self.size = self.width * self.height
        self.empty_space = self.size
        self.inventory = [[None for j in range(self.width)] for i in range(self.height)]

    def is_enough_space(self):
        return self.empty_space > 0

    def is_empty(self):
        return self.empty_space == self.size

    def add(self, item: InventoryItem):
        inserted = False
        for i in range(self.height):
            for j in range(self.width):
                if self.inventory[i][j] is None:
                    self.inventory[i][j] = item
                    self.empty_space -= 1
                    inserted = True
                    break
            if inserted:
                break

    def sort(self):
        new_inventory = [[None for j in range(self.width)] for i in range(self.height)]
        items = self.as_list()
        for i in range(self.height):
            for j in range(self.width):
                if len(items) == 0:
                    self.inventory = new_inventory
                    return
                new_inventory[i][j] = items.pop()

    def remove(self, item: InventoryItem):
        removed = False
        for i in range(self.height):
            for j in range(self.width):
                if self.inventory[i][j] is item:
                    self.inventory[i][j] = None
                    self.empty_space += 1
                    removed = True
                    break
            if removed:
                break
        self.sort()

    def contains(self, class_item):
        for i in range(self.height):
            for j in range(self.width):
                if isinstance(self.inventory[i][j], class_item):
                    return self.inventory[i][j]
        return None

    def as_list(self):
        inventory_list = []
        for i in range(self.height):
            for j in range(self.width):
                if self.inventory[i][j] is not None:
                    inventory_list.append(self.inventory[i][j])
        return inventory_list

    def set_new_owner(self, owner):
        for i in range(self.height):
            for j in range(self.width):
                if self.inventory[i][j]:
                    self.inventory[i][j].owner = owner

    def get_item(self, i, j):
        return self.inventory[i][j]

    def __str__(self):
        string = ''
        for i in range(self.height):
            for j in range(self.width):
                if self.inventory[i][j]:
                    string += str(self.inventory[i][j]) + '\n'
        return string
