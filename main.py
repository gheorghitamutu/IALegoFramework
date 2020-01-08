from piece import Piece
from super_piece import SuperPiece

piece_list = [
    Piece((2, 2), [(0, 0), (0, 1), (1, 0)]),
    Piece((12, 2), fill_all=True),
    Piece((2, 12), fill_all=True),
    Piece((2, 6), fill_all=True),
    Piece((6, 2), fill_all=True),
    Piece((1, 1), fill_all=True),
    Piece((1, 2), fill_all=True),
    Piece((2, 1), fill_all=True),
    Piece((1, 8), fill_all=True),
    Piece((8, 1), fill_all=True),

    Piece((3, 3), [(0, 0), (0, 1), (1, 0), (2, 0), (1, 1), (2, 1), (2, 2)]),
    Piece((2, 2), [(0, 0), (0, 1), (1, 1)]),
    Piece((3, 3), [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (2, 2)]),
    Piece((3, 3), [(0, 0), (0, 1), (1, 0), (1, 1), (0, 2), (1, 2), (2, 2)]),
    Piece((3, 4), fill_all=True),
    Piece((3, 1), fill_all=True),
    Piece((1, 3), fill_all=True),
    Piece((4, 3), fill_all=True),
    Piece((2, 2), fill_all=True),
    Piece((5, 2), fill_all=True)
]

super_piece = SuperPiece(piece_list)
super_piece.output_piece_plotly()
