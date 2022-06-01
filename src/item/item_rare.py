from enum import Enum


class ItemRare(Enum):
    COMMON = 1
    RARE = 2
    LEGENDARY = 3


rare_to_color = {
    ItemRare.COMMON: '#4a4a4a',
    ItemRare.RARE: '#338726',
    ItemRare.LEGENDARY: '#ad1822'
}

rare_to_name = {
    ItemRare.COMMON: 'Common',
    ItemRare.RARE: 'Rare',
    ItemRare.LEGENDARY: 'Legendary'
}
