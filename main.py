from chess.board import Board
from setup import setup_units
from collections import deque


if __name__ == "__main__":
    board = Board()
    
    #put board setup here
    setup_units(board)

    #this would be triggered by a person's click
    #but will be simulated by just hard coding for now
    # board.scope_units(queen_on_board) #the player selects the unit

    print(board)
    board.view_overlay()