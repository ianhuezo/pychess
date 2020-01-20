
from chess.units import (Queen, King, Pawn, Rook, Bishop, Knight, Suggestion)
from chess.board import Board, Point
from collections import deque


if __name__ == "__main__":
    board = Board()
    
    queen = Knight(1)
    pawn = Pawn(-1)
    #this would be triggered by a person's click
    #but will be simulated by just hard coding for now
    queen_on_board = Point(4,1,queen)
    board.insert_piece(queen_on_board)
    board.insert_piece(Point(3,3,pawn))
    board.update(queen_on_board)

    print(board)