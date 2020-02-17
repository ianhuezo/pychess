from chess.units import Unit

class Point:
    """
    A generalized place on the board that can
    have any type of piece associated with it
    """
    def __init__(self, row, col,piece: Unit):
        self.row = row
        self.col = col
        self.piece = piece

    @property
    def position(self):
        """
        position returned as a tuple
        """
        return (self.row, self.col)

    def convert_position(self):
        """
        turns row/col into chess positions i.e. A3, etc
        """

    def __eq__(self, other):
        if other.row == self.row and other.col == self.col:
            return True
        return False
    
    def __ne__(self, other):
        return not self == other
    
    def __repr__(self):
        return "row: {} col: {} unit: {}".format(self.row, self.col, self.piece)