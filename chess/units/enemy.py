from .unit import Unit

class Enemy(Unit):
    value = 0
    char = "E"
    def __init__(self, team):
        super().__init__(team)
        pass

    def move(self):
        return [1,5]