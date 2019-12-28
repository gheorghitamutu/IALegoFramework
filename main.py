class Piece:
    def __init__(self, size, filled_cells=None, fill_all=False):
        self.n = size[0]
        self.m = size[1]
        self.matrix = [[1 if fill_all else 0] * self.n for _ in range(self.m)]

        if fill_all is False and filled_cells is not None:
            for i in filled_cells:
                self.matrix[i[0]][i[1]] = 1

    def output_matrix(self):
        for i in self.matrix:
            for j in i:
                print("{} ".format(j), end="")
            print()


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

    Piece((3, 3), [(0, 0), (0, 1), (1, 0),(2, 0),(1, 1),(2, 1), (2,2)]),
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

for piece in piece_list:
    piece.output_matrix()
    print()

