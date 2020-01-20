from .unit import Unit

class Knight(Unit):
    value = 3
    char = "Kn"
    def __init__(self, team):
        super().__init__(team)
        pass

    def move(self):
        """
        return L shape permutations for the board
        """
        return ""