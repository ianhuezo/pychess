from chess.units import Unit, Empty, Suggestion, Enemy
from typing import List
from collections import deque
from math import inf
import math

class Point:
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

class Board:
    def __init__(self):
        
        #the actual board
        self.coordinates: List[Point] = [[Point(row=i,col=j,piece = Empty("none")) for i in range(8)] for j in range(8)]
        self.movement_maps = {
            "R": (inf, self.cardinal_directions),
            "Q": (inf, self.omni_directions),
            "Ki": (1, self.omni_directions),
            "B": (inf, self.slope_directions),
            "P": (1, self.pawn_directions),
            "Kn": (1, self.knight_directions) #TODO
        }
        

    def __repr__(self):
        output = ""
        for row in self.coordinates:
            output += "{} {} {} {} {} {} {} {}\n".format(*map(lambda x: x.piece.char, row))
        return output

    def move_map(self,point: Point):
        name = point.piece.char
        return self.movement_maps[name]


    def update(self, unit_on_board: Point):
        initial_position = unit_on_board
        point_queue = deque([unit_on_board])
        limit, direction_func = self.move_map(initial_position)
        early_end = 0
        while point_queue and early_end < limit:
            point = point_queue.popleft()
            for neighbor in direction_func(point, initial_position):
                if initial_position == neighbor:
                    continue
                current = self.coordinates[neighbor.row][neighbor.col]
                if current.piece.char == "-":
                    self.insert_piece(neighbor)
                    point_queue.append(neighbor)
                elif current.piece.char != "*" and current.piece.team != initial_position.piece.team:
                    enemy = Enemy(neighbor.piece.team)
                    self.insert_piece(Point(neighbor.row, neighbor.col, enemy))
            early_end += 1

    def omni_directions(self, point, initial_position):
        return self.slope_directions(point, initial_position) + self.cardinal_directions(point, initial_position)

    def slope_directions(self, point, initial_position):
        neighbors = []
        suggestion = Suggestion("None")
        up = point.row - 1
        down = point.row + 1
        left = point.col - 1
        right = point.col + 1
        #y = x, so as long as the slope of the
        #initial position is the same, then it's fine
        in_bounds = up > -1 and left > -1 and right < len(self.coordinates) and down < len(self.coordinates)
        slope_topright = abs(right - initial_position.col) > 0 and abs(up - initial_position.row) / abs(right - initial_position.col) == 1
        slope_topleft = abs(left - initial_position.col) > 0 and abs(up - initial_position.row) / abs(left - initial_position.col) == 1
        slope_downleft =  abs(left - initial_position.col) > 0 and abs(down - initial_position.row) / abs(left - initial_position.col) == 1
        slope_downright = abs(right - initial_position.col) > 0 and abs(down - initial_position.row) / abs(right - initial_position.col) == 1
        if in_bounds  and slope_topleft:
            neighbors.append(Point(row=up, col=left, piece=suggestion))
        if in_bounds and slope_topright:
            neighbors.append(Point(row=up, col=right, piece=suggestion))
        if in_bounds  and slope_downright:
            neighbors.append(Point(row=down, col=right, piece=suggestion))
        if in_bounds  and slope_downleft:
            neighbors.append(Point(row=down, col=left, piece=suggestion))

        return neighbors


    
    def cardinal_directions(self,point, initial_position):
        """
        Vertical and horizaontal positions for the chess board mapped
        for the unit
        """
        neighbors = []
        suggestion = Suggestion("None")
        up = point.row - 1
        down = point.row + 1
        left = point.col - 1
        right = point.col + 1
        if up > -1  and point.col == initial_position.col:
            neighbors.append(Point(row=up, col=point.col, piece=suggestion))
        if down < len(self.coordinates)  and point.col == initial_position.col:
            neighbors.append(Point(row=down, col=point.col, piece=suggestion))
        if left > -1  and point.row == initial_position.row:
            neighbors.append(Point(row=point.row, col=left, piece=suggestion))
        if right < len(self.coordinates) and point.row == initial_position.row:
            neighbors.append(Point(row=point.row, col=right, piece=suggestion))

        return neighbors

    def pawn_directions(self, point, initial_position):
        """
        -1: looks up from current pawn
        1: looks down from current pawn
        """
        neighbors = []
        move_direction = point.piece.team
        suggestion = Suggestion("None")
        in_bounds_col = point.col + 1 < len(self.coordinates) and point.col - 1 > -1
        in_bounds_row = point.row + move_direction > -1 and point.row + move_direction < len(self.coordinates)
        in_bounds = in_bounds_col and in_bounds_row
        if(in_bounds and self.coordinates[point.row + move_direction][point.col + 1].piece.team != move_direction and
           self.coordinates[point.row + move_direction][point.col + 1].piece.char != "-"):
            neighbors.append(Point(row=point.row + move_direction, col = point.col + 1, piece= suggestion))
        if(in_bounds and self.coordinates[point.row + move_direction][point.col -1].piece.team != move_direction and
           self.coordinates[point.row + move_direction][point.col - 1].piece.char != "-"):
            neighbors.append(Point(row=point.row + move_direction, col = point.col - 1, piece= suggestion))
        if(in_bounds):
            neighbors.append(Point(row=point.row + move_direction, col = point.col, piece= suggestion))
        return neighbors

    def knight_directions(self, point, initial_position):
        neighbors = []
        suggestion = Suggestion("None")
        point_1 = (point.row -2, point.col + 1)
        point_2 = (point.row - 1, point.col + 2)
        point_3 = (point.row + 1, point.col +  2)
        point_4 = (point.row + 2, point.col + 1)
        point_5 = (point.row + 2, point.col - 1)
        point_6 = (point.row + 1, point.col - 2)
        point_7 = (point.row - 1, point.col - 2)
        point_8 = (point.row - 2, point.col - 1)
        all_points = (point_1, point_2,point_3,point_4,point_5,point_6,point_7,point_8)

        for row, col in all_points:
            in_bounds = row > -1 and row < len(self.coordinates) and col > -1 and col < len(self.coordinates)
            if in_bounds:
                neighbors.append(Point(row=row, col=col, piece=suggestion))
        return neighbors

    def insert_piece(self, point: Point):
        if point.row < len(self.coordinates) and point.col < len(self.coordinates[0]):
            self.coordinates[point.row][point.col] = point
        else:
            raise IndexError("Coordinate inserted is out of range ({}, {})".format(point.row, point.col))

    def __len__(self):
        return len(self.coordinates)