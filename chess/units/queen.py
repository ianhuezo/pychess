from .unit import Unit

class Queen(Unit):
    value = 9
    char = "Q"
    def __init__(self, team):
        super().__init__(team)
        pass

    def move(self):
        return "up", "down", "left", "right", "topleft", "topright", "downleft", "downright"