from chess.units import Unit, Empty, Suggestion, Enemy
from chess.board.point import Point
from chess.board.board_logic import BoardLogic
from typing import List

class Board:
    def __init__(self):
        
        #the actual board and it's representation
        self.coordinates: List[Point] = [[Point(row=i,col=j,piece = Empty("none")) for i in range(8)] for j in range(8)]
        #an overaly displaying(more like underaly) potential moves of the current piece
        self.move_overlay: List[Point] = [[Point(row=i,col=j,piece = Empty("none")) for i in range(8)] for j in range(8)]
        self.logic = BoardLogic(self.coordinates)

    def view_overlay(self):
        output = ""
        for row in self.move_overlay:
            output += "{} {} {} {} {} {} {} {}\n".format(*map(lambda x: x.piece.char, row))
        print(output)

    def __repr__(self):
        output = ""
        for row in self.coordinates:
            output += "{} {} {} {} {} {} {} {}\n".format(*map(lambda x: x.piece.char, row))
        return output

    def scope_units(self, unit_on_board: Point):
        """
        typically  called when the player select a chess piece, but
        hasn't made their move yet
        """
        unit_moves = self.logic.moves(unit_on_board)
        for move in unit_moves:
            self.insert_overlay(move)

    def insert_all(self, point: Point):
        """
        Used to assign boards to the next state.  This call should be made primarily
        for when going to a different turn.  However is called on all units
        before for setup
        """
        self.insert_piece(point)
        self.insert_overlay(point)
        self.logic.coordinates = self.coordinates

    def insert_piece(self, point: Point):
        if point.row < len(self.coordinates) and point.col < len(self.coordinates[0]):
            self.coordinates[point.row][point.col] = point
        else:
            raise IndexError("Coordinate inserted is out of range ({}, {})".format(point.row, point.col))

    def insert_overlay(self, point: Point):
        if point.row < len(self.coordinates) and point.col < len(self.coordinates[0]):
            self.move_overlay[point.row][point.col] = point
        else:
            raise IndexError("Coordinate inserted is out of range ({}, {})".format(point.row, point.col))

    def __len__(self):
        return len(self.coordinates)