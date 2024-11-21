class Item:
    def __init__(self, id, name, desc, outDesc, damage, state, listPrevItem, evolveItem):
        self.id = id
        self.name = name
        self.desc = desc
        self.outDesc = outDesc
        self.damage = damage
        self.state = state
        self.listPrevItem = listPrevItem
        self.evolveItem = evolveItem
