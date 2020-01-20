from .unit import Unit

class Bishop(Unit):
    value = 3
    char = "B"
    def __init__(self, team):
        super().__init__(team)
        pass

    def move(self):
        return "topleft", "topright", "downleft", "downright"