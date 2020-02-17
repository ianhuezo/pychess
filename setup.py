from chess.units import *
from chess.board import Board
from chess.board import Point
from typing import Dict
from math import inf

def setup_units(board: Board):
    #setup of all 32 pieces
    side_1: Dict = {
        "queen_1": Point(0, 3, Queen(1)),
        "king_1": Point(0, 4, King(1)),
        "rook_1_left": Point(0, 0, Rook(1)),
        "bishop_1_left" : Point(0, 2, Bishop(1)),
        "knight_1_left" : Point(0, 1, Knight(1)),
        "rook_1_right": Point(0, 7, Rook(1)),
        "bishop_1_right" : Point(0, 6, Bishop(1)),
        "knight_1_right" : Point(0, 5, Knight(1)),
    }

    side_2: Dict = {
        "queen_2": Point(7, 3, Queen(-1)),
        "king_2": Point(7, 4, King(-1)),
        "rook_2_left": Point(7, 0, Rook(-1)),
        "bishop_2_left" : Point(7, 2, Bishop(-1)),
        "knight_2_left" : Point(7, 1, Knight(-1)),
        "rook_2_right": Point(7, 7, Rook(-1)),
        "bishop_2_right" : Point(7, 6, Bishop(-1)),
        "knight_2_right" : Point(7, 5, Knight(-1)),
    }

    for k1, k2 in zip(side_1, side_2):
        board.insert_all(side_1[k1])
        board.insert_all(side_2[k2])


    pawn_1 =  Pawn(1)
    pawn_2 = Pawn(-1)
    for x in range(8):
        pawn_side_1 = Point(1, x, pawn_1)
        board.insert_all(pawn_side_1)

        pawn_side_2 = Point(6, x, pawn_2)
        board.insert_all(pawn_side_2)





    