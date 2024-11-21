from array import array


class Player:
    def __init__(self, id, name, desc, itemList, goalList, hitPoint, gold):
        self.id = id
        self.name = name
        self.desc = desc
        self.itemList = array(itemList)
        self.goalList = array(goalList)
        self.hitPoint = hitPoint
        self.gold = gold
