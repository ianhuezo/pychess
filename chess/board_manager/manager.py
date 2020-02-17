#things I intend to have in this module: check, castling, turning pawn into different unit
#board setup
#keep track of players turns
#

class BoardManager:
    def __init__(self):


    def scope_units(self, unit_on_board: Point):
        """
        typically  called when the player select a chess piece, but
        hasn't made their move yet
        """
        unit_moves = self.logic.moves(unit_on_board)
        for move in unit_moves:
            self.insert_overlay(move)