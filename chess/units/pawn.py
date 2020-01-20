from .unit import Unit

class Pawn(Unit):
    value = 1
    char = "P"
    def __init__(self, team):
        super().__init__(team)
        pass

    def move(self):
        return "forward"