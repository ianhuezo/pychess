from chess.units.unit import Unit, Queen, King, Knight, Rook, Pawn, Bishop


def setup_units():
    #setup of all 32 pieces
    queen_1 = Queen(1)
    pawn_1 = Pawn(1)
    king_1 = King(1)
    rook_1 = Rook(1)
    bishop_1 = Bishop(1)
    knight_1 = Knight(1)

    queen_2 = Queen(2)
    pawn_2 = Pawn(2)
    king_2 = King(2)
    rook_2 = Rook(2)
    bishop_2 = Bishop(2)
    knight_2 = Knight(2)

    movement_maps = {
        "R": (inf, self.cardinal_directions),
        "Q": (inf, self.omni_directions),
        "Ki": (1, self.omni_directions),
        "B": (inf, self.slope_directions),
        "P": (1, self.pawn_directions),
        "Kn": (1, self.knight_directions)
    }