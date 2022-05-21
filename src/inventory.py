from src.item import InventoryItem


class Inventory:

    def __init__(self) -> None:
        self.width = 6
        self.height = 3
        self.size = self.width * self.height
        self.empty_space = self.size
        self.inventory = [[None for i in range(self.width)] for j in range(self.height)]

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
        new_inventory = [[None for i in range(self.width)] for j in range(self.height)]
        filled = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.inventory[i][j] is not None:
                    new_inventory[filled // self.height][filled % self.width] = self.inventory[i][j]
                    filled += 1
        self.inventory = new_inventory

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

    def get_item(self, i, j):
        return self.inventory[i][j]

    def __str__(self):
        string = ''
        for i in range(self.height):
            for j in range(self.width):
                if self.inventory[i][j]:
                    string += str(self.inventory[i][j]) + '\n'
        return string
