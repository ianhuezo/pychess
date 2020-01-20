from .unit import Unit

class Empty(Unit):
    value = 0
    char = "-"
    def __init__(self, team):
        super().__init__(team)
        pass

    def move(self):
        return [1,5]