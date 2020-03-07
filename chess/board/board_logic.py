from chess.units import Unit, Empty, Suggestion, Enemy
from chess.board.point import Point
from collections import deque
from math import inf
import math


class BoardLogic:
    """
    Class logic to control unit behavior for chess

    """
    def __init__(self, board_coordinates):
        self.coordinates = board_coordinates
        self.movement_maps = {
            "R": (inf, self.cardinal_directions),
            "Q": (inf, self.omni_directions),
            "Ki": (1, self.omni_directions),
            "B": (inf, self.slope_directions),
            "P": (1, self.pawn_directions),
            "Kn": (1, self.knight_directions)
        }

    def move_map(self,point: Point):
        name = point.piece.char
        return self.movement_maps[name]

    def moves(self, unit_on_board: Point):
        initial_position = unit_on_board
        point_queue = deque([unit_on_board])
        limit, direction_func = self.move_map(initial_position)
        early_end = 0
        in_check = False
        potential_moves = []
        while point_queue and early_end < limit:
            point = point_queue.popleft()
            for neighbor in direction_func(point, initial_position):
                if initial_position == neighbor:
                    continue
                current = self.coordinates[neighbor.row][neighbor.col]
                if current.piece.char == "-":
                    potential_moves.append(neighbor)
                    point_queue.append(neighbor)
                elif current.piece.char != "*" and current.piece.team != initial_position.piece.team and current.piece.char == "Ki":
                    enemy = Enemy(neighbor.piece.team)
                    potential_moves.append((Point(neighbor.row, neighbor.col, enemy)))
                    in_check = True
                elif current.piece.char != "*" and current.piece.team != initial_position.piece.team:
                    enemy = Enemy(neighbor.piece.team)
                    potential_moves.append((Point(neighbor.row, neighbor.col, enemy)))
            early_end += 1
        return potential_moves, in_check

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
