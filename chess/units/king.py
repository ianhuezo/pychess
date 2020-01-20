from .unit import Unit
import math

class King(Unit):
    value = math.inf
    char = "Ki"
    def __init__(self, team):
        super().__init__(team)
        pass

    def move(self):
        """
        King is omnidirectional
        """
        return "up", "down", "left", "right", "topleft", "topright", "downleft", "downright"