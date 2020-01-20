from .unit import Unit

class Rook(Unit):
    value = 5
    char = "R"
    def __init__(self, team):
        super().__init__(team)
        pass

    def move(self):
        return "up", "down", "left", "right"