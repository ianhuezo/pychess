from chess.units import *
from chess.board.point import Point
from chess.board.board_logic import BoardLogic
from typing import List, Dict, Optional
from math import inf

class Board:
    def __init__(self):
        
        #the actual board and it's representation
        self.coordinates: List[Point] = [[Point(row=i,col=j,piece = Empty("none")) for i in range(8)] for j in range(8)]
        #an overaly displaying(more like underaly) potential moves of the current piece
        self.move_overlay: List[Point] = [[Point(row=i,col=j,piece = Empty("none")) for i in range(8)] for j in range(8)]
        self.check_overlay: List[Point] = [[Point(row=i,col=j,piece = Empty("none")) for i in range(8)] for j in range(8)]
        self.player_turn = 1
        self.king_1 = None
        self.king_2 = None
        self.setup()
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

    def king_in_check(self) -> bool:
        """
        typically  called when the player select a chess piece, but
        hasn't made their move yet
        """
        checked_king: Optional[Point] = None
        check_counter = 0
        if player_turn is 1:
            checked_king = self.king_1
        elif player_turn is -1:
            checked_king = self.king_2
        else:
            raise ValueError("Turn is not valid, must be either 1 or -1")

        check_logic = BoardLogic(self.check_overlay)
        #first get all of the kings potential moves
        unit_moves, _ = check_logic.moves(checked_king)
        #update the overlay to have every potential overlay, with the king on it
        possible_moves = len(unit_moves)
        for move in unit_moves:
            self.check_overlay(Point(move.row, move.col, checked_king))
        #update the logic
        check_logic = BoardLogic(self.check_overlay)
        #now look at the other pieces and see if any can attack the king
        for row in self.check_overlay:
            for col in row:
                if (checked_king.piece.team != col.piece.team and
                    col.piece.char in check_logic.movement_maps.keys()):
                        unit_moves, is_check = check_logic.moves(checked_king)
                        if is_check is True:
                            return True
        return False

    def scope_units(self, unit_on_board: Point):
        """
        typically  called when the player select a chess piece, but
        hasn't made their move yet
        """
        self.unscope_units()
        unit_moves, _ = self.logic.moves(unit_on_board)
        for move in unit_moves:
            self.insert_overlay(move)

    def unscope_units(self):
        self.move_overlay = self.coordinates

    def insert_all(self, point: Point):
        """
        Used to assign boards to the next state.  This call should be made primarily
        for when going to a different turn.  However is called on all units
        before for setup
        """
        #TODO
        # if self.king_in_check():

        self.unscope_units()
        self.insert_piece(point)
        self.insert_overlay(point)
        self.check_overlay = self.coordinates

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

    def check_overlay(self, point: Point):
        if point.row < len(self.coordinates) and point.col < len(self.coordinates[0]):
            self.check_overlay[point.row][point.col] = point
        else:
            raise IndexError("Coordinate inserted is out of range ({}, {})".format(point.row, point.col))

    def setup(self):
        """
        Setup function for the board, puts the units in the original
        chess position
        """
        side_1: Dict = {
            "queen_1": Point(0, 3, Queen(1)),
            "king_1": Point(0, 4, King(1)),
            "rook_1_left": Point(0, 0, Rook(1)),
            "bishop_1_left" : Point(0, 2, Bishop(1)),
            "knight_1_left" : Point(0, 1, Knight(1)),
            "rook_1_right": Point(0, 7, Rook(1)),
            "bishop_1_right" : Point(0, 5, Bishop(1)),
            "knight_1_right" : Point(0, 6, Knight(1)),
        }

        side_2: Dict = {
            "queen_2": Point(7, 3, Queen(-1)),
            "king_2": Point(7, 4, King(-1)),
            "rook_2_left": Point(7, 0, Rook(-1)),
            "bishop_2_left" : Point(7, 2, Bishop(-1)),
            "knight_2_left" : Point(7, 1, Knight(-1)),
            "rook_2_right": Point(7, 7, Rook(-1)),
            "bishop_2_right" : Point(7, 5, Bishop(-1)),
            "knight_2_right" : Point(7, 6, Knight(-1)),
        }

        for k1, k2 in zip(side_1, side_2):
            if "king" in k1:
                self.king_1, self.king_2 = side_1[k1], side_2[k2]
            self.insert_all(side_1[k1])
            self.insert_all(side_2[k2])


        pawn_1 =  Pawn(1)
        pawn_2 = Pawn(-1)
        for x in range(8):
            pawn_side_1 = Point(1, x, pawn_1)
            self.insert_all(pawn_side_1)

            pawn_side_2 = Point(6, x, pawn_2)
            self.insert_all(pawn_side_2)

    def __len__(self):
        return len(self.coordinates)