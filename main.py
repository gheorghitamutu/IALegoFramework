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


piece = Piece((12, 2), fill_all=True)
piece.output_matrix()
